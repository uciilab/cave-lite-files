#!/bin/bash
directory=$(pwd)

intexit() {
    # Kill all subprocesses (all processes in the current process group)
    kill -HUP -$$
}

hupexit() {
    # HUP'd (probably by intexit)
    echo
    echo "Interrupted"
    exit
}

processing() {
    read -p "Enter distance to signal in feet: " distance
    python3 $directory/msgRecv.py $distance &
    python3 $directory/bsmGenerator.py &
    python3 $directory/bsmSend.py &
}

trap hupexit HUP
trap intexit INT

processing

wait
