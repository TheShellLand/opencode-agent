#!/bin/bash 
# copies run.sh to your local bin

docker="run.sh"
ro="run-readonly.sh"

cd "$(dirname $0)"/../
set -ex

chmod ugo+rx *.sh

if sudo touch /usr/bin/.TOUCH 2>/dev/null ; then 
	sudo rm /usr/bin/.TOUCH

	sudo cp $docker /usr/bin/opencode-docker
	sudo cp $docker /usr/bin/oc-d
	sudo cp $ro /usr/bin/oc-ro
fi

if sudo touch /usr/local/bin/.TOUCH 2>/dev/null ; then
	sudo rm /usr/local/bin/.TOUCH

	sudo cp $docker /usr/local/bin/opencode-docker
	sudo cp $docker /usr/local/bin/oc-d
	sudo cp $ro /usr/local/bin/oc-ro
fi


