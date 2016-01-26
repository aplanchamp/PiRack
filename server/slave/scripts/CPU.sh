#!/bin/bash

TIMER=1

function usageCPU {
  read cpu user nice system reste < <(grep "^cpu " /proc/stat);
  echo "$user+$nice+$system" 
}

NB_CPU=$(grep "^processor" /proc/cpuinfo | wc -l)

  MESURE_1=$(usageCPU)
  sleep $TIMER
  MESURE_2=$(usageCPU)
  CPU_USAGE=$(echo "scale=2; ($MESURE_2-$MESURE_1)/($TIMER*$NB_CPU)")
  echo "$CPU_USAGE%"

