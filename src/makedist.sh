#!/bin/bash

VER=r2-pre
SDK=0.4-pre

PYQT4VER=4.3
PYQT3VER=3.17.3
PYQT4DIR=PyQt-x11-gpl-${PYQT4VER}
PYQT3DIR=PyQt-x11-gpl-${PYQT3VER}

echo "=========================================================="
echo "Preparing the distribution packages"
echo "=========================================================="

echo "----------------------------------------------------------"
echo "Downloading PyQt4 ad PyQt3 sources..."
echo "----------------------------------------------------------"

wget -c http://www.riverbankcomputing.com/Downloads/PyQt4/GPL/${PYQT4DIR}.tar.gz
[ ! -d ${PYQT4DIR} ] && tar xvf ${PYQT4DIR}.tar.gz

wget -c http://www.riverbankcomputing.com/Downloads/PyQt3/GPL/${PYQT3DIR}.tar.gz
[ ! -d ${PYQT3DIR} ] && tar xvf ${PYQT3DIR}.tar.gz


echo "----------------------------------------------------------"
echo "Building the full package..."
echo "----------------------------------------------------------"
FDESTDIR=PyQt3Support_PyQt${PYQT4VER}_GPL_${VER}

rm -rf $FDESTDIR

echo "Patching PyQt4 sources..."
src/q3sipconvert.py

echo "Copying PyQt3Support sources in $FDESTDIR"
mv PyQt3Support $FDESTDIR

cp README.TXT $FDESTDIR/PYQT3SUPPORT.TXT

echo "Building ${FDESTDIR}.tar.gz package..."
rm -rf ${FDESTDIR}.tar.gz
tar -cf ${FDESTDIR}.tar $FDESTDIR
gzip ${FDESTDIR}.tar



echo "----------------------------------------------------------"
echo "Building the addon package..."
echo "----------------------------------------------------------"
PDESTNAME=PyQt3Support_PyQt${PYQT4VER}_GPL_${VER}.patch

rm -f $PDESTNAME
cp README.TXT $PDESTNAME

echo "Diffing common files..."
pushd $PYQT4DIR
diff -urN ./sip ../$FDESTDIR/sip >> ../$PDESTNAME
diff -uN ./configure.py ../$FDESTDIR/configure.py >> ../$PDESTNAME
popd

echo "----------------------------------------------------------"
echo "Building the source package..."
echo "----------------------------------------------------------"

rm -rf /tmp/PyQt3Support_sdk_${SDK}
hg clone ./ /tmp/PyQt3Support_sdk_${SDK}
pushd /tmp
tar -cvvf PyQt3Support_sdk_${SDK}.tar PyQt3Support_sdk_${SDK}
gzip PyQt3Support_sdk_${SDK}.tar
popd
mv /tmp/PyQt3Support_sdk_${SDK}.tar.gz ./

