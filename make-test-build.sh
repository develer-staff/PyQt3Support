#!/bin/bash

PYQT=PyQt3Support-PyQt4.4.4-gpl-r5-pre

mkdir build
pushd $PYQT
PYTHONPATH=../build python configure.py -c -j3 -b ../build/ -d ../build/ -p ../build/ -n ../build/ -e QtGui -e Qt3Support --confirm-license && make clean && make && make install
popd

PYTHONPATH=build python -c "from PyQt4.Qt import *; print dir()"
