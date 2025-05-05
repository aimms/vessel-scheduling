echo on

rem Script to execute a single procedure in an AIMMS app stored in a docker image.

cd /d "%~dp0"
set VS_DOCK=%CD%
cd ..
set VS_ROOT=%CD%

set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs 

del  %VS_OUTPUTS%\aimms-log.txt
del  %VS_OUTPUTS%\single-run.*
copy %VS_ROOT%\AIMMSProject\data\VS_70Vessel_100Cargo_results.xlsx %VS_INPUTS%
 

docker run --rm -i -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%:/outputs" -w /model vesselscheduling:1.0.2.1 AimmsCmd --run-only pr_solveModelSessionArguments "VesselScheduling.aimms" /inputs/VS_70Vessel_100Cargo.xlsx /outputs/VS_70Vessel_100Cargo_results.xlsx

pause