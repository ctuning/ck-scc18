Portable [Collective Knowledge](https://github.com/ctuning/ck) workflow and reusable components for the 
[CLUSTER competition at Supercomputing'18](https://sc18.supercomputing.org/sc18-announces-selected-paper-for-next-student-cluster-competition-reproducibility-challenge).

Paper: [Extreme scale multi-physics simulations of the tsunamigenic 2004 sumatra megathrust earthquake](https://dl.acm.org/citation.cfm?id=3126948)

[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](https://github.com/ctuning/ck)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)



# CK Installation

The minimal installation requires:

* Python 2.7 or 3.3+ (limitation is mainly due to unitests)
* Git command line client
* wget tool

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via PIP with sudo to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

See [minimal CK installation guide](https://github.com/ctuning/ck#minimal-installation) for further details.
You can also read this [Getting started guide](https://github.com/ctuning/ck/wiki/First-feeling) to grasp CK concepts.


# CK workflow installation with dependencies

```
$ ck pull repo:ck-cluster18
```

# Choosing which compiler and MPI to use

## Intel 

### Intel compilers

If you do not yet have Intel compilers installed on your system, you can download them from [here](https://software.intel.com/en-us/intel-compilers).
You can then automatically detect and register them via CK as follows:

```
$ ck detect soft --tags=compiler,icc
```

Note that if Intel compiler was not automatically found, you can provide a path to Intel installation as follows:
```
$ ck detct soft --tags=compiler,icc --search-dirs=<<INSTALLATION_PATH>>
```

### Intel MPI library

Install Intel MPI lib following the instruction (here)[https://software.seek.intel.com/performance-libraries]
or via (**apt**)[https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-apt-repo]

```
1. wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
2. apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB

3. sudo wget https://apt.repos.intel.com/setup/intelproducts.list -O /etc/apt/sources.list.d/intelproducts.list
4. sudo sh -c 'echo deb https://apt.repos.intel.com/mpi all main > /etc/apt/sources.list.d/intel-mpi.list'
5. sudo apt-get update
6. sudo apt-get install intel-mpi

7. ck detect soft --tags=lib,mpi,intel
```

Note that if this library is installed in an unusual path, you can help CK detect it as follows:
```
7. ck detect soft --tags=lib,mpi,intel --search_dirs=<<INSTALLATION_PATH>>
```

## GCC

You can detect your GCC installation as follows:
```
$ ck detect soft --tags=compiler,gcc
```

OpenMPI will be later automatically detected or installed when you run seissol program for the first time.

# Installing SeisSol version from the above paper

```
ck install package:lib-seissol-201703 --reuse_deps
```

CK will automatically detect or install other subdependencies and will register this library in the virtual CK environment:
```
$ ck show env
```

# Running SeisSol workflow

```
$ ck run program:seissol-netcdf
```

# Customizing SeisSol workflow

```
$ ck run program:seissol-netcdf --env.MPI_NUM_PROCESSES=16 --env.OMP_NUM_THREADS=54
```

## SuperMUC  Phase 2

```
$ ck run program:seissol-netcdf --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=54 --env.KMP_AFFINITY="compact,granularity=thread"
```

## Shaheen  II

```
$ ck run program:seissol-netcdf --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=62 --env.KMP_AFFINITY="compact,granularity=thread"
```

## Cori

```
$ ck run program:seissol-netcdf --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=65 --env.KMP_AFFINITY="proclist =[2-66],explicit,granularity=thread"
```

## Extra parameters

```
$ export XDMFWRITER_ALIGNMENT=8388608
$ export XDMFWRITER_BLOCK_SIZE=8388608
$ export SEISSOL_CHECKPOINT_ALIGNMENT=8388608
$ export SEISSOL_CHECKPOINT_DIRECT=1
$ export ASYNC_MODE=THREAD
$ export ASYNC_BUFFER_ALIGNMENT=8388608
```

or via CK

```
$ ck run program:seissol-netcdf ... --env.XDMFWRITER_ALIGNMENT=8388608 \
    --env.XDMFWRITER_BLOCK_SIZE=8388608 \
    --env.SEISSOL_CHECKPOINT_ALIGNMENT=8388608 \
    --env.SEISSOL_CHECKPOINT_DIRECT=1 \
    --env.ASYNC_MODE=THREAD \
    --env.ASYNC_BUFFER_ALIGNMENT=8388608
```

# Next steps

Adding CK modules and scripts to automatically run and validate all experiments, share results 
and generate interactive article similar to [this one](http://cKnowledge.org/rpi-crowd-tuning).

# Feedback

Get in touch with the CK community about this workflow and CK components [here](https://github.com/ctuning/ck/wiki/Contacts). 
