#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2007 Develer S.r.l. (http://www.develer.com/)
#
# This file is part of PyQt3Support.
#
# PyQt3Support is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyQt3Support is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyQt3Support; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA#
#
# $Id:$
#
# Author: Matteo Bertini <naufraghi@develer.com>
#

"""
This script is a converter/merger that uses the sip files from the PyQt3
sources, modifies them and places them in a PyQt4 sources tree using the
Qt3Support module.

The actual form of the script is quite confused, that is because it is the
minimum affort to reach our needs, but we hope it is the same better than
nothing!
"""

import re
import glob
import fileinput
import shutil
import stat
import sys
import subprocess
import os, os.path

#pyqt3base = r"../PyQt-x11-gpl-3.17.3/"
#pyqt4base = r"../PyQt-x11-gpl-4.3.1/"
destbase = r"../PyQt3Support/"
destdir = destbase + "sip/Qt3Support/"

modulename = "Qt3Supportmod.sip"

q4classes = {# Class:          [(Anchor, method/enum/typedef),]
            "Gui/Application": [("static QStyle *setStyle(const QString &);",
                                 "virtual void setMainWidget")],
            "Gui/Label": [],
            "Gui/PushButton": [("virtual ~QPushButton();", "virtual void setOn"),
                               ("virtual ~QPushButton();", "bool isOn() const;"),
                               ],
            "Gui/Widget": [("QPalette::ColorRole backgroundRole() const;",
                            "const QColor &paletteBackgroundColor"),
                           ("QPalette::ColorRole backgroundRole() const;",
                            "virtual void setPaletteBackgroundColor"),
                           ("QPalette::ColorRole backgroundRole() const;",
                            "void setBackgroundMode(Qt::BackgroundMode,Qt::BackgroundMode = Qt::PaletteBackground);"),
                           ("QPalette::ColorRole backgroundRole() const;",
                            "virtual void setCaption"),
                           ("QPalette::ColorRole backgroundRole() const;",
                            "virtual void setEraseColor")],
            "Gui/GridLayout": [("void setColumnStretch(int column, int stretch);",
                                "virtual void setColStretch")],
            "Gui/LCDNumber": [],
            "Gui/Slider": [("virtual ~QSlider();",
                            "virtual void setTickmarks(TickPosition);"),
                           ("virtual ~QSlider();",
                            "TickPosition tickmarks() const;")],
            "Core/Timer": [],
            "Core/TextCodec": [("QByteArray fromUnicode(const QString &uc) const;",
                                "static const char *locale")],
            "OpenGL/GLWidget": [],
            "Core/Object": [("virtual ~QObject();",
                             "QObject *child"),],
            "Core/Namespace": [("typedef QFlags<Qt::TextInteractionFlag> TextInteractionFlags;",
                                "enum Dock"),
                               ("typedef QFlags<Qt::TextInteractionFlag> TextInteractionFlags;",
                                "typedef int ButtonState;"),
                               ("typedef QFlags<Qt::TextInteractionFlag> TextInteractionFlags;",
                                "enum BackgroundMode")],
            "Gui/Layout": [("QRect alignmentRect(const QRect &) const;",
                            "void deleteAllItems"),
                           ("virtual ~QLayout();",
                            "virtual void setAutoAdd")],
            "Gui/Event": [("virtual ~QWheelEvent();","ButtonState state"),
                          ("virtual ~QMouseEvent();","ButtonState state"),
                          ("virtual ~QKeyEvent();", "ButtonState state"),],
            "Gui/Dialog": [],
            "Gui/Menu": [("virtual ~QMenu();",
                          "int insertItem"),
                         ("virtual ~QMenu();",
                         "void setItemEnabled(int,bool);"),
                         ("virtual ~QMenu();",
                         "void setItemChecked(int,bool);"),
                         ("virtual ~QMenu();",
                         "virtual void setActiveItem(int);"),
                         ("virtual ~QMenu();",
                         "int indexOf(int) const;"),
                         ("virtual ~QMenu();",
                         "int insertTearOffHandle(int = -1,int = -1);"),
                         ("protected:",
                         "int itemHeight(int index);"),
                         ],
            "Gui/ToolButton": [("virtual ~QToolButton();",
                                "void setPopupDelay"),
                               ("virtual ~QToolButton();",
                                "void setPopup"),
                               ("void showMenu();",
                                "virtual void setTextLabel"),
                               ("void showMenu();",
                                "void setTextLabel"),
                               ("void showMenu();",
                                "virtual void setUsesTextLabel"),
                                ],
            "Gui/BoxLayout": [("QVBoxLayout();", "QVBoxLayout"),
                              ("QHBoxLayout();", "QHBoxLayout"),
                              ],
            "Gui/Pixmap": [("QPixmap();", "QPixmap(const QImage &);")],
            "Gui/MenuBar": [("virtual ~QMenuBar();", "int insertItem")],
            "Gui/LineEdit": [],
            "Gui/Palette": [("~QPalette();", "const QColorGroup")],
            "Gui/TabWidget": [],
            "Gui/TextEdit": [("~QTextEdit();", "QString text() const;")],
            "Gui/InputDialog": [("public:", "static QString getText")],
            "Gui/CheckBox": [],
            }

q3classes = """qt/VBox qt/HBox qt/Frame qt/Grid qt/Accel qt/PopupMenu qt/MenuData
               qt/DockWindow qt/DockArea qt/ListView qt/ScrollView
               qt/ColorGroup qt/Header qt/ListBox qt/StrList qttable/Table
               qt/MemArray qt/MainWindow qt/ToolBar qt/Action qt/SimpleRichText
               qt/StyleSheet qt/Mime qt/ComboBox qt/GroupBox qt/FileDialog
               qt/Url qt/WidgetStack qt/HGroupBox qt/VGroupBox qt/IconView
               qt/DragObject qt/Picture qt/ValueList qt/CString qt/ButtonGroup
               qt/VButtonGroup""".split()
assert len(q3classes) == len(set(q3classes)), (len(q3classes), len(set(q3classes)))

getCompatCode = re.compile("%If\ [\(\ ]*.*-.*Qt[^%]*%End\n*")

class SipFilters:
    @staticmethod
    def filter_convertQtVersion(line, c=None, filename=""):
        getmin = re.compile("\(Qt_[^\s]* -\)")
        getmax = re.compile("\(- Qt_[^\)]*\)")
        getrange = re.compile("\(Qt_[^\s]* - Qt_[^\)]*\)")
        line = getmin.sub("(Qt_4_2_0 -)", line)
        line = getmax.sub("(- Qt_4_1_3)", line)
        line = getrange.sub("(Qt_4_1_3 - Qt_4_2_0)", line)
        return line

    @staticmethod
    def filter_expandMacros(line, c=None, filename=""):
        features = """Qt_TRANSFORMATIONS Qt_ACTION Qt_DRAGANDDROP Qt_TABLE
                      Qt_TABLEVIEW Qt_FILEDIALOG Qt_ICONVIEW Qt_PICTURE""".split()
        line = line.replace(
            "%%Features%%",
            "%Feature " + "\n%Feature ".join(features)
            )
        toinclude = ["q3%s.sip" % qclass.split("/")[1].lower()
                     for qclass in q3classes if qclass not in ("qt/MenuData", "qt/ColorGroup")]
        line = line.replace(
            "%%Includes%%",
            "%Include " + "\n%Include ".join(toinclude)
            )
        return line

    @staticmethod
    def filter_typeChange(line, c=None, filename=""):
        getQ3PtrList = re.compile("Q3PtrList(\s*)<([^>]*)>(.*)")
        line = getQ3PtrList.sub("QList\\1<\\2*>\\3", line)
        return line

    @staticmethod
    def filter_extraDefines(line, c=None, filename=""):
        if "pointarray.sip" in filename:
            line = line.replace("class Q3PointArray",
                                """typedef qint32 QCOORD;\n\nclass Q3PointArray""")
        elif "listbox.sip" in filename:
            line = line.replace("Q3ListBoxItem *findItem(const QString &,",
                            """typedef uint ComparisonFlags;
	enum StringComparisonMode {
		CaseSensitive,
		BeginsWith,
		EndsWith,
		Contains,
		ExactMatch
		};
	Q3ListBoxItem *findItem(const QString &,""")
        elif "listview.sip" in filename:
            line = line.replace("Q3ListViewItem *findItem(const QString &,int,",
                            """typedef uint ComparisonFlags;
	enum StringComparisonMode {
		CaseSensitive,
		BeginsWith,
		EndsWith,
		Contains,
		ExactMatch
	};
	Q3ListViewItem *findItem(const QString &,int,""")
        elif "iconview.sip" in filename:
            line = line.replace("Q3IconViewItem *findItem(const QString &,",
                            """typedef uint ComparisonFlags;
	enum StringComparisonMode {
		CaseSensitive,
		BeginsWith,
		EndsWith,
		Contains,
		ExactMatch
	};
	Q3IconViewItem *findItem(const QString &,""")
        elif "mainwindow.sip" in filename:
            classgraph = SipMerge.readtext("q3classgraph.sip.in")
            line = line.replace("public:", classgraph+"\n\npublic:", 1)
        return line

    @staticmethod
    def filter_resolveProblematics(line, c=None, filename=""):
        line = line.replace("\tvirtual Q3DragObject *dragObject();",
                            "\t//virtual Q3DragObject *dragObject();")
        line = line.replace("QToolTipGroup *toolTipGroup() const;",
                            "//QToolTipGroup *toolTipGroup() const;")
        line = line.replace("QCustomMenuItem",
                            "QMenuItem")
        line = line.replace("QIconSet",
                            "QIcon")
        if "popupmenu.sip" in filename:
            line = line.replace("class Q3PopupMenu : QTableView, QMenuData",
                                "class Q3PopupMenu : QMenu")
            line = line.replace("class Q3PopupMenu : Q3Frame, QMenuData",
                                "class Q3PopupMenu : QMenu")
            line = line.replace("\tint itemHeight(",
                                "\t//int itemHeight(")
            line = line.replace("\tvoid drawItem(",
                                "\t//void drawItem(")
            line = line.replace("\tvoid drawContents(",
                                "\t//void drawContents(")
            line = line.replace("\tint idAt(const QPoint &) const;",
                                "\t//int idAt(const QPoint &) const;")
            line = line.replace("\tbool customWhatsThis()",
                                "\t//bool customWhatsThis()")
            line = line.replace("\tint itemAtPos(",
                                "\t//int itemAtPos(")
            line = line.replace("\tvoid updateItem(int);",
                                "\t//void updateItem(int);")
        elif "listview.sip" in filename:
            line = line.replace("class Q3ListView : Qt",
                                "class Q3ListView")
            line = line.replace("class Q3ListViewItem : Qt",
                                "class Q3ListViewItem")
        elif "listbox.sip" in filename:
            line = line.replace("\tvoid insertStrList(const Q3StrList *,int = -1);",
                                "\t//void insertStrList(const Q3StrList *,int = -1);")
        elif "table.sip" in filename:
            line = line.replace("class Q3TableItem : Qt",
                                "class Q3TableItem")
        elif "stylesheet.sip" in filename:
            line = line.replace("class Q3StyleSheetItem : Qt",
                                "class Q3StyleSheetItem")
        elif "mainwindow.sip" in filename or "toolbar.sip" in filename:
            line = line.replace("DockTop",
                                "Qt::DockTop")
        elif "action.sip" in filename:
            line = line.replace("qaction.h", "q3action.h")
            line = line.replace("QAction", "Q3Action")
        elif "colorgroup.sip" in filename:
            line = line.replace("QColorGroup(QColorGroup&);",
                                "QColorGroup(const QColorGroup&);\n\tQColorGroup(const QPalette&);")
        elif "combobox.sip" in filename:
            line = line.replace("qcombobox.h", "q3combobox.h")
            line = line.replace("QComboBox", "Q3ComboBox")
        elif "boxlayout.sip" in filename:
            line = line.replace("QBoxLayout(Direction,int = -1",
                                "QBoxLayout(Direction,int")
        elif "menu" in filename or "toolbutton.sip" in filename:
            line = line.replace("QPopupMenu",
                                "QMenu")
            line = line.replace("#include <Q3PopupMenu>\n", "")
        elif "groupbox" in filename:
            line = line.replace("class Q3GroupBox : Q3Frame",
                                "class Q3GroupBox : QGroupBox")
        elif "filedialog" in filename:
            line = line.replace("QButton", "QAbstractButton")
            if "Q3UrlOperator" in line:
                line = "//" +  line
        elif "url" in filename:
            if "operator!=" in line:
                line = "//" +  line
        elif "iconview" in filename:
            line = line.replace("class Q3IconViewItem : Qt",
                                "class Q3IconViewItem")
            line = line.replace("Q3Picture *picture()",
                                "QPicture *picture()")
        elif "cstring" in filename:
            if "QRegExp" in line:
                line = "//" + line
            if "//" not in line:
                line = line.replace("bool resize", "void resize")
                line = line.replace("bool truncate", "void truncate")
                line = line.replace("bool fill", "QByteArray & fill")
                line = line.replace("uint length", "int length")
                line = line.replace("int contains", "bool contains")
                line = line.replace(",bool = 1", "")
                line = line.replace("sipClass_QCString", "sipClass_Q3CString")
        elif "dragobject" in filename:
            if "setTarget" in line:
                line = "//" + line
            elif "decode" in line:
                line = line.replace("Q3CString", "QString")
        elif "picture" in filename:
            line = line.replace("Q3Picture : QPaintDevice", "Q3Picture : QPicture")
            line = line.replace("Q3Picture(int = -1)", "Q3Picture()")
        elif "valuelist" in filename:
            line = line.replace("for (uint i = 0;", "for (int i = 0;")
        elif "buttongroup" in filename:
            line = line.replace("QButton", "QAbstractButton")
            line = line.replace("qvbuttongroup.h", "q3buttongroup.h")
            if "moveFocus" in line or "buttonToggled" in line:
                line = "//" + line
        return line

    @staticmethod
    def filter_resetEnums(line, c=None, filename=""):
        getNamespacedUnum = re.compile("enum Qt::(.*)")
        line = getNamespacedUnum.sub("enum \\1", line)
        return line

    @staticmethod
    def filter_qt3to4Defines(line, c=None, filename=""):
        line = line.replace("//Added by qt3to4:", "//Added by qt3to4:\n%ModuleHeaderCode")
        if c != 0:
            line = line.replace("// This is the SIP","%End\n// This is the SIP")
        return line

class SipMerge:
    @staticmethod
    def readtext(filename):
        afile = open(filename)
        atext = afile.read()
        afile.close()
        return atext
    @staticmethod
    def writetext(filename, text):
        afile = open(filename, "w+")
        try:
            afile.write(text)
        except:
            print "Error writing", filename
        finally:
            afile.close()

    @staticmethod
    def filter_addNamespace(line, c=None, filename=""):
        for ns in "ArrowType Orientation".split():
            line = line.replace("Qt::%s" % ns, ns)
            line = line.replace(ns, "Qt::%s" % ns)
        return line

    @staticmethod
    def filter_qt3Constructor(line, c=0, filename=None):
        line = SipMerge.filter_addNamespace(line)
        line = line.replace("WFlags", "Qt::WindowFlags")
        line = line.replace("/TransferThis/ = 0", "/TransferThis/")
        if "object" not in filename:
            line = line.replace(",const char * = 0,", ",const char *,")
            line = line.replace(" const char * = 0,", " const char *,")
        if "boxlayout" in filename:
            line = line.replace("(Direction,int = -1", "(Direction,int")
        if "textedit" in filename:
            if "QString::null" in line:
                return ""
        if "toolbutton" in filename:
            line = line.replace("SIP_SLOT_CON(),QToolBar", "SIP_SLOT_CON(),QWidget")
        line = line.replace("QWidget * /TransferThis/,int = 1",
                            "QWidget * /TransferThis/,int")
        line = line.replace("QWidget * /TransferThis/,int = 0",
                            "QWidget * /TransferThis/,int")
        line = line.replace("QGridLayout(int = 1",
                            "QGridLayout(int")
        line = line.replace("Layout(int = -1",
                            "Layout(int")
        return line

    @staticmethod
    def merge_qt3supportConstructor(qt3filename, qt4filename, qclass=None):
        getConstructor = re.compile(r"^\s*(?:explicit)?\s*Q%s\([^;]*;" % qclass, re.MULTILINE)
        qt3text = getCompatCode.sub("", SipMerge.readtext(qt3filename))
        qt4text = SipMerge.readtext(qt4filename)
        q3constructors = []
        for q3 in getConstructor.findall(qt3text):
            if "SIP_PYLIST" in q3:
                continue
            if "char *" not in q3:
                continue
            q3 = SipMerge.filter_qt3Constructor(q3, filename=qt4filename)
            if q3.strip() not in [s.strip() for s in getConstructor.findall(qt4text)]+[""]:
                q3constructors.append("    "+q3.strip())
        if len(q3constructors) > 0:
            qt3stuff = [r"%If (Qt_QT3SUPPORT)"]
            for line in q3constructors:
                line = SipFilters.filter_resolveProblematics(line)
                if line not in qt3stuff:
                    qt3stuff.append(line)
            qt3stuff += [r"%End"]
            first_constructor = getConstructor.findall(qt4text)[0]
            qt4text = qt4text.replace(first_constructor,
                                      "\n".join([first_constructor]+qt3stuff))
        SipMerge.writetext(qt4filename, qt4text)

    @staticmethod
    def merge_qt3supportStuff(qt3filename, qt4filename, anchor, method):
        code = method
        for c in " *()&":
            code = code.replace(c, "\%s" % c)
        qt4text = SipMerge.readtext(qt4filename)
        if ";" not in method:
            getStuff = re.compile("^\s*%(code)s[\(\{\s]+[^;]*;" % {"code":code}, re.MULTILINE)
            qt3text = getCompatCode.sub("", SipMerge.readtext(qt3filename))
        else:
            getStuff = re.compile("%(code)s" % {"code":code})
            qt3text = method
        q3stuff = []
        for q3 in getStuff.findall(qt3text):
            if "SIP_PYLIST" in q3:
                continue
            if "menudata.sip" in qt3filename:
                if sum([i in q3 for i in "QCustomMenuItem QWidget QIconSet QPixmap".split()]):
                    continue
            if "layout.sip" in qt3filename:
                if "BoxLayout &" in q3:
                    continue
            if "namespace.sip" not in qt3filename:
                for addns in "ButtonState BackgroundMode".split():
                    getNoNS = re.compile("([^:\w])(%s)([\W])" % addns)
                    #FIXME: ci deve essere un modo più carino
                    last = None
                    while last != q3:
                        last = q3
                        q3 = getNoNS.sub("\\1Qt::\\2\\3", q3)
            res = []
            for q3line in q3.split("\n"):
                q3line = SipMerge.filter_qt3Constructor(q3line, filename=qt4filename)
                q3line = SipFilters.filter_convertQtVersion(q3line)
                q3line = SipFilters.filter_resolveProblematics(q3line, filename=qt4filename)
                q3line = SipFilters.filter_extraDefines(q3line, filename=qt4filename)
                res.append(q3line)
            q3 = "\n".join(res)
            if q3.strip() not in [s.strip() for s in q3stuff]:
                q3stuff.append("\t"+q3.strip())
        if not getStuff.findall(qt3text):
            print "!! '%s' not found!!" % code
        newlines = ["%If (Qt_QT3SUPPORT)"] + q3stuff + ["%End"]
        newtext = "\n".join([anchor]+newlines)
        qt4text = qt4text.replace(anchor, newtext, 1)
        if "menu" in qt4filename:
            qt4text = qt4text.replace("\nclass QMenuBar : QWidget",
                                """%If (Qt_QT3SUPPORT)
%Include ../Qt3Support/q3menudata.sip
%End

class QMenuBar : QWidget""")
        SipMerge.writetext(qt4filename, qt4text)

    @staticmethod
    def merge_cleanup2CompatibilityCode(qt3filename, qt4filename, anchor=None, method=None):
        qt3text = getCompatCode.sub("", SipMerge.readtext(qt3filename))
        SipMerge.writetext(qt4filename, qt3text)

    @staticmethod
    def add_features(qt4modulename):
        res = SipMerge.readtext(qt4modulename)
        res = res.replace("%Copying", "%Feature Qt_QT3SUPPORT\n\n%Copying")
        SipMerge.writetext(qt4modulename, res)

    @staticmethod
    def add_includes(qt4modulename):
        res = SipMerge.readtext(qt4modulename)
        res += "%If (Qt_QT3SUPPORT)\n%Include Qt3Support/q3colorgroup.sip\n%End\n"
        SipMerge.writetext(qt4modulename, res)

def process(filename, line, c, comment_lines={}):
    oldline = line
    for qtfilter in [f for f in dir(SipFilters) if "filter_" in f]:
        line = getattr(SipFilters, qtfilter)(line, c, filename)
    if "q3menudata.sip" in filename:
        comment_lines.setdefault(filename, False)
        if "class QMenuData" in line: # we need only QMenuItem
            comment_lines[filename] = True
    elif "q3mime.sip" in filename:
        if "class QMimeSource" in line: # we need only QMimeSource
            comment_lines[filename] = True
        elif "class Q3MimeSourceFactory" in line:
            comment_lines[filename] = False
    if comment_lines.get(filename, False):
        line = "// "+line
    if oldline != line and "-----" in filename:
        sys.stderr.write("Pre :"+oldline)
        sys.stderr.write("Post:"+line)
    if line:
        print line,

if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    from optparse import OptionParser
    usage = "usage: %prog pyqt3dir pyqt4dir" 
    parser = OptionParser(usage=usage)
    (opts, args) = parser.parse_args()

    # Prints out the effected classes
    if len(args) < 2:
        report = {'Qt4': [], 'Qt3': []}
        for qclass in q3classes:
            report['Qt3'].append("Q3%s" % qclass.split("/")[1])
        for qclass in q4classes:
            report['Qt4'].append("%s.Q%s" % tuple(qclass.split("/")))
        print "PyQt3 ported classes:\n%s" % ", ".join(report['Qt3'])
        print "PyQt4 qt3supported classes:\n%s" % ", ".join(report['Qt4'])
        sys.exit(0)
    elif len(args) == 2:
        pyqt3base = args[0]
        pyqt4base = args[1]
        for base in args:
            if not os.path.exists(base):
                parser.error("%s dir missing!" % base)
    else:
        parser.error("Provide only two arguments!")

    print "Mirroring the PyQt4 tree..."
    if not os.path.exists(destbase):
        shutil.copytree(pyqt4base, destbase)
    else:
        print "PyQt3Support tree is present, remove it manually if needed."
    shutil.rmtree(destdir, ignore_errors=True)
    os.makedirs(destdir)
    print "Moving qt3 sip files..."
    for qclassref in q3classes:
        qdir, qclass = qclassref.split("/")
        destfilename = destdir + "q3%s.sip" % qclass.lower()
        shutil.copy(pyqt3base + "sip/%s/q%s.sip" % (qdir, qclass.lower()), destfilename)
        os.chmod(destfilename, stat.S_IREAD + stat.S_IWRITE)
        SipMerge.merge_cleanup2CompatibilityCode(destfilename, destfilename)
    shutil.copy(modulename + ".in", destdir + modulename)
    files = glob.glob(destdir + "*.sip")
    print "Processing %d files..." % len(files)
    if os.path.exists("portinglog.txt"):
        os.remove("portinglog.txt")
    subprocess.call(["qt3to4", "-alwaysOverwrite", "-rulesFile", "q3porting.xml"] + files)
    for filename in files:
        sys.stderr.write(filename+"\n")
        for c, line in enumerate(fileinput.input([filename], inplace=1)):
            process(filename, line, c)
    print "Adding qt3support methods to qt4 sip files..."
    constructors = []
    methods = []
    mods = []
    for qclass in q4classes:
        orig3 = pyqt3base + "sip/qt/q%s.sip" % qclass.split("/")[1].lower()
        orig4 = pyqt4base + "sip/Qt%s/q%s.sip" % (qclass.split("/")[0], qclass.split("/")[1].lower())
        mod4 = destbase + "sip/Qt%s/Qt%smod.sip" % (qclass.split("/")[0], qclass.split("/")[0])
        dest = orig4.replace(pyqt4base, destbase)
        if qclass.split("/")[0] not in mods:
            print "--->", qclass.split("/")[0],
            for filename in glob.glob(pyqt4base + "sip/Qt%s/*.sip" % qclass.split("/")[0]):
                dest_filename = filename.replace(pyqt4base, destbase)
                dest_path = os.path.dirname(dest_filename)
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                shutil.copy2(filename, dest_filename)
                sys.stdout.write(".")
            print "!"
            mods.append(qclass.split("/")[0])
            print mod4
            if "Core" in mod4:
                SipMerge.add_features(mod4.replace(pyqt4base, destbase))
            elif "Gui" in mod4:
                SipMerge.add_includes(mod4.replace(pyqt4base, destbase))
        print "--->", qclass
        if "Layout" in qclass:
            orig3 = pyqt3base + "sip/qt/qlayout.sip"
        elif qclass == "OpenGL/GLWidget":
            orig3 = orig3.replace("qt/qglwidget.sip","qtgl/qgl.sip")
            orig4 = orig4.replace("qglwidget.sip","qgl.sip")
            dest = dest.replace("qglwidget.sip","qgl.sip")
        elif qclass in ["Gui/Menu", "Gui/MenuBar"]:
            orig3 = pyqt3base + "sip/qt/qmenudata.sip"
        shutil.copy(orig4, dest)
        if qclass not in ["Gui/Layout", "Gui/Pixmap"]:
            constructors.append((orig3, dest, qclass.split("/")[1]))
        if qclass in q4classes:
            for item in q4classes[qclass]:
                methods.append((orig3, dest, item[0], item[1]))
    [SipMerge.merge_qt3supportConstructor(*filedata) for filedata in constructors]
    [SipMerge.merge_qt3supportStuff(*filedata) for filedata in methods]
    print "Copying modified configure.py..."
    shutil.copy("configure.py", destbase + "configure.py")
