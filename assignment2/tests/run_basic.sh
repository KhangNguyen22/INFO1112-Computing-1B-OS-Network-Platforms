#!/bin/bash

cd ../

python3 client.py < tests/temp.in
# python3 -m trace --trace client.py < tests/temp.in