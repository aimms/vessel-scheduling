echo on

rem Use AimmsCMD to start Vessel Scheduling with session arguments.

set AIMMS_VERSION=25.3.2.6-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

pushd ..\AIMMSProject

%AIMMS_EXECUTABLE% --run-only pr_solveModelSessionArguments  "VesselScheduling.aimms" data\VS_7Vessel_20Cargo.xlsx data\VS_7Vessel_20Cargo_Results.xlsx

popd

echo Current time: %time%

pause
