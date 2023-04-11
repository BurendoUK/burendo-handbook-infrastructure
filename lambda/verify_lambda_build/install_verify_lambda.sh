#!/bin/bash
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
pip3 install -r requirements.txt -t .
