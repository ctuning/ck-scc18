[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This repository contains [Collective Knowledge](https://github.com/ctuning/ck) 
workflows and [reusable research components](http://cKnowledge.org) 
to automate installation, execution and customization of SeisSol application 
from the [SC18 Student Cluster Competition Reproducibility Challenge](https://sc18.supercomputing.org/sc18-announces-selected-paper-for-next-student-cluster-competition-reproducibility-challenge)
across diverse platforms and environments.

* Collective Knowledge concepts and long-term vision to automate and crowdsource complex HPC experiments: https://bit.ly/reboot-open-science
* SeisSol paper: [Extreme scale multi-physics simulations of the tsunamigenic 2004 sumatra megathrust earthquake](https://dl.acm.org/citation.cfm?id=3126948)
* Original SeisSol application: https://github.com/SeisSol/SeisSol

# CK Installation

CK requires minimal dependencies:

* Python 2.7 or 3+
* git command line client
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

Please check [minimal CK installation guide](https://github.com/ctuning/ck#minimal-installation) 
and [CK customization](https://github.com/ctuning/ck/wiki/Customization) 
if you need more details about installation process.

You can also find this [Getting started guide](https://github.com/ctuning/ck/wiki/First-steps) 
useful if you are not yet familiar with the CK framework.

Finally, please bear in mind that CK is a continuously evolving community project similar to Wikipedia,
so if you don't like something or something is not working, please do not hesistate to send your feedback
to the [public CK mailing list](https://groups.google.com/forum/#!forum/collective-knowledge),
open tickets in related [CK GitHub repositories](http://cKnowledge.org/shared-repos.html),
or even contribute patches, updates, new workflows and research components!

# CK workflow installation with dependencies

```
$ ck pull repo:ck-scc18
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
$ ck detect soft --tags=compiler,icc --search-dirs=<<INSTALLATION_PATH>>
```

### Intel MPI library

Install Intel MPI lib following the instruction [here](https://software.seek.intel.com/performance-libraries)
or via [**apt**](https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-apt-repo)

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

# Installing and testing SeisSol proxy version from the above paper

```
ck install package:lib-seissol-scc18-proxy --reuse_deps
ck run program:seissol-proxy
```

# Installing SeisSol version from the above paper

```
ck install package:lib-seissol-scc18 --reuse_deps
```

CK will automatically detect or install other sub-dependencies and will register this library in the virtual CK environment:
```
$ ck show env
```

CK will automatically detect or install other sub-dependencies and will register this library in the virtual CK environment:
```
$ ck show env
```

## Troubleshooting

If compilation fails due to incompatible GCC (we had some issues building SeisSol using GCC 7.3 on a few platforms), 
you can detect other GCC versions via CK and then use them as follows:
```
$ ck detect soft:compiler.gcc

```

and then restart SeisSol installation;
```
ck install package:lib-seissol-scc18 --reuse_deps --rebuild
```

If required GCC is in an unusual path, you can help CK detect it by providing a search path as follows:
```
$ ck detect soft:compiler.gcc --search_dirs={path to GCC installation}
```

If you still encounter problems, please feel free to get in touch with the 
[CK community](https://github.com/ctuning/ck/wiki/Contacts) and we will help you fix them. 
You feedback is very important since the whole point of CK is to continuously and collaboratively 
improve all shared research workflows and components thus gradually improving 
their stability and reproducibility across diverse platforms and environments!

# Running SeisSol workflow

Running SeisSol is an on-going work:

```
$ ck run program:seissol-netcdf
```

In the mean time, you can start CK virtual environment and run the code yourself as follows:
```
$ ck virtual env --tags=lib,seissol

> cd ${CK_ENV_LIB_SEISSOL_BIN}
> ls

> echo ${CK_ENV_LIB_SEISSOL_BINARY}
> echo ${CK_ENV_LIB_SEISSOL_BINARY_FULL}
> echo ${CK_ENV_LIB_SEISSOL_MAPLE}
> echo ${CK_ENV_LIB_SEISSOL_SET}
> echo ${CK_ENV_LIB_SEISSOL_SRC}
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

* LLNL: add installation of software dependencies via [spack](https://github.com/spack/spack);
* LLNL+dividiti: Prototype execution of seissol via [Flux](https://github.com/flux-framework/flux-core);
* Check [easybuild](https://easybuild.readthedocs.io/en/latest);
* dividiti: add public [CK scoreboard](http://cKnowledge.org/repo) to exchange results.

Get in touch with the CK community about this workflow and CK components [here](https://github.com/ctuning/ck/wiki/Contacts). 
