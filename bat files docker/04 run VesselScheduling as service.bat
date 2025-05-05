echo on

rem Start the VesselScheduling app with a REST API Service, handling tasks to solve the VesselScheduling problem.

cd /d "%~dp0"
set VS_DOCK=%CD%
cd ..
set VS_ROOT=%CD%

set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs

del  %VS_OUTPUTS%\aimms-log.txt

docker run --rm -i -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%:/outputs"  -p 12003:12003 -w /model vesselscheduling:1.0.2.1 AimmsCmd --run-only dex::api::RESTServiceHandler "VesselScheduling.aimms" 

cd %VS_DOCK%

pause
