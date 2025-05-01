echo on

Rem look in docker for name running container!

set CONTAINER_ID=nervous_northcutt

rem docker start %CONTAINER_ID%
docker start %CONTAINER_ID%
docker exec -it %CONTAINER_ID% /bin/bash
rem docker debug %CONTAINER_ID%

rem docker run -i laughing_leakey bash


pause