#!/bin/bash

echo "Preparing the patch package"

PYQT4VER = 4.3
PYQT3VER = 3.17.3
PYQT4DIR = PyQt-x11-gpl-${PYQT4VER}
PYQT3DIR = PyQt-x11-gpl-${PYQT3VER}

DESTDIR = Qt3Support${PYQT4VER}_Qt${PYQT4VER}_patch

mkdir $DESTDIR
mkdir $DESTDIR/sip

cd PyQt3Support
cp -rv sip/Qt3Support ../$DESTDIR/sip
diff -urN -x Qt3Support ../PyQt-x11-gpl-4.3/sip ./sip > ../$DESTDIR/qt3support.patch
diff -urN ../PyQt-x11-gpl-4.3/configure.py ./configure.py > ../$DESTDIR/configure.patch

cd ..
tar -cvvf ${DESTDIR}.tar $DESTDIR
gzip ${DESTDIR}.tar