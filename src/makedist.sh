#!/bin/bash

VER=r4-pre
SDKVER=0.6-pre
PYQT4VER=4.4.4
PYQT3VER=3.17.5
SIPVER=4.7.8

DIST=glp
#DIST=commercial

if [ "$DIST" = "gpl" ]; then
  DOWNLOADIR=http://www.riverbankcomputing.co.uk/static/Downloads
  PYQT4DIR=PyQt-x11-${DIST}-${PYQT4VER}
  PYQT3DIR=PyQt-x11-${DIST}-${PYQT3VER}
else
  DOWNLOADIR=http://download.yourself.it/
  PYQT4DIR=PyQt-win-${DIST}-${PYQT4VER}
  PYQT3DIR=PyQt-${DIST}-${PYQT3VER}
fi

SIPDIR=sip-${SIPVER}

cd $(dirname $0) && cd ..

echo "=========================================================="
echo "Preparing the distribution packages"
echo "=========================================================="

echo "----------------------------------------------------------"
echo "Downloading PyQt4, PyQt3 and sip sources..."
echo "----------------------------------------------------------"

wget -c ${DOWNLOADIR}/PyQt4/${PYQT4DIR}.tar.gz
[ ! -d ${PYQT4DIR} ] && tar zxf ${PYQT4DIR}.tar.gz

wget -c ${DOWNLOADIR}/PyQt3/${PYQT3DIR}.tar.gz
[ ! -d ${PYQT3DIR} ] && tar zxf ${PYQT3DIR}.tar.gz

wget -c ${DOWNLOADIR}/sip4/${SIPDIR}.tar.gz
[ ! -d ${SIPDIR} ] && tar zxf ${SIPDIR}.tar.gz

echo "----------------------------------------------------------"
echo "Building the full package..."
echo "----------------------------------------------------------"
FDESTDIR=PyQt3Support-PyQt${PYQT4VER}-${DIST}-${VER}

rm -rf $FDESTDIR

echo "Patching PyQt4 sources..."
src/q3sipconvert.py ${PYQT3DIR} ${PYQT4DIR}

echo "Copying PyQt3Support sources in $FDESTDIR"
mv PyQt3Support $FDESTDIR

cp README.TXT $FDESTDIR/PYQT3SUPPORT.TXT

echo "----------------------------------------------------------"
echo "Patching configure.py..."
echo "----------------------------------------------------------"
patch $FDESTDIR/configure.py -p0 <src/configure.diff

echo "Building ${FDESTDIR}.tar.gz package..."
rm -rf ${FDESTDIR}.tar.gz
tar -cf ${FDESTDIR}.tar $FDESTDIR
gzip ${FDESTDIR}.tar



echo "----------------------------------------------------------"
echo "Building the addon package..."
echo "----------------------------------------------------------"
PDESTNAME=${FDESTDIR}.patch

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
SDK=PyQt3Support_sdk_${SDKVER}

rm -rf /tmp/${SDK}
hg clone ./ /tmp/${SDK}
pushd /tmp
tar -cf ${SDK}.tar ${SDK}
gzip ${SDK}.tar
popd
mv /tmp/${SDK}.tar.gz ./

echo "----------------------------------------------------------"
echo "Done!"
echo "----------------------------------------------------------"

