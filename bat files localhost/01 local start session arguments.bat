echo on

rem Use AimmsCMD to start Vessel Scheduling with session arguments.

set AIMMS_VERSION=25.3.4.2-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

cd /d "%~dp0"
set VS_BAT=%CD%
cd ..
set VS_ROOT=%CD%
set VS_PROJECT=%VS_ROOT%\AIMMSProject
echo Start time: %time%

cd %VS_PROJECT%

%AIMMS_EXECUTABLE% --run-only pr_solveModelSessionArguments  "VesselScheduling.aimms" data\VS_7Vessel_20Cargo.xlsx data\VS_7Vessel_20Cargo_Results.xlsx

cd %VS_BAT%

echo Current time: %time%

pause
