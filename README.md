# PyQt3Support - Python bindings for Qt3Support

### What is this?

PyQt3Support is an extension to
[PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/intro) that adds
bindings to [Qt's Qt3Support library](http://doc.trolltech.com/4.4/qt3support.html) for usage from the Python language.

This is very helpful to **migrate existing PyQt3 applications to PyQt4**.


### Why?

Porting from Qt3 to Qt4 can be tedious and bug-prone.

For C++ programmers, Trolltech/Nokia/Digia provides a library, called Qt3Support, that immensely helps. With Qt3Support, a C++ programmer basically only needs mechanical changes to your source code. The library is made of two different parts:

 * A new family of widgets (`Q3*`) with the *same* API of Qt3.
 * New member functions (or overloads) within standard Qt4 widgets.

For Python programmers, the situation is worse: PyQt4 does not bind
Qt3Support to Python. Developers of PyQt3 are forced to manually upgrade their code to PyQt4, class by class.

This package fills the gap. By providing a new module `PyQt4.Qt3Support`,
it **enables PyQt3 developers to access Trolltech's migration library**,
and thus upgrade their code much easily and faster, with almost only
mechanical changes. It's not a panacea of course: you probably still need minor manual adjustments and supervising, but it can still be of great help.


### Where?

PyQt3Support has been developed and tested under **both Windows** (2000, XP, Vista) **and Linux** (Ubuntu, Fedora).


### License

PyQt3Support follows whatever license you have for PyQt3 and PyQt4,
because its source code is machine-generated from PyQt3's and PyQt4's source code.

Thus, PyQt3Support can be **freely used under both the GPL or the
commercial license** offered by Qt/PyQt producers.

In case you are interested in developing PyQt3Support itself, you want to know that the script that generates PyQt3Support is released under the GPL license.


### Download

 * The (big) full package, containing a patched PyQt4 GPL tree with
 PyQt3Support. You can basically use this package instead of your PyQt4 pakage: [PyQt3Support-PyQt4.4.4-gpl-r4.tar.gz](http://www.develer.com/~naufraghi/PyQt3Support/PyQt3Support-PyQt4.4.4-gpl-r4.tar.gz)

 * The patch to be applied to a PyQt4 release to add PyQt3Support: [PyQt3Support-PyQt4.4.4-gpl-r4.patch](http://www.develer.com/~naufraghi/PyQt3Support/PyQt3Support-PyQt4.4.4-gpl-r4.patch)

Both these packages were produced running the automated script against PyQt4 4.4.4 and PyQt3 3.17.6.

If you have a commercial license and you are *very* paranoid, you probably want to run the script yourself against your own commercial copies of the packages. Otherwise, just grab the patch and apply it, since the result is exactly the same.

### Status

PyQt3Support is not complete: it binds about 30% of the Qt3Support, but don't be fooled by this figure: it's the part that is probably used most in existing programs (more common widgets, constructors, ecc.). A full list is available here: [[Status List]].

Moreover, since it is fully machine-generated, it is very easy to extend it to cover more classes and functions. See below as per how to contribute to the development.

### Deprecated warnings support

PyQt3Support now uses the new `/Deprecated/` SIP annotation.
The `Deprecated` annotation raises a [Python Warning](http://docs.python.org/lib/module-warnings.html) when Qt3Support is used, both plain Qt3 classes and !Qt3Support methods in Qt4 classes.

You can filter the warning flood with the standard python machinery:

    warnings.simplefilter('ignore', DeprecationWarning)

To use PyQt3Support you need at least a SIP snapshot containing the `/Deprecated/` patch or a release >= 4.7.8.

    2008/09/20 14:16:53  phil
    Added the /Deprecated/ class and function annotation (based on a patch from Lorenzo Berni).

### Support

If you have any question about PyQt3Support, mail us at <pyqt3support@develer.com>.

For professionals, commercial support is also available through our employer, [Develer](www.develer.com); for example: full PyQt3 to PyQt4 porting service. Mail us for pricing information.


### Authors

 * Matteo Bertini <naufraghi@develer.com>
 * Lorenzo Berni <duplo@develer.com> (PyQt 4.4.3 upgrade, / Deprecated / sip dupport)


### Development

If you want to send patches or further develop this module,
you can download the source code from GitHub and start reading [SOURCES.TXT](https://github.com/develersrl/PyQt3Support/blob/master/SOURCE.TXT).

If you need some help, feel free to mail us at <pyqt3support@develer.com>

### Thanks

 * Damon McCormick (code cleanup and fixes)
 * Matt Newell (fix wrong Q3Frame hierarchy)

