echo on

rem Use AimmsCMD to start Vessel Scheduling as a service.

set AIMMS_VERSION=25.3.4.2-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

cd /d "~/dp0"
set VS_BAT=%CD%
cd ..
set VS_ROOT=%CD%
set VS_PROJECT=%VS_ROOT%\AIMMSProject
echo Start time: %time%

cd AIMMSProject

%AIMMS_EXECUTABLE% --run-only dex::api::RESTServiceHandler "VesselScheduling.aimms"  

rem --dex::serviceTimeOut 30000

cd %VS_BAT%

echo Current time: %time%

pause