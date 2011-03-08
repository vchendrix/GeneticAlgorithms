#!/bin/bash

export PYTHONPATH="`pwd`/src:`pwd`/results:${PYTHONPATH}"
export TEST_RESULTS="`pwd`/results"
cd test
python -m unittest discover -p '*test.py'
