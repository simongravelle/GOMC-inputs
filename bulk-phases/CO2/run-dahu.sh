#!/bin/bash
#OAR -n GOMC-CO2
#OAR -l /nodes=1/cpu=1/core=8,walltime=24:00:00
#OAR --stdout log.out
#OAR --stderr log.err
#OAR --project tamtam

set -e

./launch-GOMC.sh

