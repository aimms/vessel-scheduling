echo on

rem copies the network license to the data folder in the aimms-eo clone.
rem assuming:
rem 1. current directory, is the directory in which this .bat file is stored.
rem 2. a network license file is in the folder licenses/network license.

pushd ..

rem clean out completely old licensing info in aimms-eo clone.
rmdir data /s /q

rem now copy the keyless license to its expected place.
mkdir data
mkdir data\Config
mkdir data\Licenses
copy  "licenses\keyless license\Config\licenses.cfg" "aimms-eo\data\Config\licenses.cfg"
xcopy "licenses\keyless license\Licenses\*.*"        "aimms-eo\data\Licenses\" /E /I /Q /S /Y

popd

pause