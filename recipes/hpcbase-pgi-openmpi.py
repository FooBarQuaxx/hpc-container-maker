"""
HPC Base image

Contents:
  CUDA version 9.0
  FFTW version 3.3.7
  HDF5 version 1.10.1
  Mellanox OFED version 3.4-1.0.0.0
  OpenMPI version 3.0.0
  PGI compilers version 18.4
  Python 2 and 3 (upstream)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

# The PGI End-User License Agreement (https://www.pgroup.com/doc/LICENSE)
# must be accepted.
pgi_eula=False
if USERARG.get('pgi_eula_accept', False):
  pgi_eula=True
else:
  raise RuntimeError('PGI EULA not accepted. To accept, use "--userarg pgi_eula_accept=yes"\nSee PGI EULA at https://www.pgroup.com/doc/LICENSE')

######
# Devel stage
######

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image='nvidia/cuda:9.0-devel', _as='devel')

# Python
python = python()
Stage0 += python

# PGI compilers
pgi = pgi(eula=pgi_eula, version='18.4')
Stage0 += pgi

# Setup the toolchain.  Use the PGI compiler toolchain as the basis.
tc = pgi.toolchain
tc.CUDA_HOME = '/usr/local/cuda'

# Mellanox OFED
ofed = mlnx_ofed(version='3.4-1.0.0.0')
Stage0 += ofed

# OpenMPI
ompi = openmpi(version='3.0.0', toolchain=tc)
Stage0 += ompi

# FFTW
fftw = fftw(version='3.3.7', toolchain=tc)
Stage0 += fftw

# HDF5
hdf5 = hdf5(version='1.10.1', toolchain=tc)
Stage0 += hdf5

######
# Runtime image
######

Stage1 += baseimage(image='nvidia/cuda:9.0-runtime')

# Python
Stage1 += python.runtime()

# PGI compiler
Stage1 += pgi.runtime()

# Mellanox OFED
Stage1 += ofed.runtime()

# OpenMPI
Stage1 += ompi.runtime()

# FFTW
Stage1 += fftw.runtime()

# HDF5
Stage1 += hdf5.runtime()
