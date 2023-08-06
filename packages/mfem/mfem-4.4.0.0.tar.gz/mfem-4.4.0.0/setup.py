"""
  MFEM + PyMFEM (finite element method library)
"""
from sys import platform
import sys
import os
import urllib
import gzip
import site
import re
import shutil
import configparser
import itertools
import subprocess
from subprocess import DEVNULL

import multiprocessing

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.install import install as _install
from setuptools.command.install_egg_info import install_egg_info as _install_egg_info
from setuptools.command.install_lib import install_lib as _install_lib
from setuptools.command.install_scripts import install_scripts as _install_scripts
import setuptools.command.sdist

try:
    from setuptools._distutils.command.clean import clean as _clean
except ImportError:
    from distutils.command.clean import clean as _clean

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    haveWheel = True
except ImportError:
    haveWheel = False

# To use a consistent encoding
# from codecs import open

# constants
repo_releases = {
    "metis": "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz",
    "hypre": "https://github.com/hypre-space/hypre/archive/v2.24.0.tar.gz",
    "libceed": "https://github.com/CEED/libCEED/archive/refs/tags/v0.10.0.tar.gz",
    "gslib": "https://github.com/Nek5000/gslib/archive/refs/tags/v1.0.7.tar.gz"}

repos = {"mfem": "https://github.com/mfem/mfem.git",
         "libceed": "https://github.com/CEED/libCEED.git"}
repos_sha = {"mfem": "a1f6902ed72552f3e680d1489f1aa6ade2e0d3b2"}

rootdir = os.path.abspath(os.path.dirname(__file__))
extdir = os.path.join(rootdir, 'external')
if not os.path.exists(extdir):
    os.mkdir(os.path.join(rootdir, 'external'))

if platform == "linux" or platform == "linux2":
    dylibext = '.so'
elif platform == "darwin":
    # OS X
    dylibext = '.dylib'
elif platform == "win32":
    # Windows...
    assert False, "Windows is not supported yet. Contribution is welcome"


### global variables
is_configured = False
prefix = ''

verbose = -1
swig_only = False
skip_install = False
run_swig = False
clean_swig = False
build_mfem = True
mfem_branch = None
build_mfemp = False
build_metis = False
build_hypre = False
build_libceed = False
build_gslib = False
build_parallel = False
build_serial = False

ext_prefix = ''
mfems_prefix = ''
mfemp_prefix = ''
mfem_source = ''
metis_prefix = ''
hypre_prefix = ''

enable_cuda = False
enable_cuda_hypre = False
cuda_prefix = ''
cuda_arch = ''
enable_pumi = False
pumi_prefix = ''
enable_strumpack = False
strumpack_prefix = ''
enable_libceed = False
libceed_prefix = ''
libceed_only = False
enable_gslib = False
gslibs_prefix = ''
gslibp_prefix = ''
gslib_only = False

enable_suitesparse = False
suitesparse_prefix = 'usr/lib/x86_64-linux-gnu'

dry_run = -1
do_bdist_wheel = False

cc_command = 'cc' if os.getenv("CC") is None else os.getenv("CC")
cxx_command = 'c++' if os.getenv("CC") is None else os.getenv("CXX")
mpicc_command = 'mpicc' if os.getenv("MPICC") is None else os.getenv("MPICC")
mpicxx_command = 'mpic++' if os.getenv(
    "MPICXX") is None else os.getenv("MPICXX")
cxx11_flag = '-std=c++11' if os.getenv(
    "CXX11FLAG") is None else os.getenv("CXX11FLAG")

# meta data


def version():
    VERSIONFILE = os.path.join('mfem', '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))


def version():
    VERSIONFILE = os.path.join('mfem', '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))


def long_description():
    with open(os.path.join(rootdir, 'README.md'), encoding='utf-8') as f:
        return f.read()


def install_requires():
    fname = os.path.join(rootdir, 'requirements.txt')
    if not os.path.exists(fname):
        return []
    fid = open(fname)
    requirements = fid.read().split('\n')
    fid.close()
    return requirements

def read_mfem_tplflags(prefix):
    filename = os.path.join(prefix, 'share', 'mfem', 'config.mk')
    if not os.path.exists(filename):
        print("NOTE: " + filename + " does not exist.")
        print("returning empty string")
        return ""
    
    config = configparser.ConfigParser()
    with open(filename) as fp:
        config.read_file(itertools.chain(['[global]'], fp), source=filename)
    flags = dict(config.items('global'))['mfem_tplflags']
    return flags
    
keywords = """
scientific computing
finite element method
"""

platforms = """
Mac OS X
Linux
"""
metadata = {'name': 'mfem',
            'version': version(),
            'description': __doc__.strip(),
            'long_description': long_description(),
            'long_description_content_type': "text/markdown",
            'url': 'http://mfem.org',
            'download_url': 'https://github.com/mfem',
            'classifiers': ['Development Status :: 4 - Beta',
                            'Intended Audience :: Developers',
                            'Topic :: Scientific/Engineering :: Physics',
                            'License :: OSI Approved :: BSD License',
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Programming Language :: Python :: 3.9',
                            'Programming Language :: Python :: 3.10', ],
            'keywords': [k for k in keywords.split('\n') if k],
            'platforms': [p for p in platforms.split('\n') if p],
            'license': 'BSD-3',
            'author': 'MFEM developement team',
            'author_email': '',
            'maintainer': 'S. Shiraiwa',
            'maintainer_email': 'shiraiwa@princeton.edu', }

# utilities


def abspath(path):
    return os.path.abspath(os.path.expanduser(path))


'''
def install_prefix():
    """Return the installation directory, or None"""
    if '--user' in sys.argv:
        paths = (site.getusersitepackages(),)
    else:
        py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
        paths = (s % (py_version) for s in (
            sys.prefix + '/lib/python%s/dist-packages/',
            sys.prefix + '/lib/python%s/site-packages/',
            sys.prefix + '/local/lib/python%s/dist-packages/',
            sys.prefix + '/local/lib/python%s/site-packages/',
            '/Library/Python/%s/site-packages/',
        ))

    for path in paths:
        #if verbose:
        #    print("testing installation path", path)
        if os.path.exists(path):
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            if verbose:
                print("found this one", path)
            return path
    assert False, "no installation path found"
    return None
'''


def external_install_prefix(verbose=True):
    if '--user' in sys.argv:
        paths = (site.getusersitepackages(),)
    else:
        py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
        paths = (s % (py_version) for s in (
            sys.prefix + '/lib/python%s/dist-packages/',
            sys.prefix + '/lib/python%s/site-packages/',
            sys.prefix + '/local/lib/python%s/dist-packages/',
            sys.prefix + '/local/lib/python%s/site-packages/',
            '/Library/Python/%s/site-packages/',
        ))

    for path in paths:
        # if verbose:
        #    print("testing installation path", path)
        if os.path.exists(path):
            path = os.path.join(path, 'mfem', 'external')
            return path
    assert False, "no installation path found"
    return None


def find_command(name):
    from shutil import which
    return which(name)


def make_call(command, target=''):
    '''
    call command
    '''
    if dry_run or verbose:
        print("calling ... " + " ".join(command))
    if dry_run:
        return
    kwargs = {}
    if not verbose:
        kwargs['stdout'] = DEVNULL
        kwargs['stderr'] = DEVNULL
    try:
        subprocess.check_call(command, **kwargs)
    except subprocess.CalledProcessError:
        if target == '':
            target = " ".join(command)
        print("Failed when calling command: " + target)
        raise


def chdir(path):
    '''
    change directory
    '''
    pwd = os.getcwd()
    os.chdir(path)
    if verbose:
        print("Moving to a directory : " + path)
    return pwd


def remove_files(files):
    for f in files:
        if verbose:
            print("Removing : " + f)
        if dry_run:
            continue
        os.remove(f)


def make(target):
    '''
    make : add -j option automatically
    '''
    command = ['make', '-j', str(max((multiprocessing.cpu_count() - 1, 1)))]
    make_call(command, target=target)


def make_install(target, prefix=None):
    '''
    make install
    '''
    command = ['make', 'install']
    if prefix is not None:
        command.append('prefix='+prefix)
    make_call(command, target=target)


def download(xxx):
    '''
    download tar.gz from somewhere. xxx is name.
    url is given by repos above
    '''
    from urllib import request
    import tarfile

    if os.path.exists(os.path.join(extdir, xxx)):
        print("Download " + xxx + " skipped. Use clean --all-exts if needed")
        return
    url = repo_releases[xxx]
    print("Downloading :", url)

    ftpstream = request.urlopen(url)
    targz = tarfile.open(fileobj=ftpstream, mode="r|gz")
    targz.extractall(path=extdir)
    os.rename(os.path.join(extdir, targz.getnames()[0].split('/')[0]),
              os.path.join(extdir, xxx))


def gitclone(xxx, use_sha=False, branch='master'):
    cwd = os.getcwd()
    repo_xxx = os.path.join(extdir, xxx)
    if os.path.exists(repo_xxx):
        print("Deleting the existing " + xxx)
        shutil.rmtree(repo_xxx)

    os.chdir(extdir)
    command = ['git', 'clone', repos[xxx], xxx]
    make_call(command)

    if not os.path.exists(repo_xxx):
        print(repo_xxx + " does not exist. Check if git clone worked")
    os.chdir(repo_xxx)
    if use_sha:
        sha = repos_sha[xxx]
        command = ['git', 'checkout',  sha]
    else:
        command = ['git', 'checkout', branch]
    make_call(command)
    os.chdir(cwd)


def record_mfem_sha(mfem_source):
    pwd = chdir(mfem_source)
    command = ['git', 'rev-parse', 'HEAD']
    try:
        sha = subprocess.run(
            command, capture_output=True).stdout.decode().strip()
    except subprocess.CalledProcessError:
        print("subprocess failed to read sha...continuing w/o recording SHA")
        sha = None
    except BaseException:
        print("subprocess failed to read sha...continuing w/o recording SHA")
        sha = None

    chdir(pwd)

    sha_file = os.path.join('mfem', '__sha__.py')
    fid = open(sha_file, 'w')
    if sha is not None:
        fid.write('mfem = "' + sha + '"')
    fid.close()


def cmake(path, **kwargs):
    '''
    run cmake. must be called in the target directory
    '''
    command = ['cmake', path]
    for key, value in kwargs.items():
        command.append('-' + key + '=' + value)
    make_call(command)


def find_libpath_from_prefix(lib, prefix0):
    prefix0 = os.path.expanduser(prefix0)
    prefix0 = abspath(prefix0)
    soname = 'lib' + lib + dylibext
    path = os.path.join(prefix0, 'lib', soname)
    if not os.path.exists(path):
        path = os.path.join(prefix0, 'lib64', soname)
        if not os.path.exists(path):
            return ''
    return path

###
#  build libraries
###


def cmake_make_hypre():
    '''
    build hypre
    '''
    if verbose:
        print("Building hypre")

    cmbuild = 'cmbuild'
    path = os.path.join(extdir, 'hypre', 'src', cmbuild)
    if os.path.exists(path):
        print("working directory already exists!")
    else:
        os.makedirs(path)

    pwd = chdir(path)

    cmake_opts = {'DCMAKE_VERBOSE_MAKEFILE': '1',
                  'DBUILD_SHARED_LIBS': '1',
                  'DHYPRE_INSTALL_PREFIX': hypre_prefix,
                  'DHYPRE_ENABLE_SHARED': '1',
                  'DCMAKE_INSTALL_PREFIX': hypre_prefix,
                  'DCMAKE_INSTALL_NAME_DIR': os.path.join(hypre_prefix, 'lib'), }

    if enable_cuda and enable_cuda_hypre:
        # in this case, settitng CMAKE_C_COMPILER
        # causes "mpi.h" not found error. For now, letting CMAKE
        # to find MPI
        cmake_opts['DHYPRE_WITH_CUDA'] = '1'
        if cuda_arch != '':
            cmake_opts['DCMAKE_CUDA_ARCHITECTURES'] = cuda_arch
    else:
        cmake_opts['DCMAKE_C_COMPILER'] = mpicc_command

    cmake('..', **cmake_opts)

    make('hypre')
    make_install('hypre')

    os.chdir(pwd)


def make_metis(use_int64=False, use_real64=False):
    '''
    build metis
    '''
    if verbose:
        print("Building metis")

    path = os.path.join(extdir, 'metis')
    if not os.path.exists(path):
        assert False, "metis is not downloaded"

    pwd = chdir(path)

    sed_command = find_command('sed')
    if sed_command is None:
        assert False, "sed is not foudn"

    if use_int64:
        command = [sed_command, '-i',
                   's/#define IDXTYPEWIDTH 32/#define IDXTYPEWIDTH 64/g',
                   'include/metis.h']
    else:
        command = [sed_command, '-i',
                   's/#define IDXTYPEWIDTH 64/#define IDXTYPEWIDTH 32/g',
                   'include/metis.h']

    if use_real64:
        command = [sed_command, '-i',
                   's/#define REALTYPEWIDTH 32/#define REALTYPEWIDTH 64/g',
                   'include/metis.h']
    else:
        command = [sed_command, '-i',
                   's/#define REALTYPEWIDTH 64/#define REALTYPEWIDTH 32/g',
                   'include/metis.h']
    make_call(command)

    command = ['make', 'config', 'shared=1',
               'prefix=' + metis_prefix,
               'cc=' + cc_command]
    make_call(command)
    make('metis')
    make_install('metis')

    if platform == "darwin":
        command = ['install_name_tool',
                   '-id',
                   os.path.join(metis_prefix, 'lib', 'libmetis.dylib'),
                   os.path.join(metis_prefix, 'lib', 'libmetis.dylib'), ]
        make_call(command)
    os.chdir(pwd)


def make_libceed(serial=False):
    if verbose:
        print("Building libceed")

    path = os.path.join(extdir, 'libceed')
    if not os.path.exists(path):
        assert False, "libceed is not downloaded"

    pwd = chdir(path)
    try:
        make_call(['make', 'clean'])
    except:
        pass

    if enable_cuda:
        command = ['make', 'configure', 'CUDA_DIR='+cuda_prefix]
        make_call(command)

    make('libceed')
    make_install('libceed', prefix=libceed_prefix)
    os.chdir(pwd)


def make_gslib(serial=False):
    if verbose:
        print("Building gslib")

    path = os.path.join(extdir, 'gslib')
    if not os.path.exists(path):
        assert False, "gslib is not downloaded"

    pwd = chdir(path)
    make_call(['make', 'clean'])
    if serial:
        command = ['make', 'CC=' + cc_command, 'MPI=0', 'CFLAGS=-fPIC']
        make_call(command)
        command = ['make', 'DESTDIR=' + gslibs_prefix]
        make_call(command)
    else:
        command = ['make', 'CC=' + mpicc_command, 'CFLAGS=-O2 -fPIC']
        make_call(command)
        command = ['make', 'DESTDIR=' + gslibp_prefix]
        make_call(command)
    os.chdir(pwd)


def cmake_make_mfem(serial=True):
    '''
    build MFEM
    '''
    cmbuild = 'cmbuild_ser' if serial else 'cmbuild_par'
    path = os.path.join(extdir, 'mfem', cmbuild)
    if os.path.exists(path):
        print("working directory already exists!")
    else:
        os.makedirs(path)

    ldflags = os.getenv('LDFLAGS') if os.getenv('LDFLAGS') is not None else ''

    rpaths = []

    def add_rpath(p):
        print("checking this", p)
        if not p in rpaths:
            rpaths.append(p)

    cmake_opts = {'DCMAKE_VERBOSE_MAKEFILE': '1',
                  'DBUILD_SHARED_LIBS': '1',
                  'DMFEM_ENABLE_EXAMPLES': '1',
                  'DMFEM_ENABLE_MINIAPPS': '1',
                  'DCMAKE_SHARED_LINKER_FLAGS': ldflags,
                  'DMFEM_USE_ZLIB': '1',
                  'DCMAKE_CXX_FLAGS': cxx11_flag,
                  'DCMAKE_BUILD_WITH_INSTALL_RPATH': '1'}

    if serial:
        cmake_opts['DCMAKE_CXX_COMPILER'] = cxx_command
        cmake_opts['DMFEM_USE_EXCEPTIONS'] = '1'
        cmake_opts['DCMAKE_INSTALL_PREFIX'] = mfems_prefix

        add_rpath(os.path.join(mfems_prefix, 'lib'))

    else:
        cmake_opts['DCMAKE_CXX_COMPILER'] = mpicxx_command
        cmake_opts['DMFEM_USE_EXCEPTIONS'] = '0'
        cmake_opts['DCMAKE_INSTALL_PREFIX'] = mfemp_prefix
        cmake_opts['DMFEM_USE_MPI'] = '1'
        cmake_opts['DMFEM_USE_METIS_5'] = '1'
        cmake_opts['DHYPRE_DIR'] = hypre_prefix
        cmake_opts['DMETIS_DIR'] = metis_prefix

        #cmake_opts['DCMAKE_CXX_STANDARD_LIBRARIES'] = "-lHYPRE -lmetis"
        add_rpath(os.path.join(mfemp_prefix, 'lib'))

        hyprelibpath = os.path.dirname(
            find_libpath_from_prefix(
                'HYPRE', hypre_prefix))
        metislibpath = os.path.dirname(
            find_libpath_from_prefix(
                'metis', metis_prefix))

        add_rpath(metislibpath)
        add_rpath(hyprelibpath)

        ldflags = "-L" + metislibpath + " " + ldflags
        ldflags = "-L" + hyprelibpath + " " + ldflags
        cmake_opts['DCMAKE_SHARED_LINKER_FLAGS'] = ldflags
        cmake_opts['DCMAKE_EXE_LINKER_FLAGS'] = ldflags

        if enable_strumpack:
            cmake_opts['DMFEM_USE_STRUMPACK'] = '1'
            cmake_opts['DSTRUMPACK_DIR'] = strumpack_prefix
            libpath = os.path.dirname(
                find_libpath_from_prefix("STRUMPACK", strumpack_prefix))
            add_rpath(libpath)
        if enable_pumi:
            cmake_opts['DMFEM_USE_PUMI'] = '1'
            cmake_opts['DPUMI_DIR'] = pumi_prefix
            libpath = os.path.dirname(
                find_libpath_from_prefix("pumi", strumpack_prefix))
            add_rpath(libpath)

    if enable_cuda:
        cmake_opts['DMFEM_USE_CUDA'] = '1'
        if cuda_arch != '':
            cmake_opts['DCMAKE_CUDA_ARCHITECTURES'] = cuda_arch
        
    if enable_libceed:
        cmake_opts['DMFEM_USE_CEED'] = '1'
        cmake_opts['DCEED_DIR'] = libceed_prefix
        libpath = os.path.dirname(
            find_libpath_from_prefix("ceed", libceed_prefix))
        add_rpath(libpath)

    if enable_gslib:
        if serial:
            pass
            #cmake_opts['DMFEM_USE_GSLIB'] = '1'
            #cmake_opts['DGSLIB_DIR'] = gslibs_prefix
        else:
            cmake_opts['DMFEM_USE_GSLIB'] = '1'
            cmake_opts['DGSLIB_DIR'] = gslibp_prefix
            
    if enable_suitesparse:
        if serial:
            pass
        else:
            cmake_opts['DMFEM_USE_SUITESPARSE'] = '1'
            if suitesparse_prefix != '':
                 cmake_opts['DSuiteSparse_DIR'] = suitesparse_prefix
        

    cmake_opts['DCMAKE_INSTALL_RPATH'] = ":".join(rpaths)
    
    pwd = chdir(path)
    cmake('..', **cmake_opts)

    txt = 'serial' if serial else 'parallel'
    make('mfem_' + txt)
    make_install('mfem_' + txt)

    os.chdir(pwd)


def write_setup_local():
    '''
    create setup_local.py. parameters written here will be read
    by setup.py in mfem._ser and mfem._par
    '''
    import numpy

    # if build_mfem:
    #    mfemser = os.path.join(prefix, 'mfem', 'ser')
    #    mfempar = os.path.join(prefix, 'mfem', 'par')
    # else:
    mfemser = mfems_prefix
    mfempar = mfemp_prefix

    hyprelibpath = os.path.dirname(
        find_libpath_from_prefix(
            'HYPRE', hypre_prefix))
    metislibpath = os.path.dirname(
        find_libpath_from_prefix(
            'metis', metis_prefix))

    mfems_tpl = read_mfem_tplflags(mfems_prefix)
    mfemp_tpl = read_mfem_tplflags(mfemp_prefix)
    print(mfems_tpl, mfemp_tpl)
    
    params = {'cxx_ser': cxx_command,
              'cc_ser': cc_command,
              'cxx_par': mpicxx_command,
              'cc_par': mpicc_command,
              'whole_archive': '--whole-archive',
              'no_whole_archive': '--no-whole-archive',
              'nocompactunwind': '',
              'swigflag': '-Wall -c++ -python -fastproxy -olddefs -keyword',

              'hypreinc': os.path.join(hypre_prefix, 'include'),
              'hyprelib': hyprelibpath,
              'metisinc': os.path.join(metis_prefix, 'include'),
              'metis5lib': metislibpath,
              'numpync': numpy.get_include(),
              'mfembuilddir': os.path.join(mfempar, 'include'),
              'mfemincdir': os.path.join(mfempar, 'include', 'mfem'),
              'mfemlnkdir': os.path.join(mfempar, 'lib'),
              'mfemserbuilddir': os.path.join(mfemser, 'include'),
              'mfemserincdir': os.path.join(mfemser, 'include', 'mfem'),
              'mfemserlnkdir': os.path.join(mfemser, 'lib'),
              'mfemsrcdir': os.path.join(mfem_source),
              'mfemstpl': mfems_tpl,
              'mfemptpl': mfemp_tpl,
              'add_pumi': '',
              'add_strumpack': '',
              'add_cuda': '',
              'add_libceed': '',
              'add_suitesparse': '',              
              'add_gslib': '',
              'add_gslibp': '',
              'add_gslibs': '',
              'libceedinc': os.path.join(libceed_prefix, 'include'),
              'gslibsinc': os.path.join(gslibs_prefix, 'include'),
              'gslibpinc': os.path.join(gslibp_prefix, 'include'),
              'cxx11flag': cxx11_flag,
              }

    try:
        import mpi4py  # avaialbility of this is checked before
        params['mpi4pyinc'] = mpi4py.get_include()
    except ImportError:
        params['mpi4pyinc'] = ''

    def add_extra(xxx):
        params['add_' + xxx] = '1'
        params[xxx +
               'inc'] = os.path.join(globals()[xxx +
                                               '_prefix'], 'include')
        params[xxx + 'lib'] = os.path.join(globals()[xxx + '_prefix'], 'lib')

    if enable_pumi:
        add_extra('pumi')
    if enable_strumpack:
        add_extra('strumpack')
    if enable_cuda:
        add_extra('cuda')
    if enable_libceed:
        add_extra('libceed')
    if enable_suitesparse:
        add_extra('suitesparse')        
    # if enable_gslib:
    #    add_extra('gslibs')
    if enable_gslib:
        add_extra('gslibp')

    pwd = chdir(rootdir)

    fid = open('setup_local.py', 'w')
    fid.write("#  setup_local.py \n")
    fid.write("#  generated from setup.py\n")
    fid.write("#  do not edit this directly\n")

    for key, value in params.items():
        text = key.lower() + ' = "' + value + '"'
        fid.write(text + "\n")
    fid.close()

    os.chdir(pwd)


def generate_wrapper():
    '''
    run swig.
    '''
    if dry_run or verbose:
        print("generating SWIG wrapper")
        print("using MFEM source", os.path.abspath(mfem_source))
    if not os.path.exists(os.path.abspath(mfem_source)):
        assert False, "MFEM source directory. Use --mfem-source=<path>"

    def ifiles():
        ifiles = os.listdir()
        ifiles = [x for x in ifiles if x.endswith('.i')]
        ifiles = [x for x in ifiles if not x.startswith('#')]
        ifiles = [x for x in ifiles if not x.startswith('.')]
        return ifiles

    def check_new(ifile):
        wfile = ifile[:-2] + '_wrap.cxx'
        if not os.path.exists(wfile):
            return True
        return os.path.getmtime(ifile) > os.path.getmtime(wfile)

    mfemser = mfems_prefix
    mfempar = mfemp_prefix

    pwd = chdir(os.path.join(rootdir, 'mfem', 'common'))
    command1 = [sys.executable, "generate_lininteg_ext.py"]
    command2 = [sys.executable, "generate_bilininteg_ext.py"]
    make_call(command1)
    make_call(command2)
    os.chdir(pwd)

    swig_command = (find_command('swig') if os.getenv("SWIG") is None
                    else os.getenv("SWIG"))
    if swig_command is None:
        assert False, "SWIG is not installed"

    swigflag = '-Wall -c++ -python -fastproxy -olddefs -keyword'.split(' ')

    pwd = chdir(os.path.join(rootdir, 'mfem', '_ser'))

    serflag = ['-I' + os.path.join(mfemser, 'include'),
               '-I' + os.path.join(mfemser, 'include', 'mfem'),
               '-I' + os.path.abspath(mfem_source)]
    for file in ifiles():
        if not check_new(file):
            continue
        command = [swig_command] + swigflag + serflag + [file]
        make_call(command)

    if not build_parallel:
        os.chdir(pwd)
        return

    chdir(os.path.join(rootdir, 'mfem', '_par'))

    import mpi4py
    parflag = ['-I' + os.path.join(mfempar, 'include'),
               '-I' + os.path.join(mfempar, 'include', 'mfem'),
               '-I' + os.path.abspath(mfem_source),
               '-I' + os.path.join(hypre_prefix, 'include'),
               '-I' + os.path.join(metis_prefix, 'include'),
               '-I' + mpi4py.get_include()]

    if enable_pumi:
        parflag.append('-I' + os.path.join(pumi_prefix, 'include'))
    if enable_strumpack:
        parflag.append('-I' + os.path.join(strumpack_prefix, 'include'))

    for file in ifiles():
        #        pumi.i does not depends on pumi specific header so this should
        #        work
        #        if file == 'pumi.i':# and not enable_pumi:
        #            continue
        if file == 'strumpack.i' and not enable_strumpack:
            continue
        if not check_new(file):
            continue
        command = [swig_command] + swigflag + parflag + [file]
        make_call(command)

    os.chdir(pwd)


def clean_wrapper():

    pwd = chdir(os.path.join(rootdir, 'mfem', '_ser'))

    wfiles = [x for x in os.listdir() if x.endswith('_wrap.cxx')]
    remove_files(wfiles)

    chdir(os.path.join(rootdir, 'mfem', '_par'))
    wfiles = [x for x in os.listdir() if x.endswith('_wrap.cxx')]
    remove_files(wfiles)

    chdir(pwd)


def clean_so():
    pwd = chdir(os.path.join(rootdir, 'mfem', '_ser'))
    for f in os.listdir():
        if f.endswith('.so'):
            os.remove(f)
        if f.endswith('.dylib'):
            os.remove(f)

    chdir(os.path.join(rootdir, 'mfem', '_par'))
    for f in os.listdir():
        if f.endswith('.so'):
            os.remove(f)
        if f.endswith('.dylib'):
            os.remove(f)
    chdir(pwd)


def make_mfem_wrapper(serial=True):
    '''
    compile PyMFEM wrapper code
    '''
    if dry_run or verbose:
        print("compiling wrapper code, serial=" + str(serial))
    if not os.path.exists(os.path.abspath(mfem_source)):
        assert False, "MFEM source directory. Use --mfem-source=<path>"

    record_mfem_sha(mfem_source)

    write_setup_local()

    if serial:
        pwd = chdir(os.path.join(rootdir, 'mfem', '_ser'))
    else:
        pwd = chdir(os.path.join(rootdir, 'mfem', '_par'))

    python = sys.executable
    command = [python, 'setup.py', 'build_ext', '--inplace', '--parallel',
               str(max((multiprocessing.cpu_count() - 1, 1)))]
    make_call(command)
    os.chdir(pwd)


def print_config():
    print("----configuration----")
    print(" prefix", prefix)
    print(" when needed, the dependency (mfem/hypre/metis) will be installed under " +
          ext_prefix)
    print(" build mfem : " + ("Yes" if build_mfem else "No"))
    print(" build metis : " + ("Yes" if build_metis else "No"))
    print(" build hypre : " + ("Yes" if build_hypre else "No"))
    print(" build libceed : " + ("Yes" if build_libceed else "No"))
    print(" build gslib : " + ("Yes" if build_gslib else "No"))
    print(" call SWIG wrapper generator: " + ("Yes" if run_swig else "No"))
    print(" build serial wrapper: " + ("Yes" if build_serial else "No"))
    print(" build parallel wrapper : " + ("Yes" if build_parallel else "No"))

    print(" hypre prefix", hypre_prefix)
    print(" metis prefix", metis_prefix)
    print(" c compiler : " + cc_command)
    print(" c++ compiler : " + cxx_command)
    print(" mpi-c compiler : " + mpicc_command)
    print(" mpi-c++ compiler : " + mpicxx_command)
    print("")


def configure_install(self):
    '''
    called when install workflow is used
    '''
    global prefix, dry_run, verbose, ext_prefix
    global clean_swig, run_swig, swig_only, skip_install
    global build_mfem, build_mfemp, build_parallel, build_serial

    global mfem_branch, mfem_source
    global build_metis, build_hypre, build_libceed, build_gslib

    global mfems_prefix, mfemp_prefix, metis_prefix, hypre_prefix
    global cc_command, cxx_command, mpicc_command, mpicxx_command
    global metis_64
    global enable_cuda, cuda_prefix, enable_cuda_hypre, cuda_arch
    global enable_pumi, pumi_prefix
    global enable_strumpack, strumpack_prefix
    global enable_libceed, libceed_prefix, libceed_only
    global enable_gslib, gslibs_prefix, gslibp_prefix, gslib_only
    global enable_suitesparse, suitesparse_prefix

    verbose = bool(self.verbose) if verbose == -1 else verbose
    dry_run = bool(self.dry_run) if dry_run == -1 else dry_run
    if dry_run:
        verbose = True

    prefix = abspath(self.prefix)
    mfem_source = abspath(self.mfem_source)

    skip_ext = bool(self.skip_ext)
    skip_install = bool(self.build_only)
    swig_only = bool(self.swig)
    ext_only = bool(self.ext_only)

    metis_64 = bool(self.with_metis64)
    enable_pumi = bool(self.with_pumi)
    enable_strumpack = bool(self.with_strumpack)
    enable_cuda = bool(self.with_cuda)
    enable_cuda_hypre = bool(self.with_cuda_hypre)
    if self.cuda_arch is not None:
        cuda_arch = self.cuda_arch
    enable_libceed = bool(self.with_libceed)
    libceed_only = bool(self.libceed_only)
    enable_gslib = bool(self.with_gslib)
    gslib_only = bool(self.gslib_only)
    enable_suitesparse = bool(self.with_suitesparse)    

    build_parallel = bool(self.with_parallel)     # controlls PyMFEM parallel
    build_serial = not bool(self.no_serial)

    run_swig = swig_only

    if build_serial:
        build_serial = (not swig_only and not ext_only)

    if build_parallel:
        try:
            import mpi4py
        except ImportError:
            assert False, "Can not import mpi4py"

    if self.mfem_prefix != '':
        mfem_prefix = abspath(self.mfem_prefix)
        mfems_prefix = abspath(self.mfem_prefix)
        mfemp_prefix = abspath(self.mfem_prefix)
        if self.mfems_prefix != '':
            mfems_prefix = abspath(self.mfems_prefix)
        if self.mfemp_prefix != '':
            mfemp_prefix = abspath(self.mfemp_prefix)

        check = find_libpath_from_prefix('mfem', mfems_prefix)
        assert check != '', "libmfem.so is not found in the specified <path>/lib"
        check = find_libpath_from_prefix('mfem', mfemp_prefix)
        assert check != '', "libmfem.so is not found in the specified <path>/lib"

        build_mfem = False
        hypre_prefix = mfem_prefix
        metis_prefix = mfem_prefix

        if self.mfem_prefix_no_swig != '':
            clean_swig = False
            run_swig = False
        else:
            clean_swig = True
            run_swig = True
        if swig_only:
            clean_swig = False

    else:
        build_mfem = True
        build_mfemp = build_parallel
        build_hypre = build_parallel
        build_metis = build_parallel

        if ext_prefix == '':
            ext_prefix = external_install_prefix()
        hypre_prefix = os.path.join(ext_prefix)
        metis_prefix = os.path.join(ext_prefix)

        mfem_prefix = ext_prefix
        mfems_prefix = os.path.join(ext_prefix, 'ser')
        mfemp_prefix = os.path.join(ext_prefix, 'par')

    if self.mfem_branch != '':
        mfem_branch = self.mfem_branch

    if self.hypre_prefix != '':
        check = find_libpath_from_prefix('HYPRE', self.hypre_prefix)
        assert check != '', "libHYPRE.so is not found in the specified <path>/lib or lib64"
        hypre_prefix = os.path.expanduser(self.hypre_prefix)
        build_hypre = False

    if self.metis_prefix != '':
        check = find_libpath_from_prefix('metis', self.metis_prefix)
        assert check != '', "libmetis.so is not found in the specified <path>/lib or lib64"
        metis_prefix = os.path.expanduser(self.metis_prefix)
        build_metis = False

    if enable_libceed or libceed_only:
        if self.libceed_prefix != '':
            libceed_prefix = os.path.expanduser(self.libceed_prefix)
            build_libceed = False
        else:
            libceed_prefix = mfem_prefix
            build_libceed = True

    if enable_gslib or gslib_only:
        if self.gslib_prefix != '':
            build_gslib = False
            gslibs_prefix = os.path.expanduser(self.gslib_prefix)
            gslibp_prefix = os.path.expanduser(self.gslib_prefix)
        else:
            gslibs_prefix = mfems_prefix
            gslibp_prefix = mfemp_prefix
            build_gslib = True

    if enable_suitesparse and self.suitesparse_prefix != '':
        suitesparse_prefix = self.suitesparse_prefix
        
    if enable_pumi:
        run_swig = True

    if enable_strumpack:
        run_swig = True

    if self.pumi_prefix != '':
        pumi_prefix = abspath(self.pumi_prefix)
    else:
        pumi_prefix = mfem_prefix

    if self.strumpack_prefix != '':
        strumpack_prefix = abspath(self.strumpack_prefix)
    else:
        strumpack_prefix = mfem_prefix

    if enable_cuda:
        nvcc = find_command('nvcc')
        cuda_prefix = os.path.dirname(os.path.dirname(nvcc))

    if self.CC != '':
        cc_command = self.CC
    if self.CXX != '':
        cxx_command = self.CXX
    if self.MPICC != '':
        mpicc_command = self.MPICC
    if self.MPICXX != '':
        mpicxx_command = self.MPICXX

    if skip_ext:
        build_metis = False
        build_hypre = False
        build_mfem = False
        build_mfemp = False
        build_libceed = False
        build_gslib = False

    if swig_only:
        build_serial = False

    if ext_only:
        clean_swig = False
        run_swig = False
        build_serial = False
        build_parallel = False
        skip_install = True

    if libceed_only:
        clean_swig = False
        run_swig = False
        build_mfem = False
        build_mfemp = False
        build_metis = False
        build_hypre = False
        build_gslib = False
        build_serial = False
        build_parallel = False
        build_libceed = True
        skip_install = True

    if gslib_only:
        clean_swig = False
        run_swig = False
        build_mfem = False
        build_mfemp = False
        build_metis = False
        build_hypre = False
        build_serial = False
        build_libceed = False
        build_gslib = True
        skip_install = True

    global is_configured
    is_configured = True


def configure_bdist(self):
    '''
    called when bdist workflow is used
    '''
    global prefix, dry_run, verbose, run_swig
    global build_mfem, build_parallel, build_serial
    global mfem_branch, mfem_source

    global cc_command, cxx_command, mpicc_command, mpicxx_command
    global enable_pumi, pumi_prefix
    global enable_strumpack, strumpack_prefix
    global do_bdist_wheel
    dry_run = bool(self.dry_run) if dry_run == -1 else dry_run
    verbose = bool(self.verbose) if verbose == -1 else verbose

    prefix = abspath(self.bdist_dir)

    run_swig = False
    build_parallel = False
    build_serial = True

    global is_configured
    is_configured = True
    do_bdist_wheel = True

    mfem_source = './external/mfem'


class Install(_install):
    '''
    called when pyton setup.py install
    '''
    user_options = _install.user_options + [
        ('with-parallel', None, 'Installed both serial and parallel version'),
        ('no-serial', None, 'Skip building the serial wrapper'),
        ('mfem-prefix=', None, 'Specify locaiton of mfem' +
         'libmfem.so must exits under <mfem-prefix>/lib. ' +
         'This mode uses clean-swig + run-swig, unless mfem-prefix-no-swig is on'),
        ('mfemp-prefix=', None, 'Specify locaiton of parallel mfem ' +
         'libmfem.so must exits under <mfemp-prefix>/lib. ' +
         'Need to use it with mfem-prefix'),
        ('mfems-prefix=', None, 'Specify locaiton of serial mfem ' +
         'libmfem.so must exits under <mfems-prefix>/lib. ',
         'Need to use it with mfem-prefix'),
        ('mfem-prefix-no-swig', None, 'skip running swig when mfem-prefix is chosen'),
        ('mfem-branch=', None, 'Specify branch of mfem' +
         'MFEM is cloned and built using the specfied branch '),
        ('mfem-source=', None, 'Specify mfem source location' +
         'MFEM source directory. Required to run-swig '),
        ('hypre-prefix=', None, 'Specify locaiton of hypre' +
         'libHYPRE.so must exits under <hypre-prefix>/lib'),
        ('metis-prefix=', None, 'Specify locaiton of metis' +
         'libmetis.so must exits under <metis-prefix>/lib'),
        ('swig', None, 'Run Swig and exit'),
        ('ext-only', None, 'Build metis, hypre, mfem(C++) only'),

        ('skip-ext', None, 'Skip building metis, hypre, mfem(C++) only'),
        ('build-only', None, 'Skip final install stage to prefix'),
        ('CC=', None, 'c compiler'),
        ('CXX=', None, 'c++ compiler'),
        ('MPICC=', None, 'mpic compiler'),
        ('MPICXX=', None, 'mpic++ compiler'),

        ('with-cuda', None, 'enable cuda'),
        ('with-cuda-hypre', None, 'enable cuda in hypre'),
        ('cuda-arch=', None, 'set cuda compute capability. Ex if A100, set to 80'),
        ('with-metis64', None, 'use 64bit int in metis'),
        ('with-pumi', None, 'enable pumi (parallel only)'),
        ('pumi-prefix=', None, 'Specify locaiton of pumi'),
        ('with-suitesparse', None, 'build MFEM with suitesparse (MFEM_USE_SUITESPARSE=YES) (parallel only)'),
        ('suitesparse-prefix=', None, 'Specify locaiton of suitesparse (=SuiteSparse_DIR)'),
        ('with-libceed', None, 'enable libceed'),
        ('libceed-prefix=', None, 'Specify locaiton of libceed'),
        ('libceed-only', None, 'Build libceed only'),
        ('gslib-prefix=', None, 'Specify locaiton of gslib'),
        ('with-gslib', None, 'enable gslib (parallel only)'),
        ('gslib-only', None, 'Build gslib only'),
        ('with-strumpack', None, 'enable strumpack (parallel only)'),
        ('strumpack-prefix=', None, 'Specify locaiton of strumpack'),
    ]

    def initialize_options(self):
        _install.initialize_options(self)
        self.swig = False
        self.ext_only = False

        self.skip_ext = False
        self.with_parallel = False
        self.build_only = False
        self.no_serial = False
        self.mfem_prefix = ''
        self.mfems_prefix = ''
        self.mfemp_prefix = ''
        self.mfem_source = './external/mfem'
        self.mfem_prefix_no_swig = ''
        self.mfem_branch = ''
        self.metis_prefix = ''
        self.hypre_prefix = ''

        self.with_cuda = False
        self.with_cuda_hypre = False
        self.cuda_arch = None
        self.with_metis64 = False

        self.with_pumi = False
        self.pumi_prefix = ''

        self.with_strumpack = False
        self.strumpack_prefix = ''

        self.with_suitesparse = False
        self.suitesparse_prefix = ''        

        self.with_libceed = False
        self.libceed_prefix = ''
        self.libceed_only = False

        self.with_gslib = False
        self.gslib_prefix = ''
        self.gslib_only = False

        self.CC = ''
        self.CXX = ''
        self.MPICC = ''
        self.MPICXX = ''

    def finalize_options(self):
        if (bool(self.ext_only) and bool(self.skip_ext)):
            assert False, "skip-ext and ext-only can not use together"

        given_prefix = True
        if (self.prefix == '' or
                self.prefix is None):
            given_prefix = False
        else:
            self.prefix = os.path.expanduser(self.prefix)
            prefix = self.prefix

        global verbose
        verbose = bool(self.verbose)
        if given_prefix:
            global ext_prefix
            self.prefix = prefix
            ext_prefix = prefix
        else:
            if '--user' in sys.argv:
                path = site.getusersitepackages()
                if not os.path.exists(path):
                    try:
                        print("attempting to make a --user directory", path)
                        os.makedirs(path)
                    except BaseException:
                        pass
                if os.path.exists(path):
                    path = os.path.dirname(path)
                    path = os.path.dirname(path)
                    path = os.path.dirname(path)
                else:
                    assert False, "no installation path found"
                self.prefix = path
            else:
                self.prefix = sys.prefix

        self.user = 0
        _install.finalize_options(self)

        if verbose:
            print("prefix is :", self.prefix)

    def run(self):
        if not is_configured:
            configure_install(self)
            print_config()

        if swig_only:
            self.run_command("build")
        else:
            _install.run(self)


class BuildPy(_build_py):
    '''
    Called when python setup.py build_py
    '''
    user_options = _build_py.user_options

    def initialize_options(self):
        _build_py.initialize_options(self)

    def finalize_options(self):
        _build_py.finalize_options(self)

    def run(self):
        if not swig_only:
            if build_metis:
                download('metis')
                make_metis(use_int64=metis_64)
            if build_hypre:
                download('hypre')
                cmake_make_hypre()
            if build_libceed:
                download('libceed')
                #gitclone('libceed',branch='main')
                make_libceed()
            if build_gslib:
                download('gslib')
                make_gslib()
                make_gslib(serial=True)

            mfem_downloaded = False
            if build_mfem:
                gitclone('mfem', use_sha=True) if mfem_branch is None else gitclone(
                    'mfem', branch=mfem_branch)
                mfem_downloaded = True
                cmake_make_mfem(serial=True)

            if build_mfemp:
                if not mfem_downloaded:
                    gitclone('mfem', use_sha=True) if mfem_branch is None else gitclone(
                        'mfem', branch=mfem_branch)
                cmake_make_mfem(serial=False)

        if clean_swig:
            clean_wrapper()
        if run_swig:
            generate_wrapper()
            if swig_only:
                return

        if build_serial:
            make_mfem_wrapper(serial=True)
        if build_parallel:
            make_mfem_wrapper(serial=False)

        if not skip_install:
            _build_py.run(self)
        else:
            sys.exit()


if haveWheel:
    class BdistWheel(_bdist_wheel):
        '''
        Wheel build performs serial+paralell
        '''

        def finalize_options(self):
            def _has_ext_modules():
                return True
            from setuptools.dist import Distribution
            #Distribution.is_pure = _is_pure
            self.distribution.has_ext_modules = _has_ext_modules
            _bdist_wheel.finalize_options(self)

        def run(self):
            if not is_configured:
                print('running config')
                configure_bdist(self)
                print_config()
            self.run_command("build")
            _bdist_wheel.run(self)
            #assert False, "bdist install is not supported, use source install"

            # Ensure that there is a basic library build for bdist_egg to pull from.
            # self.run_command("build")
            # _cleanup_symlinks(self)

            # Run the default bdist_wheel command


class InstallLib(_install_lib):
    def finalize_options(self):
        _install_lib.finalize_options(self)
        src_cmd_obj = self.distribution.get_command_obj('install')
        src_cmd_obj.ensure_finalized()
        self.install_dir = src_cmd_obj.install_platlib


class InstallEggInfo(_install_egg_info):
    def run(self):
        if not dry_run:
            _install_egg_info.run(self)
        else:
            print("skipping regular install_egg_info")


class InstallScripts(_install_scripts):
    def run(self):
        if not dry_run:
            _install_scripts.run(self)
        else:
            print("skipping regular install_scripts")


class Clean(_clean):
    '''
    Called when python setup.py clean
    '''
    user_options = _clean.user_options + [
        ('ext', None, 'clean exteranal dependencies)'),
        ('mfem', None, 'clean mfem'),
        ('metis', None, 'clean metis'),
        ('hypre', None, 'clean hypre'),
        ('swig', None, 'clean swig'),
        ('all-exts', None, 'delete all externals'),
    ]

    def initialize_options(self):
        _clean.initialize_options(self)
        self.ext = False
        self.mfem = False
        self.hypre = False
        self.metis = False
        self.swig = False
        self.all_exts = False

    def run(self):
        global dry_run, verbose
        dry_run = self.dry_run
        verbose = bool(self.verbose)

        os.chdir(extdir)

        make_command = find_command('make')

        if self.ext or self.mfem:
            path = os.path.join(extdir, 'mfem', 'cmbuild_par')
            if os.path.exists(path):
                shutil.rmtree(path)
            path = os.path.join(extdir, 'mfem', 'cmbuild_ser')
            if os.path.exists(path):
                shutil.rmtree(path)
        if self.ext or self.hypre:
            path = os.path.join(extdir, 'hypre', 'cmbuild')
            if os.path.exists(path):
                shutil.rmtree(path)
        if self.ext or self.metis:
            path = os.path.join(extdir, 'metis')
            if os.path.exists(path):
                os, chdir(path)
                command = ['make', 'clean']
                subprocess.check_call(command)
        if self.all_exts or self.hypre:
            for xxx in ('metis', 'hypre', 'mfem'):
                path = os.path.join(extdir, xxx)
                if os.path.exists(path):
                    shutil.rmtree(path)
        if self.swig:
            clean_wrapper()

        clean_so()

        os.chdir(rootdir)
        _clean.run(self)


#cdatafiles = [os.path.join('data', f) for f in os.listdir('data')]


def run_setup():
    setup_args = metadata.copy()
    cmdclass = {'build_py': BuildPy,
                'install': Install,
                'install_lib': InstallLib,
                'install_egg_info': InstallEggInfo,
                'install_scripts': InstallScripts,
                'clean': Clean}
    if haveWheel:
        cmdclass['bdist_wheel'] = BdistWheel

    install_req = install_requires()
    # print(install_req)
    setup(
        cmdclass=cmdclass,
        install_requires=install_req,
        packages=find_packages(),
        extras_require={},
        package_data={'mfem._par': ['*.so'], 'mfem._ser': ['*.so']},
        #data_files=[('data', datafiles)],
        entry_points={},
        **setup_args)


def main():
    run_setup()


if __name__ == '__main__':
    main()
