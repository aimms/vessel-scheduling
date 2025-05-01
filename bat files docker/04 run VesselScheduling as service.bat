echo on

rem Start the VesselScheduling app with a REST API Service, handling tasks to solve the VesselScheduling problem.

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs

rem --rm
rem  --dex::serviceTimeOut 10000

docker run  -i -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%:/outputs"  -p 12003:12003 -w /model vesselscheduling:1.0.2.1 AimmsCmd --run-only dex::api::RESTServiceHandler "VesselScheduling.aimms" 

echo Current time: %time%

pause
