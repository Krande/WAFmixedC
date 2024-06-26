# coding=utf-8
# --------------------------------------------------------------------
# Copyright (C) 1991 - 2023 - EDF R&D - www.code-aster.org
# This file is part of code_aster.
#
# code_aster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# code_aster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with code_aster.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

import os
import pathlib
from pathlib import PureWindowsPath
from subprocess import PIPE, Popen

from waflib import Configure, Errors, Logs


def options(self):
    self.load("python")  # --nopyc/--nopyo are enabled below


def configure(self):
    self.check_python()
    self.check_numpy()
    self.check_asrun()
    self.check_mpi4py()


###############################################################################
@Configure.conf
def check_python(self):
    self.load("python")
    self.check_python_version((3, 5, 0))
    #self.check_python_headers()
    path = self.env["PATH"]
    include_dir = os.environ["CONDA_PREFIX"] + "/include"
    self.env["PATH"] = f"{path};{include_dir}"

    if "icc" in self.env.CC_NAME.lower():
        self.env["LIB_PYEXT"] = list(set(self.env["LIB_PYEXT"]))
        # Best is to clear PYEMBED and PYEXT {c/cxx}flags
        for lang in ("CFLAGS", "CXXFLAGS"):
            for feat in ("PYEMBED", "PYEXT"):
                self.env[lang + "_" + feat] = []
    try:
        self.check_python_module("yaml")
        self.env["CFG_EXT"] = "yaml"
    except Errors.ConfigurationError:
        self.env["CFG_EXT"] = "json"


@Configure.conf
def check_numpy(self):
    if not self.env["PYTHON"]:
        self.fatal("load python tool first")
    self.check_python_module("numpy")
    self.check_numpy_headers()


@Configure.conf
def check_numpy_headers(self):
    if not self.env["PYTHON"]:
        self.fatal("load python tool first")
    self.start_msg("Checking for numpy include")
    # retrieve includes dir from numpy module
    numpy_includes = self.get_python_variables(
        ['"\\n".join([np.get_include()])'],
        ["import numpy as np"],
    )
    python_include_dir = os.environ["CONDA_PREFIX"] + "/include"
    python_libs_dir = os.environ["CONDA_PREFIX"] + "/libs"
    numpy_includes.append(pathlib.Path(python_include_dir).as_posix())
    numpy_includes.append(pathlib.Path(python_libs_dir).as_posix())

    #Logs.warn(f"{numpy_includes=}")

    if self.is_defined("ASTER_PLATFORM_MINGW"):
        incs = [PureWindowsPath(i) for i in numpy_includes]
        numpy_includes = []
        for path in incs:
            parts = list(path.parts)
            if path.anchor:
                parts[0] = path.root
            for i, sub in enumerate(parts):
                if sub == "lib":
                    parts[i] = "Lib"
            numpy_includes.append(PureWindowsPath(*parts).as_posix())


    # check the given includes dirs
    self.check(
        feature="c",
        header_name="Python.h numpy/arrayobject.h",
        includes=numpy_includes,
        use=["PYEXT"],
        uselib_store="NUMPY",
        errmsg="Could not find the numpy development headers",
        linkflags=["/LIBPATH:" + python_libs_dir, "/LIBPATH:" + python_include_dir],
    )
    self.end_msg(numpy_includes)


@Configure.conf
def check_asrun(self):
    if not self.env["PYTHON"]:
        self.fatal("load python tool first")
    try:
        self.check_python_module("asrun")
    except Errors.WafError:
        # optional
        pass


@Configure.conf
def check_mpi4py(self):
    if not self.env.BUILD_MPI:
        return
    if not self.env["PYTHON"]:
        self.fatal("load python tool first")
    try:
        self.check_python_module("mpi4py")
    except Errors.ConfigurationError:
        if self.options.with_py_mpi4py:
            raise


@Configure.conf
def check_optimization_python(self):
    self.setenv("debug")
    self.env["PYC"] = self.env["PYO"] = 0
    self.setenv("release")
    self.env["PYC"] = self.env["PYO"] = 0


def _get_default_pythonpath(python):
    """Default sys.path should be added into PYTHONPATH"""
    env = os.environ.copy()
    env["PYTHONPATH"] = ""
    proc = Popen([python, "-c", "import sys; print(sys.path)"], stdout=PIPE, env=env)
    system_path = eval(proc.communicate()[0])
    return system_path
