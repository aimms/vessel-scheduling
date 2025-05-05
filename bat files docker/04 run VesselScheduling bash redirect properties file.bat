echo on

rem run vessel-scheduling by redirecting the AimmsCmd command file /inputs/single-run.properties as input to AimmsCmd in a docker container.

cd /d "%~dp0"
set VS_DOCK=%CD%
cd ..
set VS_ROOT=%CD%

set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs

docker run -i -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%:/outputs" -w /model vesselscheduling:1.0.2.1 /bin/bash -c "/usr/local/Aimms/Bin/AimmsCmd VesselScheduling.aimms </inputs/single-run.properties >/outputs/single-run.log 2>/outputs/single-run.err"

pause