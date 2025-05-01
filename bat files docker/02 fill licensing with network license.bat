echo on

rem copies the network license to the data folder in the aimms-eo clone.
rem assuming:
rem 1. current directory, is the directory in which this .bat file is stored.
rem 2. a network license file is in the folder licenses/network license.

set VS_ROOT=C:\u\s\examples\application-examples\vessel-scheduling
set VS_LICENSES=%VS_ROOT%\licenses\

pushd %VS_ROOT%\aimms-eo

rem ensure clean data folder.
rmdir data /s /q
mkdir data
mkdir data\Config
mkdir data\Licenses


rem now copy the network license to its expected place.
copy "%VS_LICENSES%\network license\licenses.cfg" "data\Config\licenses.cfg"

popd

pause