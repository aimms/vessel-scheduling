echo on

rem Builds a docker image with: 
rem 1. license info in sub-folder "data" of aimms-eo checkout
rem 2. AIMMS application in sub-folder "model" of aimms-eo checkout
rem 3. AIMMS 25.2.3.1 installation

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling

pushd %VS_ROOT%\aimms-eo

Rem The dockerfile is non-standard - copy from source.
copy "../changes aimms-eo/Dockerfile.WithLicenseAndModel" .

Rem actually build:
docker build -f Dockerfile.WithLicenseAndModel -t vesselscheduling:1.0.2.1 --build-arg AIMMS_VERSION_MAJOR=25.3 --build-arg AIMMS_VERSION_MINOR=1.0 .

popd

pause