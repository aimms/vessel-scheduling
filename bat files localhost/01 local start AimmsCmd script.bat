echo off

rem Use AimmsCMD to start Vessel Scheduling via an AimmsCmd script

set AIMMS_VERSION=25.3.4.2-x64-VS2022
set AIMMS_EXECUTABLE=%localappdata%\AIMMS\IFA\Aimms\%AIMMS_VERSION%\Bin\AimmsCMD.exe

cd /d "%~dp0"
set VS_BAT=%CD%
cd ..
set VS_ROOT=%CD%
set VS_PROJECT=%VS_ROOT%\AIMMSProject
echo Start time: %time%

cd %VS_PROJECT%

%AIMMS_EXECUTABLE% "VesselScheduling.aimms" < single-run.properties > log/single-run.log 2> log/single-run.err

cd %VS_BAT%

echo Current time: %time%

pause