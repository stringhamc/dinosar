# Script to retrive ISCE source code and create a docker container
echo '\n***** Downloading ISCE from github... *****\n'
wget https://github.com/isce-framework/isce2/archive/v2.3.1.tar.gz
echo '\n***** Starting Docker multistage build *****\n'
docker build --rm -t dinosar/isce:v2.3.1_gpu . 
if [$1 == '-r']
then
       echo '\n***** Removing intermediate docker image *****\n'
       docker rmi $(docker images -q -f dangling=true)
fi
echo '\n***** ISCE is now a Docker image tagged "dinosar/isce:v2.3.1_gpu" *****\n'
