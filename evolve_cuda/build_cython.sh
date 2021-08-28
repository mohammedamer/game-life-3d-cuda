#!/bin/bash

make
python setup.py build_ext -i
cp *.so ../