echo on

rem run vessel-scheduling by redirecting the AimmsCmd command file /inputs/single-run.properties as input to AimmsCmd in a docker container.

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs

docker run -i -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%:/outputs" -w /model vesselscheduling:1.0.2.1 /bin/bash -c "/usr/local/Aimms/Bin/AimmsCmd VesselScheduling.aimms < /inputs/single-run.properties > /outputs/single-run.log 2> /outputs/single-run.err"

rem Note that /bin/bash is needed to redirect input/output within the execution in the container.

pause