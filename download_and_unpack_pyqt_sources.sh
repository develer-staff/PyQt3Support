#!/bin/bash

PyQt4=PyQt-x11-gpl-4.3.tar.gz
PyQt3=PyQt-x11-gpl-3.17.3.tar.gz

wget -c http://www.riverbankcomputing.com/Downloads/PyQt4/GPL/$PyQt4
tar xvf $PyQt4

wget -c http://www.riverbankcomputing.com/Downloads/PyQt3/GPL/$PyQt3
tar xvf $PyQt3