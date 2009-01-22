#!/bin/bash
mkdir build
cd sip-4.7.9
python configure.py -b ../build -d ../build -e ../build -v ../build
make && make install
cd ..
cd PyQt3Support-PyQt4.4.4-gpl-r5-pre
PYTHONPATH=../sip-4.7.9 python configure.py -c -j3 -g --confirm-license -b ../build -d ../build --no-sip-files -p ../build --no-qsci-api -e QtGui -e Qt3Support
make && make install
