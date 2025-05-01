echo on

rem Setup bash for running on a Docker container with vessel-scheduling image.

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_INPUTS=%VS_ROOT%\inputs
set VS_OUTPUTS=%VS_ROOT%\outputs

docker run -it -v "%VS_INPUTS%:/inputs" -v "%VS_OUTPUTS%\outputs:/outputs" -w /model vesselscheduling:1.0.2.1 /bin/bash

rem sample command for bash: /usr/local/Aimms/Bin/AimmsCmd 

pause