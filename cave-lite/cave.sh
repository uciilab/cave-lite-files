#!/bin/bash
#!/usr/bin/env python3

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

extract() {
    printf 'Available files:\n'
    ls *.pcap
    read -rep $'\nType pcap file from list: ' fileName
    
    tshark -r $fileName --disable-protocol wsmp -Tfields -Eseparator=, -e data.data > pcapOutput.txt
}

processing() {
    extract # uncomment if different SPAT file will be used
    python3 $directory/tscScript.py &
    python3 $directory/trafficSignal.py &
}

trap hupexit HUP
trap intexit INT

processing

wait