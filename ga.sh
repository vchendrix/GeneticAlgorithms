export PYTHONPATH=`pwd`/src
export TEST_RESULTS="`pwd`/results"
echo "Setting PYTHONPATH to $PYTHONPATH"

python src/ga/tools.py
