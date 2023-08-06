==============
Use Flag Guide
==============

Use flags can be used to control optional dependencies and optional
configurations which a user may want to choose between.

Use flags should be declared in IUSE and described using the ``use`` top
level field in the mod’s ``metadata.yaml``.

E.g.

Build File

.. code:: python

   ...
   class Package(Pybuild1):
       IUSE = "foo bar"
       RDEPEND = """
           foo? ( !!cat/bar cat/foo )
           bar? ( !!cat/foo cat/bar )
       """
       REQUIRED_USE = "?? ( foo bar )"
   ...

metadata.yaml

.. code:: yaml

   use:
       foo: description of foo
       bar: description of bar

Use flags can be used in use-conditional expressions, that is, either
``flag?`` or ``!flag?``, followed by brackets to indicate the scope of
the conditional. RDEPEND and SRC_URI both support including
use-conditional expressions.

Use flags can also be used in the REQUIRED_USE field. `See the relevant
section of the Pybuild Format
page <https://portmod.gitlab.io/portmod/pybuild.html#pybuild.Pybuild1.REQUIRED_USE>`__
for details.

In the above example, we declare flags ``foo`` and ``bar``. From
``RDEPEND`` we see that if the user enables flag ``foo``, the mod will
pull in ``cat/foo`` as a dependency, and block ``cat/bar`` from being
installed. On the other hand, if the user enables ``bar``, the reverse
will happen. We then declare in ``REQUIRED_USE``, that at most one of
``foo`` and ``bar`` can be set at once (``??`` allows zero or one of the
flags in the set to be enabled). You might see a configuration like this
for a mod that has two mutually exclusive optional dependencies.

Note that the `InstallDir
object <https://portmod.gitlab.io/portmod/pybuild.html#pybuild.InstallDir>`__
as well as the File object, also have REQUIRED_USE fields. In their
cases, the InstallDir, or File will only be included if REQUIRED_USE is
satisfied. You could, for example, disable an InstallDir when a use flag
is not enabled by including that use flag in its ``REQUIRED_USE`` field.

Global and Local Use Flags
--------------------------

Global use flags are described in the ``/profiles/use.yaml`` file and
should not be included in a mod’s specific ``metadata.yaml`` file. They
do however need to be included in IUSE. If a use flag is to be made
global, it should be used by multiple mods for more or less the same
purpose.

All use flags that are not declared in ``/profiles/use.yaml``, and are
not use expand flags (see below), are considered to be local use flags.

Use Expand variables
--------------------

There are a certain class of automatically generated use flags set by
the user’s global configuration. For example, ``texture_size_`` prefixed
flags are automatically set based on a mod’s ``TEXTURE_SIZES`` field and
the user’s ``TEXTURE_SIZE`` variable in portmod.cfg. These flags should
not be listed in ``IUSE``, and they are automatically added to
``IUSE_EFFECTIVE`` (used internally). They can, however, be used in
use-conditionals and ``REQUIRED_USE`` fields just like other use flags.

You can declare new use expand groups by adding the prefix to the
``USE_EXPAND`` variable in the appropriate profile. Supported flags
should then be described in ``/profiles/desc/{use}.yaml`` (where
``{use}`` is the lowercased use flag group name).

E.g. in ``/profiles/base/defaults.conf`` (note that this path varies
depending on the profile setup):

.. code:: python

   USE_EXPAND = "SCREEN_ASPECT"

in ``/profiles/desc/screen_aspect.yaml``:

.. code:: yaml

   4x3: Use 4x3 screen aspect ratio
   16x9: Use 16x9 screen aspect ratio
   16x10: Use 16x10 screen aspect ratio

This produces the flags ``screen_aspect_4x3``, ``screen_aspect_16x9``
and ``screen_aspect_16x10``, which can be enabled by the user declaring
something such as the following in their config file:

.. code:: python

   SCREEN_ASPECT = "16x9"

External Resources
------------------

https://devmanual.gentoo.org/general-concepts/use-flags/index.html
