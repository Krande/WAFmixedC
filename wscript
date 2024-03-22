import os

top = "."
out = "build"
install_suffix = os.environ.get("WAF_DEFAULT_VARIANT") or os.environ.get("WAF_SUFFIX", "mpi")
default_prefix = "../install/%s" % install_suffix


def options(self):
    self.load('clang_compilation_database', tooldir="config")
    orig_get_usage = self.parser.get_usage

    def _usage():
        return orig_get_usage() + os.linesep.join(
            (
                "",
                "Environment variables:",
                "  CC             : C compiler",
                "  FC             : Fortran compiler",
                "  CXX            : C++ compiler",
                "  DEFINES        : extra preprocessor defines",
                "  LINKFLAGS      : extra linker options",
                "  CFLAGS         : extra C compilation options",
                "  CXXFLAGS       : extra C++ compilation options",
                "  FCFLAGS        : extra Fortran compilation options",
                "  {C,CXX,FC}FLAGS_ASTER_DEBUG may be used to add options only in debug mode"
                '  LIBPATH_x, LIB_x, INCLUDES_x, PYPATH_x : paths for component "x" for libs, '
                "includes, python modules",
                "  CONFIG_PARAMETERS_name=value: extra configuration parameters "
                "(for config.yaml/json)",
                "  WAFBUILD_ENV   : environment file to be included in runtime " "environment file",
                "  PREFIX         : default installation prefix to be used, "
                "if no --prefix option is given.",
                "  ASTER_BLAS_INT_SIZE  : kind of integers to use in the fortran blas/lapack "
                "calls (4 or 8, default is 4)",
                "  ASTER_MUMPS_INT_SIZE : kind of integers to use in the fortran mumps calls "
                " (4 or 8, default is 4)",
                "  CATALO_CMD     : command line used to build the elements catalog. "
                "It is just inserted before the executable "
                "(may define additional environment variables or a wrapper that takes "
                "all arguments, see catalo/wscript)",
                "",
            )
        )

    self.parser.get_usage = _usage
    self.load("use_config")
    self.load("gnu_dirs")
    group = self.get_option_group("Installation prefix")

    descr = group.get_description() or ""

    group.add_option(
        "--prefix",
        dest="prefix",
        default=None,
        help="installation prefix [default: %r]" % default_prefix,
    )


def configure(self):
    self.load("ifort", tooldir="config")

    self.add_os_flags("FC")
    self.add_os_flags("CC")
    self.add_os_flags("CXX")
    self.add_os_flags("CFLAGS")
    self.add_os_flags("CXXFLAGS")
    self.add_os_flags("FCFLAGS")
    self.add_os_flags("LINKFLAGS")
    self.add_os_flags("DEFINES")
    self.add_os_flags("WAFBUILD_ENV")
    self.add_os_flags("CFLAGS_ASTER_DEBUG")
    self.add_os_flags("CXXFLAGS_ASTER_DEBUG")
    self.add_os_flags("FCFLAGS_ASTER_DEBUG")

    # bib* configure functions may add options required by prerequisites
    self.recurse("bibfor")
    self.recurse("bibcxx")
    self.recurse("bibc")

    self.recurse("pyx")


def build(self):
    self.recurse("bibfor")
    self.recurse("pyx")
    self.recurse("bibcxx")
    self.recurse("bibc")
