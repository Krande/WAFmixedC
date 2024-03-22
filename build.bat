@echo off
setlocal

set USE_LOG=0
set CLICOLOR_FORCE=1

call build_env.bat

rem if not exist CC
if not exist "%CC%" (
  echo "Setting compiler env vars"
  set "CC=clang-cl.exe"
  set "CXX=clang-cl.exe"
  set "FC=ifx.exe"
)

set FCFLAGS=%FCFLAGS% -fpp

where python
where cl
where ifort

SET PARENT_DIR=%~dp0
SET PARENT_DIR=%PARENT_DIR:\=/%

set LDFLAGS=%LDFLAGS% /LIBPATH:%LIB_PATH_ROOT%/lib

REM /MD link with MSVCRT.lib. /FS allow for multithreaded c compiler calls to vc140.pdb (for cl.exe only)
set CFLAGS=%CFLAGS% /MD /FS

set INCLUDES_BIBC=%PREF_ROOT%/include

waf distclean

REM Install for standard sequential
waf configure ^
  --use-config-dir=%PARENT_DIR%/config/ ^
  --prefix=%LIBRARY_PREFIX% ^

REM if USE_LOG is set, then log the output to a file
if %USE_LOG%==1 (
    REM set a datetime variable down to the minute
    @call conda_datetime.bat
    waf build_debug -v > build_debug_%datetimeString%.log 2>&1
    waf install_debug -v > install_debug_%datetimeString%.log 2>&1
) else (
    waf build_debug -v
    waf install_debug -v
)

endlocal