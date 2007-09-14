= PyQt3Support - Python bindings for Qt3Support =

== What is this? ==

PyQt3Support is an extension to
[http://www.riverbankcomputing.co.uk/pyqt/index.php PyQt4] that adds
'''bindings to [http://doc.trolltech.com/4.3/qt3support.html Qt's Qt3Support library]'''
for usage from the Python language.

This is very helpful to '''migrate existing !PyQt3 applications to !PyQt4'''.

== Why? ==

Porting from Qt3 to Qt4 can be tedious and bug-prone.

For C++ programmers, Trolltech provides a library, called !Qt3Support, that
immensely helps. With !Qt3Support, a C++ programmer basically only needs
mechanical changes to your source code. The library is made of two
different parts:

 * A new family of widgets (`Q3*`) with the '''same''' API of Qt3.
 * New member functions (or overloads) within standard Qt4 widgets.

For Python programmers, the situation is worse: !PyQt4 does not bind
!Qt3Support to Python. Developers of !PyQt3 are forced to manually upgrade
their code to !PyQt4, class by class.

This package fills the gap. By providing a new module `PyQt4.Qt3Support`,
it '''enables !PyQt3 developers to access Trolltech's migration library''',
and thus upgrade their code much easily and faster, with almost only
mechanical changes. It's not a panacea of course: you probably still need
minor manual adjustments and supervising, but it can still be of great help.

== Where? ==

!PyQt3Support has been developed and tested under '''both Windows''' (2000,
XP, Vista) '''and Linux''' (Ubuntu, Fedora).


== License ==

!Qt3Support follows whatever license you have for !PyQt3 and !PyQt4,
because its source code is machine-generated from !PyQt3's and !PyQt4's
source code.

Thus, !Qt3Support can be '''freely used under both the GPL or the
commercial license''' offered by Qt/!PyQt producers.

In case you are interested in developing !Qt3Support itself, you want to
know that the script that generates !Qt3Support is released under the GPL
license.

== Download ==

 * The (big) full package, containing a patched !PyQt4 GPL tree with
!PyQt3Support. You can basically use this package instead of your PyQt4
pakage.

[http://www.develer.com/~naufraghi/PyQt3Support/PyQt3Support_PyQt4.3_GPL_r1.tar.gz PyQt3Support_PyQt4.3_GPL_r1.tar.gz]

 * The patch to be applied to a !PyQt4 release to add !PyQt3Support.

[http://www.develer.com/~naufraghi/PyQt3Support/PyQt3Support_PyQt4.3_GPL_r1.patch PyQt3Support_PyQt4.3_GPL_r1.patch]

Both these packages were produced running the automated script against
!PyQt4 4.3 and !PyQt3 3.17.3.

If you have a commercial license and you are ''very'' anal, you probably
want to run the script yourself against your own commercial copies of the
packages. Otherwise, just grab the patch and apply it, since the result is
exactly the same.

== Status ==

!PyQt3Support is not complete: it binds about 30% of the !PyQt3Support, but
don't be fooled by this figure: it's the part that is probably used most in
existing programs (more common widgets, constructors, ecc.).

Moreover, since it is fully machine-generated, it is very easy to extend it
to cover more classes and functions. See below as per how to contribute to
the development.

== Support ==

For support queries, mail us at pyqt3support@develer.com.

Commercial support is also available through our employer
([http://www.develer.com Develer Srl]); for example: full !PyQt3 to !PyQt4
porting service. Mail us for pricing information.


== Author ==

Matteo Bertini <naufraghi-nospam@develer.com>


== Development ==

If you want to send patches or further develop this module,
you can download the script package (a mercurial working copy)
and start reading `SOURCES.TXT`:

[http://www.develer.com/~naufraghi/PyQt3Support/PyQt3Support_sdk_0.3.tar.gz PyQt3Support_sdk_0.3.tar.gz]

If you need some help, feel free to mail us at <pyqt3support@develer.com>

