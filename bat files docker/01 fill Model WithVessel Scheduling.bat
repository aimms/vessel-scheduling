echo on

rem This .bat file will copy the AIMMS project VesselScheduling to the docker sub folder "model"
rem assuming:
rem 1. Current directory is the folder in which this .bat file is stored.
rem 2. AIMMS project is in ..\..\AimmsProject

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_SOURCE=%VS_ROOT%\AIMMSProject\

pushd %VS_ROOT%\aimms-eo

rem clean out completely old app in aimms-eo clone.
rmdir model /s /q

mkdir model
xcopy  "%VS_SOURCE%\libs\*.*"                model\libs        /E /I /Q /S /Y
xcopy  "%VS_SOURCE%\MainProject\*.*"         model\MainProject /E /I /Q /S /Y
xcopy  "%VS_SOURCE%\Mappings\*.*"            model\Mappings    /E /I /Q /S /Y
xcopy  "%VS_SOURCE%\VesselScheduling.aimms"  model                         /Y
xcopy  "%VS_SOURCE%\aimmscmdrun.sh"          model                         /Y
xcopy  "%VS_SOURCE%\LoggerConfig.xml"        model                         /Y

popd

pause
