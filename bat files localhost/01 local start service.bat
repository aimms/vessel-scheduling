echo on

rem Use AimmsCMD to start Vessel Scheduling as a service.

set AIMMS_VERSION=25.3.2.6-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_PROJECT=%VS_ROOT%\AIMMSProject

pushd %VS_PROJECT%

%AIMMS_EXECUTABLE% --run-only dex::api::RESTServiceHandler "VesselScheduling.aimms"  --dex::serviceTimeOut 30000

popd

echo Current time: %time%

pause