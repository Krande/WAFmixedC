REM you need to call "build_env.bat" first

REM fortran
ifx -fpp /MD /nologo /nogen-interfaces /fpe:0 /traceback /real-size:64 /double-size:64 /4R8 /4I8 /integer-size:64 /debug:full /Od /Qopenmp  /I.\\bibfor\\include /c /o build\\fortran_code.F90.1.o .\\bibfor\\fortran_code.F90

REM c++
clang-cl /nologo /std:c++17 /FS /EHsc /EHc /permissive- /Zi /Od /I.\\bibcxx /I.\\bibc\\include .\\bibcxx\\cpp_code.cpp /FC /c /Fo.\\build\\cpp_code.cxx.2.o

REM c
clang-cl /FS /MD /nologo /Zi /Od /I.\\bibcxx /I.\\bibc\\include .\\bibc\\c_wrapper.c /FC /c /Fo.\\build\\c_wrapper.c.1.o

REM create shared libraries first of each project
REM fortran

REM linking C (ie. create a .dll and .lib)
link /nologo /MANIFEST /subsystem:console "/IMPLIB:bibc\\bibc.lib" /DLL build\\c_wrapper.c.1.o /OUT:build\\bibc.dll /DEBUG

REM linking Fortran (ie. create a .dll and .lib)
link /nologo /MANIFEST /subsystem:console "/IMPLIB:bibfor\\bibfor.lib" /DLL build\\fortran_code.F90.1.o /OUT:build\\bibfor.dll /DEBUG

REM linking C++ (ie. create a .dll and .lib)
link /nologo /MANIFEST /subsystem:console "/IMPLIB:bibcxx\\bibcxx.lib" /DLL build\\cpp_code.cxx.2.o /OUT:build\\bibcxx.dll /DEBUG