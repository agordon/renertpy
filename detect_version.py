#!/usr/bin/env python3
"""
CGI-Tools Python Package
Copyright (C) 2016-2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)


This module tries to auto-detect the version of the package,
and optionally write the package information into 'version.py'
file for automatic distribution packaging.

The version info is taken from the following sources (in order
of priority):
1. 'git describe' - if the current directroy is a git repostory
2. package/version.py - if the current directory is NOT a git repository
                        but the file exists (meaning, most likely, it was
                        extracted from a distribution tarball.

TODO:
3. Support non-git,no-version.py file (as is the result of downloading
   a bad auto-tarball from github's "release" page) - guess
   version based on the directory name.

Note about version format:

The module will convert the 'git describe' string into a PEP-440
compatible string.
 git-desctibe returns a string like:
   0.0.1-7-gab43-dirty
 where:
   0.0.1 - git tag
   7     - 7 commits after tag 0.0.1
   gab43 - current git commit SHA1 prefix is ab43
   dirty - the current working directory is dirty.

 It will be converted to:
   0.0.1+7.gab43.dirty
 where
   0.0.1 = Public version (see PEP440)
   +7... = private version info (see PEP440)


Typical usage in a setup.py file:

    from detect_version import detect_version
    setup(
       name = "my-package",
       version = detect_version("my_package"),
       ...)

The module will detect the version string from git,
and will write it to 'my_package/version.py' .

inside 'my_package/__init__.py', add the following code to load it:
    try:
        from .version import __version__
    except ImportError as e:
        __version__ = "0.0.0+BAD.VERSION"


NOTE:
Don't forget to add my_package/version.py to '.gitignore'.
DO NOT commit this file to the git repository.
"""

from subprocess import check_output,CalledProcessError
import os, re, sys


def update_fixed_version(filename, new_ver):
    """Update the version file with the given version"""
    try:
        f = open(filename,'w')
        f.write("## DO NOT EDIT - AUTO GENERATED by setup.py ##\n")
        f.write('__version__ = "%s"\n' % (str(new_ver)))
        f.close()
    except IOError as e:
        sys.exit("failed to write version file '%s': %s" % (filename, str(e)))


def get_git_version(filename):
    """get version from git repository (if exists).
    convert string to PEP-440 style, and update version file"""
    if not os.path.isdir(".git"):
        return None
    try:
        cmd = ['git','describe','--dirty','--abbrev=4']
        git_ver = check_output(cmd)
        git_ver = git_ver.decode('ascii','ignore')
        # convert git-describe string to PEP-440 string:
        git_ver = git_ver.strip().replace("-","+",1).replace("-",".")
        update_fixed_version(filename, git_ver)
        return git_ver
    except CalledProcessError as e:
        sys.exit("git-describe failed, exit code %d" % (e.returncode))
    except OSError as e:
        sys.exit("failed to execute git: %s" % (str(e)))



def get_fixed_version(filename):
    """Load the version string from 'version.py' file"""
    if not os.path.isfile(filename):
        return None

    try:
        l = open(filename).readlines()
    except IOError as e:
        sys.exit("failed to read '%s': %s" % (filename, str(e)))

    l = [x for x in l if re.search(r'^__version__ = "[^"]+"$',x)]
    if len(l)!=1:
        sys.exit("invalid version file '%s': found %d version strings" % \
                 (filename, len(l)))

    vre = re.search(r'^__version__ = "([^"]+)"$',l[0])
    if not vre:
        sys.exit("invalid version file '%s': failed to extract version" % \
                 (filename))

    return vre.group(1)



def detect_version(package_name):
    """Detect version string.
    from git first, then fallback to version.py"""
    pkg_dir = os.path.join(os.path.dirname(__file__),package_name)
    if not os.path.isdir(pkg_dir):
        raise RuntimeError("setup error: '%s' parameter is not a " \
                           "valid directory (%s)" % (package_name,pkg_dir))

    ver_py = os.path.join(pkg_dir,"version.py")

    git_ver = get_git_version(ver_py)
    if git_ver:
        return git_ver

    fixed_ver = get_fixed_version(ver_py)
    if fixed_ver:
        return fixed_ver

    return "0.0.0-VERSION.NOT.DETECTED"



if __name__ == "__main__":
    """
    If running as a stand-alone script, detect the version string
    and print it to STDOUT.
    """
    if len(sys.argv)<=1:
        sys.exit("usage: %s [pacakge directory]")
    v = detect_version(sys.argv[1])
    print(v)
