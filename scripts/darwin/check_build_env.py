#!/usr/bin/env python

"""
Test whether current python meets requirements to build Cura.
"""

if __name__ == '__main__':

    import sys
    import distutils.sysconfig as c
    from commands import getoutput

    # non-system build
    framework = "/System/Library/Frameworks/Python.framework/"
    assert not sys.prefix.startswith(framework), 'Non-system build required.'

    # framework-based
    assert len(c.get_config_var('PYTHONFRAMEWORK')) > 0, 'Framework build required.'

    # should include both i386 and x86_64. E.g:
    # "Architectures in the fat # file: /usr/local/bin/python are: i386 x86_64"
    info = getoutput("lipo -info `which python`")
    arches = set(info.split(': ')[-1].split())
    req = {'i386', 'x86_64'}
    assert req <= arches, 'Universal build required - %s missing from python architectures.' % ', '.join(req - arches)

    # deployment target set to 10.6:
    info = getoutput('otool -l `which python`')
    assert "cmd LC_VERSION_MIN_MACOSX ... version 10.6" in info
