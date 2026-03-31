#!/bin/bash

if [[ ! -d "./gexp-tracking" ]]; then
  git clone https://github.com/gianpena/gexp-tracking.git
  cd gexp-tracking
  cp ../.env .env
  pip install -r requirements.txt
else
  cd gexp-tracking
fi

python main.py