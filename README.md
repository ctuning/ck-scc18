[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This repository contains a beta [Collective Knowledge](https://github.com/ctuning/ck) 
workflow to automate installation, execution and customization of SeisSol application 
from the [SC18 Student Cluster Competition Reproducibility Challenge](https://sc18.supercomputing.org/sc18-announces-selected-paper-for-next-student-cluster-competition-reproducibility-challenge)
across different platforms, environments and datasets.

* SeisSol paper: [Extreme scale multi-physics simulations of the tsunamigenic 2004 sumatra megathrust earthquake](https://dl.acm.org/citation.cfm?id=3126948)
* Original SeisSol application: https://github.com/SeisSol/SeisSol
* Collective Knowledge concepts and long-term vision to automate and crowdsource complex HPC experiments: https://bit.ly/reboot-open-science
* CK features: https://github.com/ctuning/ck/wiki/Features

*Note that this is an ongoing and evolving project*

# Contributors

* Grigori Fursin, dividiti/cTuning foundation (SC19 reproducibility vice-chair)
* Flavio Vella, Free University of Bozen-Bolzano
* Stephen Herbein, LLNL
* Todd Gamblin, LLNL (SC18 program co-chair)

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
You can also find this [CK getting started guide](https://github.com/ctuning/ck/wiki/First-steps) 
useful if you are not yet familiar with the CK framework.

Finally, please bear in mind that [CK](http://cKnowledge.org) is a continuously evolving community project similar to Wikipedia,
so if you don't like something or something is not working, please do not hesitate to send your feedback
to the [public mailing list](https://groups.google.com/forum/#!forum/collective-knowledge),
open tickets in related [CK GitHub repositories](http://cKnowledge.org/shared-repos.html),
or even contribute patches, updates, new workflows and research components!



# CK workflow installation

```
$ ck pull repo:ck-scc18
```

Note that since we strongly encourage reuse of shared code and data, 
CK will automatically check dependencies 
on other [CK repositories](http://cKnowledge.org/shared-repos.html) 
based on this [.ckr.json](https://github.com/ctuning/ck-scc18/blob/master/.ckr.json#L9),
and will also install them in a user environment. 
In this way, we a user can take advantage of all other CK [modules](http://cKnowledge.org/shared-modules.html),
[software detection plugins](http://cKnowledge.org/shared-soft-detection-plugins.html)
and [packages](http://cKnowledge.org/shared-packages.html) shared by the community!



# SeisSol proxy execution via CK workflow while adapting to a user environment

Now you can try to run a simple 1-node SeisSol proxy application just to test CK workflow:

```
ck run program:seissol-proxy
```

CK original approach is to detect all existing software dependencies (code, data sets, models, etc) 
installed in a user environment via [shared software plugins](http://cKnowledge.org/shared-soft-detection-plugins.html),
registering all versions in a CK light-weight virtual environment 
(automatically generated environment script with preset environment variables
for a given version of a given software), and then using these virtual environments
to build an application. 

You can see all detected environments as follows:
```
$ ck show env
```

Only when a given software dependency is not found, CK will attempt to automatically
install missing software via [CK packages](http://cKnowledge.org/shared-packages.html)
which are just wrappers with a unified API to other build tools and package managers 
such as [spack](https://spack.io), [easybuild](https://easybuild.readthedocs.io/en/latest/), make, cmake, scons, etc.

The whole point of CK is to let researchers reuse past workflows in a new environment 
and adapt to it even if it can fail, rather than enforcing the use of fixed and quickly
outdated dependencies (such as when sharing Docker/VM images). At the same time,
CK also allows stable versions of workflows with fixed versions of software dependencies!

*Therefore, if something fails, the idea is to collaboratively fix shared workflows,
modules, software detection plugins and packages, thus continuously improving and adapting
them to new platforms and environments, in the spirit of Wikipedia!*

For example, our LLNL colleagues already noticed that current software detection is very slow
on NFS or some software detection plugins can hang, and opened a ticket 
which we will be resolving soon: https://github.com/ctuning/ck-env/issues/85.
Feel free to join our [active CK Slack channel]() to monitor the progress and 
participate in discussions!


# Helping CK detect software dependencies

Sometimes CK software detection plugins can't find a given software if it's in an unusual path,
or if it simply takes too long to find it (see above issue with NFS). In such case, you
can help CK to manually detect and register a given software.

For example, you can force CK to detect and register a given python version as follows:

```
$ ck detect soft --tags=compiler,python --full_path={full path to a given python compiler}
$ ck show env --tags=compiler
```

## Intel compilers

If you do not yet have Intel compilers installed on your system, you can download them from [here](https://software.intel.com/en-us/intel-compilers).
You can then automatically detect and register them via CK as follows:

```
$ ck detect soft --tags=compiler,icc
```

Note that if Intel compiler was not automatically found, you can provide a path to Intel installation as follows:
```
$ ck detect soft --tags=compiler,icc --search-dirs={INSTALLATION_PATH}
```

If automatic detection is too slow (on NFS), use the following command:
```
$ ck detect soft --tags=compiler,icc --full_path={full path to compilervars.sh}
```

## Intel MPI library

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
7. ck detect soft --tags=lib,mpi,intel --search_dirs={INSTALLATION_PATH}
```

If automatic detection is too slow (on NFS), use the following command:
```
$ ck detect soft --tags=lib,mpi,intel --full_path={full path to mpiicc}
```

## GCC

You can detect and register different GCC versions in the CK as follows:
```
$ ck detect soft --tags=compiler,gcc
```

OpenMPI will be later automatically detected or installed when you run seissol program for the first time.

## SeisSol lib

You can also try to install SeisSol library yourself via CK (useful for debugging)
before running the workflow:

```
ck install package:lib-seissol-scc18-proxy --reuse_deps
```



# Running the workflow again

If all software dependencies were detected or installed successfully, 
they will be automatically picked up by CK when you run the same workflow again:

```
ck run program:seissol-proxy
```

Furthermore, all these environments will be now reused across all other CK workflows!


# Installing SeisSol MPI version

For example, you can now try to install full SeisSol application as follows:

```
ck install package:lib-seissol-scc18 --reuse_deps
```

You can see that CK now reuses all registered environments, and attempt to detect
or install the new ones:

```
$ ck show env
```

## Troubleshooting

If compilation fails due to incompatible GCC (we had some issues building SeisSol using GCC 7.3 on a few platforms), 
you can detect other GCC versions via CK and then use them with above workflows as follows:
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
or
```
$ ck detect soft:compiler.gcc --full_path={full path to gcc}
```

If you still encounter problems, please feel free to get in touch with the 
[CK community](https://github.com/ctuning/ck/wiki/Contacts) and we will help you fix them. 
You feedback is very important since the whole point of CK is to continuously and collaboratively 
improve all shared research workflows and components thus gradually improving 
their stability and reproducibility across diverse platforms and environments!

# Running SeisSol MPI workflow

*We are now working with the community to automate execution of this application via mpirun - 
please join our [CK mailing list](https://groups.google.com/forum/#!forum/collective-knowledge)
to follow the news!*

In the mean time, you can try to run beta SeisSol workflow as follows:

```
$ ck run program:seissol-netcdf
```

You can also start a CK virtual environment and run the code yourself as follows:
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

* LLNL: add installation of SeisSol dependencies via [spack](https://github.com/spack/spack);
* LLNL+dividiti: Prototype execution of seissol via [Flux](https://github.com/flux-framework/flux-core);
* Check [easybuild](https://easybuild.readthedocs.io/en/latest);
* dividiti: add public [CK scoreboard](http://cKnowledge.org/repo) to exchange results.

