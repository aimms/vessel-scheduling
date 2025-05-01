echo on

rem Use AimmsCMD to start Vessel Scheduling via an AimmsCmd script

set AIMMS_VERSION=25.3.2.6-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_PROJECT=%VS_ROOT%\AIMMSProject

pushd %VS_PROJECT%

%AIMMS_EXECUTABLE% "VesselScheduling.aimms" < single-run.properties > log/single-run.log 2> log/single-run.err

popd

echo Current time: %time%

pause