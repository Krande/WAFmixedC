REM you need to call "build_env.bat" first

REM fortran
ifx -fpp /MD /nologo /nogen-interfaces /fpe:0 /traceback /real-size:64 /double-size:64 /4R8 /4I8 /integer-size:64 /debug:full /Od /Qopenmp  /I.\\bibfor\\include /c /o build\\fortran_code.F90.1.o .\\bibfor\\fortran_code.F90

REM c++
clang-cl /nologo /std:c++17 /FS /EHsc /EHc /permissive- /Zi /Od /I.\\bibcxx /I.\\bibc\\include .\\bibcxx\\cpp_code.cpp /FC /c /Fo.\\build\\cpp_code.cxx.2.o

REM c
clang-cl /FS /MD /nologo /Zi /Od /I.\\bibcxx /I.\\bibc\\include .\\bibc\\c_wrapper.c /FC /c /Fo.\\build\\c_wrapper.c.1.o

REM create shared libraries first of each project
REM fortran


REM linking
link /nologo /out:build\\main.exe build\\fortran_code.F90.1.o build\\cpp_code.cxx.2.o build\\c_wrapper.c.1.o
