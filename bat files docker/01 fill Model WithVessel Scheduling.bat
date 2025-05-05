echo off

rem This .bat file will copy the AIMMS project VesselScheduling to the docker sub folder "model"
rem assuming:
rem 1. Current directory is the folder in which this .bat file is stored.
rem 2. AIMMS project is in ..\..\AimmsProject

cd /d "~/dp0"
set VS_DOCK=%CD%
cd ..
set VS_ROOT=%CD%
set VS_PROJECT=%VS_ROOT%\AIMMSProject
echo Start time: %time%

cd %VS_ROOT%\aimms-eo

rem clean out completely old app in aimms-eo clone.
rmdir model /s /q
mkdir model

rem copy contents of AIMMSProject 
xcopy  "%VS_PROJECT%\libs\*.*"                model\libs        /E /I /Q /S /Y
xcopy  "%VS_PROJECT%\MainProject\*.*"         model\MainProject /E /I /Q /S /Y
xcopy  "%VS_PROJECT%\Mappings\*.*"            model\Mappings    /E /I /Q /S /Y
xcopy  "%VS_PROJECT%\VesselScheduling.aimms"  model                         /Y
xcopy  "%VS_PROJECT%\aimmscmdrun.sh"          model                         /Y
xcopy  "%VS_PROJECT%\LoggerConfig.xml"        model                         /Y

cd  %VS_DOCK%

pause
