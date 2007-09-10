#!/bin/bash

VER=0.3
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
tar xvf ${PYQT4DIR}.tar.gz

wget -c http://www.riverbankcomputing.com/Downloads/PyQt3/GPL/${PYQT3DIR}.tar.gz
tar xvf ${PYQT3DIR}.tar.gz


echo "----------------------------------------------------------"
echo "Building the full package..."
echo "----------------------------------------------------------"
FDESTDIR=PyQt3Support${PYQT4VER}_PyQt${PYQT3VER}_full${VER}

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
ADESTDIR=PyQt3Support${PYQT4VER}_PyQt${PYQT3VER}_addon${VER}

rm -rf $ADESTDIR
mkdir $ADESTDIR
mkdir $ADESTDIR/sip

echo "Copying Qt3Support sip files..."
cp -r $FDESTDIR/sip/Qt3Support $ADESTDIR/sip

cp README.TXT $ADESTDIR

echo "Diffing common files..."
cd $PYQT4DIR
diff -urN -x Qt3Support ./sip ../$FDESTDIR/sip > ../$ADESTDIR/qt3support.patch
diff -uN ./configure.py ../$FDESTDIR/configure.py >> ../$ADESTDIR/qt3support.patch
cd ..

echo "Building ${ADESTDIR}.tar.gz package..."
rm -rf ${ADESTDIR}.tar.gz
tar -cf ${ADESTDIR}.tar $ADESTDIR
gzip ${ADESTDIR}.tar

