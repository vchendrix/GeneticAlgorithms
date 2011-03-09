#!/bin/bash

export PYTHONPATH="`pwd`/src"
export TEST_RESULTS="`pwd`/results"
cd test
python -m unittest discover -p '*test.py'
