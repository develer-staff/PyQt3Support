#!/bin/bash

SIP=sip-4.7.9
PYQT=PyQt3Support-PyQt4.4.4-gpl-r5-pre

mkdir build
cd $SIP
python configure.py -b ../build -d ../build -e ../build -v ../build && make clean && make && make install
cd ..
cd $PYQT
PYTHONPATH=../build python configure.py -c -j3 -b ../build/ -d ../build/ -p ../build/ -n ../build/ -e QtGui -e Qt3Support --confirm-license && make clean && make && make install
cd ..

PYTHONPATH=build python -c "from PyQt4.Qt import *; print dir()"
