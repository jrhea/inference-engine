#!/bin/bash

name="$1"

if [ "$name" == "wind" ]; then
  export MODEL_FILE="models/$name/deploy.prototxt"
  export PRETRAINED_FILE="models/$name/snapshot_iter_4860.caffemodel"
  export LABELS_FILE="models/$name/labels.txt"
elif [ "$name" == "fire" ]; then
  export MODEL_FILE="models/$name/deploy.prototxt"
  export PRETRAINED_FILE="models/$name/snapshot_iter_6540.caffemodel"
  export LABELS_FILE="models/$name/labels.txt"
fi
mkdir -p /tmp/foo

inputpipe=./tmp/$name-input
outputpipe=./tmp/$name-output
#delete the pipe on exit
trap "rm -f $inputpipe; rm -f $outputpipe; pgrep inference |xargs kill; umount ./tmp" EXIT
rm $inputpipe $outputpipe
if [[ ! -p $inputpipe ]]; then
	# create named pipes
	mkfifo $inputpipe
	mkfifo $outputpipe
	# keep pipe open so model stays loaded
	tail -f > $inputpipe &
	# force model to load with a dummy input
	#ls tests/$name/*.png | tr ' ' '\n' | xargs cat | base64 >$inputpipe &
	image=$(ls tests/$name/*.png | tr ' ' '\n' | head -n 1 | xargs cat | base64 | tr -d '\n')
	#image=$(cat tests/wind/havey_damage_tl_1.png | base64 | tr -d '\n')
        printf "$image\\n" >$inputpipe &
	cat $outputpipe &
fi
# coommand to start the docker container, initialize model, and wait for input
DOCKER_CMD="docker run --name $name --runtime=nvidia --rm --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -it -v $(pwd):/workspace -v $(pwd)/tmp:/workspace/tmp nvcr.io/nvidia/caffe:17.10 bash -c \"python src/inference.py $MODEL_FILE $PRETRAINED_FILE $LABELS_FILE <$inputpipe \""
eval $DOCKER_CMD >$outputpipe
