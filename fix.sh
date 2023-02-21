#!/bin/bash
if [[ $EUID > 0 ]]; then
  echo "This script requires sudo"
  exit 1
fi
sed -i "539s/kill()/kill('SIGINT')/" /opt/brickpiexplorer/app.js
printf '%s\n' 539m540 540-m539- w q | ed -s /opt/brickpiexplorer/app.js
