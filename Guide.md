<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Workflow authors and contributors](#workflow-authors-and-contributors)
- [Introduction](#introduction)
- [Installing and customizing CK](#installing-and-customizing-ck)
- [Installing CK workflow for SeisSol](#installing-ck-workflow-for-seissol)
- [Updating this workflow and dependencies](#updating-this-workflow-and-dependencies)
- [Testing SeisSol proxy application via CK](#testing-seissol-proxy-application-via-ck)
- [Installing SeisSol proxy library manually](#installing-seissol-proxy-library-manually)
- [Preparing and running SeisSol MPI workflow](#preparing-and-running-seissol-mpi-workflow)
  - [Installing and parameterizing SeisSol library](#installing-and-parameterizing-seissol-library)
  - [Running SeisSol MPI](#running-seissol-mpi)
  - [Running SeisSol MPI with a small data set](#running-seissol-mpi-with-a-small-data-set)
  - [Using job managers](#using-job-managers)
    - [Slurm](#slurm)
    - [Flux](#flux)
- [Customizing SeisSol workflow](#customizing-seissol-workflow)
  - [Using different MPI libraries](#using-different-mpi-libraries)
  - [Using Intel compilers and MPI](#using-intel-compilers-and-mpi)
    - [Detecting multiple Intel compilers](#detecting-multiple-intel-compilers)
    - [Detecting Intel MPI library](#detecting-intel-mpi-library)
  - [Using stable dependencies](#using-stable-dependencies)
    - [Installing dependencies via Spack](#installing-dependencies-via-spack)
    - [Installing dependencies via EasyBuild](#installing-dependencies-via-easybuild)
  - [Using different platforms to run SeisSol](#using-different-platforms-to-run-seissol)
    - [Using "SuperMUC Phase 2" platform](#using-supermuc-phase-2-platform)
    - [Using "Shaheen II" platform](#using-shaheen-ii-platform)
    - [Using "Cori" platform](#using-cori-platform)
    - [Using "Piz Daint" platform](#using-piz-daint-platform)
  - [Changing other parameters](#changing-other-parameters)
  - [Running SeisSol binary without CK](#running-seissol-binary-without-ck)
  - [Creating a self-contained snapshot of this workflow](#creating-a-self-contained-snapshot-of-this-workflow)
- [Contacting the CK community](#contacting-the-ck-community)
- [Acknowledgments](#acknowledgments)
- [Future work](#future-work)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->




# Workflow authors and contributors

* Grigori Fursin, dividiti/cTuning foundation (CK workflow implementation)
* Flavio Vella, Free University of Bozen-Bolzano (CK workflow implementation)
* Stephen Herbein, LLNL (testing and Flux)
* Todd Gamblin, LLNL (spack feedback)
* Kenneth Hoste, Ghent University (EasyBuild feedback)
* Damian Alvarez, Jülich Supercomputing Centre (testing and EasyBuild feedback)
* Carsten Uphoff, TUM (testing and feedback)
* Michael Bader, TUM (testing and feedback)





# Introduction

This repository contains a proof-of-concept [Collective Knowledge](https://github.com/ctuning/ck) 
workflow to automate installation, execution and customization of SeisSol application 
from the [SC18 Student Cluster Competition Reproducibility Challenge](https://sc18.supercomputing.org/sc18-announces-selected-paper-for-next-student-cluster-competition-reproducibility-challenge)
across different platforms, environments and datasets. See [CK motivation](https://github.com/ctuning/ck/wiki/Publications)
about our concept to automatically generate reproducible articles with portable workflows and reusable research components.

*Note that this is an ongoing and evolving project!*

**Related resources**

* SeisSol:
  * [Paper "Extreme scale multi-physics simulations of the tsunamigenic 2004 sumatra megathrust earthquake"](https://dl.acm.org/citation.cfm?id=3126948)
  * [Application (GitHub)](https://github.com/SeisSol/SeisSol)
  * [Wiki for SCC18](https://github.com/SeisSol/SeisSol/wiki/2018-Student-Cluster-Competition)

* Collective Knowledge:
  * [Project website](http://cKnowledge.org)
  * [CK motivation publications](https://github.com/ctuning/ck/wiki/Publications)
  * [Presentation](https://bit.ly/reboot-open-science)
  * [Documentation](https://github.com/ctuning/ck/wiki)
  * [Getting Started Guide](https://github.com/ctuning/ck/wiki/First-steps)

* Events
  * [RESCUE-HPC@SC18 workshop](http://rescue-hpc.org)
  * [Artifact Evaluation](http://cTuning.org/ae)









# Installing and customizing CK

First you need to install Collective Knowledge framework (CK) as described 
[here](https://github.com/ctuning/ck#Installation). 

If you have never used CK, we also suggest you to check this
[CK getting started guide](https://github.com/ctuning/ck/wiki/First-Steps).

You may also want to check how to [customize your CK installation](https://github.com/ctuning/ck/wiki/Customization).

For example, you can force CK to install all repositories and packages (code, data sets and models) 
to your **parallel IO or scratch file system** instead of the default ${HOME}/CK and ${HOME}/CK-TOOLS
by specifying paths using environment variables "CK_REPOS" and "CK_TOOLS" respectively! 




*Note that [CK](https://github.com/ctuning/ck/wiki) 
is a continuously evolving community project similar to Wikipedia,
so if you don't like something or something is not working, 
please do not hesitate to send your feedback
to the [public mailing list](https://groups.google.com/forum/#!forum/collective-knowledge),
open tickets in related [CK GitHub repositories](http://cKnowledge.org/shared-repos.html),
or even contribute patches, updates, new workflows and research components!*






# Installing CK workflow for SeisSol

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

You can find where CK stores all such repositories as follows:
```
$ ck find repo:ck-scc18
```




# Updating this workflow and dependencies

You can update all CK components (including CK framework if you installed it from GitHub) 
at any time as follows:
```
$ ck pull all --kernel
```

If you want to re-detect and re-install all software after updating CK, 
just remove the CK environment as follows:
```
$ ck clean env:*
```

You can turn off interactive mode by adding '-f' flag:

```
$ ck clean env:* -f
```



# Testing SeisSol proxy application via CK

Now you can try to automatically build and run a simple 1-node 
SeisSol proxy application to understand how portable CK program workflow works
(select "seissol-proxy" from the list of available command lines):

```
$ ck run program:seissol-proxy
```

CK concept of [portable workflows](https://github.com/ctuning/ck/wiki/Portable-workflows) 
is to let users describe software dependencies (libraries, frameworks, data sets, models)
required to build and run their applications using simple semantic tags and version ranges. 
See example of such dependencies in this 
[CK meta.json file](https://github.com/ctuning/ck-scc18/blob/master/program/seissol-proxy/.cm/meta.json#L20) 
for the above program workflow.

CK will then attempt to automatically detect all dependencies 
using [shared CK software plugins](http://cKnowledge.org/shared-soft-detection-plugins.html)
and performing an exhaustive search in system and user directories. 
Whenever multiple acceptable versions of a given dependency are found,
CK will ask you to choose which one to use. 
Based on your selection, CK will then register this version 
in the CK "local" repository  (CK scratch pad) using "env" entry,
and will create a simple batch "env.sh" file with pre-set PATH, LD_LIBRARY_PATH 
and other environment variables.

You can see all detected and registered dependencies as follows:

```
$ ck show env
```

You can also prune this search using semantic tags:
```
$ ck show env --tags=compiler
```

Next time you run the same workflow, CK will attempt to resolve dependencies using "env" entries
instead of searching in system and user paths. 
Furthermore, other CK workflows can also reuse the same dependencies.

The pros of such approach is that you can automatically 
adapt your workflow to any environment. 
This is particularly important for research workflows which should
be able to run on continuously evolving software and hardware.

*However the cons is that such workflows may be prepared 
with some untested dependencies and thus fail. 
In such case, the CK concept is to let the community
collaboratively improve such shared workflows and all related components
in spirit of Wikipedia and similar to any agile development in open source projects.*

For example, our LLNL colleagues noticed some unexpected behavior in the python detection
plugin and opened this [https://github.com/ctuning/ck-env/issues/85](ticket) 
which we collaboratively resolved shortly afterwords.

Furthermore, you can use [Spack](http://spack.io) and [EasyBuild](https://easybuild.readthedocs.io) 
to pre-install software dependencies on your platform. You can then force 
CK to search for software dependencies only in specific paths as follows:

```
$ ck set kernel var.soft_search_dirs="{path1 to already installed dependencies},{path2}..."
```

Finally, if required software is still not found, CK will attempt to automatically
install missing software via [CK packages](http://cKnowledge.org/shared-packages.html)
which are just wrappers with a unified API to other build tools and package managers 
including [spack](https://spack.io), [easybuild](https://easybuild.readthedocs.io/en/latest/), 
make, cmake, scons, etc.

For example, see the [meta.json](https://github.com/ctuning/ck-scc18/blob/master/package/lib-seissol-scc18-proxy/.cm/meta.json) 
of the SeisSol Proxy Library with other [software sub-dependencies](https://github.com/ctuning/ck-scc18/blob/master/package/lib-seissol-scc18-proxy/.cm/meta.json#L26).

If you encounter any problems during building and fix the, you can just restart 
the same workflow until it detects or rebuilds all dependencies and runs this code:
```
$ ck run program:seissol-proxy
```

You can also customize the execution of the proxy app as follows:
```
$ ck run program:seissol-proxy --cmd_key=seissol-proxy \
                               --env.CELLS={number of cells} \
                               --env.TIMESTEP={time step} \
                               --env.KERNELS={all|local|neigh|ader|localwoader|neigh_dr|godunov_dr}
```

**If you still experience troubles or don't understand something,
do not hesitate to open tickets or get in touch with the CK
community using this [public Google group](https://groups.google.com/forum/#!forum/collective-knowledge)!**











# Installing SeisSol proxy library manually

When troubleshooting workflows, you may want to install dependencies manually.
For example, you can install SeisSol proxy application using CK package
before running workflows as follows:


```
$ ck install package:lib-seissol-proxy-scc18 --reuse_deps
```

You can also restart installation without downloading this library as follows:
```
$ ck install package:lib-seissol-proxy-scc18 --reuse_deps --rebuild
```

After you manage to successfully install it, you can run the workflow:
```
ck run program:seissol-proxy
```

Note that by default we use OpenMPI and older versions of other dependencies 
which do not give you the best performance but serve more as 
a stable proof-of-concept of experiment automation. 

Our future work includes adding dependencies and optimization parameters 
to obtain the best performance across different supercomputers 
based on SCC18 submissions.








# Preparing and running SeisSol MPI workflow

## Installing and parameterizing SeisSol library

Since MPI version of SeisSol requires [more dependencies](https://github.com/ctuning/ck-scc18/blob/master/package/lib-seissol-scc18/.cm/meta.json#L26) 
and parameterization, we suggest you to install and parameterize this library via CK as follows:

```
$ ck install package:lib-seissol-scc18 --reuse_deps \
             --env.CK_SEISSOL_TARGET_ARCH={d|s}{noarch|wsm|snb|knc|hsw|knl} \
             --env.CK_SEISSOL_COMPILE_MODE={release|debug} \
             --env.CK_SEISSOL_ORDER=6 \
             --env.CK_SEISSOL_LOG_LEVEL=error \
             --env.CK_SEISSOL_LOG_LEVEL0=info
```

or to install it with default values:
```
$ ck install package:lib-seissol-scc18 --reuse_deps
```

* CK_SEISSOL_TARGET_ARCH=dsnb
* CK_SEISSOL_COMPILE_MODE=release

You can also install several libraries with different parameters at the same time. 
Just add --extra_version flag with some identifier to the above command line such as:
```
$ ck install package:lib-seissol-scc18 --reuse_deps \
             --env.CK_SEISSOL_COMPILE_MODE=debug \
             --env.CK_SEISSOL_ORDER=4 \
             --extra_version=my-debug-cfg-order-4
```






## Running SeisSol MPI

You can now try to run SeisSol program (see related [CK entry](https://github.com/ctuning/ck-scc18/tree/master/program/seissol-netcdf)). 
If you don't use any batch system, you can run it via CK as follows:

```
$ ck run program:seissol-netcdf --cmd_key=mpi \
             --env.MPI_NUM_PROCESSES={number of processes (must be multiple of 20 when used with the default data set)} \
             --env.OMP_NUM_THREADS={number of OpenMP threads}
```

Note that CK will automatically download a CK dataset package 
"dataset-seissol-sumatra-andaman-2004" from Zenodo 
which requires around 700MB of free space:
* [CK meta.json for this package](https://github.com/ctuning/ck-scc18/blob/master/package/dataset-seissol-sumatra-andaman-2004/.cm/meta.json)
* [install script](https://github.com/ctuning/ck-scc18/blob/master/package/dataset-seissol-sumatra-andaman-2004/install.sh)

You may need the following information about this mesh when customizing SeisSol execution:

```
fursin@velociti:~/CK/ck-scc18/program/seissol-netcdf/tmp$ /home/fursin/CK/local/env/6c8d46509d02e704/install/bin/ncdump -h 1003_topo30sec_wSplays_sim5_pumgenSM2.dtc1-v2-suma.20.nc

netcdf \1003_topo30sec_wSplays_sim5_pumgenSM2.dtc1-v2-suma.20 {
dimensions:
        dimension = 3 ;
        partitions = 20 ;
        elements = 263993 ;
        element_sides = 4 ;
        element_vertices = 4 ;
        vertices = 48428 ;
        boundaries = 11 ;
        boundary_elements = 2416 ;
variables:
        int element_size(partitions) ;
        int element_vertices(partitions, elements, element_vertices) ;
        int element_neighbors(partitions, elements, element_sides) ;
        int element_boundaries(partitions, elements, element_sides) ;
        int element_neighbor_sides(partitions, elements, element_sides) ;
        int element_side_orientations(partitions, elements, element_sides) ;
        int element_neighbor_ranks(partitions, elements, element_sides) ;
        int element_mpi_indices(partitions, elements, element_sides) ;
        int element_group(partitions, elements) ;
        int vertex_size(partitions) ;
        double vertex_coordinates(partitions, vertices, dimension) ;
        int boundary_size(partitions) ;
        int boundary_element_size(partitions, boundaries) ;
        int boundary_element_rank(partitions, boundaries) ;
        int boundary_element_localids(partitions, boundaries, boundary_elements) ;
}
```

Note, that CK will create a tmp directory in the "program:seissol-netcdf" entry and will record SeisSol outputs and checkpoints there. You can find this directory as follows:
```
$ ck find program:seissol-netcdf
$ cd `ck find program:seissol-netcdf`/tmp
```

Furthermore, CK will compare the output with the reference results from the published paper using the following plugin:
* https://github.com/ctuning/ck-scc18/blob/master/program/seissol-netcdf/ck_print_job_log.py#L9





## Running SeisSol MPI with a small data set

Before running long simulations, you may want to test the workflow. You can do so by limiting simulation time as follows:
```
$ ck run program:seissol-netcdf --cmd_key=mpi \
         --env.MPI_NUM_PROCESSES=20 \
         --env.OMP_NUM_THREADS=8 \
         --env.LIMIT_SEISSOL_TIME=0.1
```




## Using job managers

### Slurm

You can run SeisSol via Slurm as follows:

```                                         
ck run program:seissol-netcdf --cmd_key=mpi \
                                            \
              --env.JOB_MANAGER=slurm \
              --env.MPI_NUM_PROCESSES=20 \
              --env.OMP_NUM_THREADS=8 \
              --env.SBATCH_NODES=20 \
              --env.SBATCH_TIME="00:05:00" \
              --env.SBATCH_MEM="100000" \
                                           \
              --env.LIMIT_SEISSOL_TIME=0.1 \
                                           \
              --env.MPI_NUM_PROCESSES=20 \
              --env.OMP_NUM_THREADS=8
```

Extra parameters:
* SBATCH_JOB_NAME (default "ck-scc18")
* SBATCH_TIME (default "00:05:00")
* SBATCH_NODES" (default 20)
* SBATCH_NTASKS_PER_CORE (default 1)
* SBATCH_NTASKS_PER_NODE (default 1)
* SBATCH_CPU_PER_TASK (default 1)
* SBATCH_PARTITION (default "normal")
* SBATCH_CONSTRAINT (default "mc")
* SBATCH_MEM (default 100000) - memory limit per node in MB


Add flag --clean to clean all SeisSol outputs and checkpoints 
(it removes "tmp" directory)!


You can then check the latest status of your job:
```
$ ck run program:seissol-netcdf --cmd_key=print-last-job-status
```

Finally, you can check the log of the last job:
```
$ ck run program:seissol-netcdf --cmd_key=print-last-job-log-and-validate-results
```



### Flux

TBD






# Customizing SeisSol workflow


## Using different MPI libraries

You can install a stable OpenMPI package via CK:

```
$ ck install package:lib-openmpi-1.10.3-universal
```

You can also detect and register other MPI libraries as follows:
```
$ ck detect soft:lib.mpi
```
If required MPI library is in an unusual path, you can help CK detect it by providing a search path as follows:
```
$ ck detect soft:lib.mpi --search_dirs={path to MPI installation}
```

Next time you build SeisSol package, CK will ask you which MPI library to use:
```
$ ck install package:lib-seissol-scc18 --reuse_deps
```


## Using Intel compilers and MPI

Note that you need to use Intel compilers and Intel MPI at the same time!
We managed to compile and run SeisSol using 2017 and 2018 versions, 
but encountered some run-time errors with 2019 version!

### Detecting multiple Intel compilers

If you would like to use Intel compilers in the CK program workflows, but did not
yet install them, you can first download them from [here](https://software.intel.com/en-us/intel-compilers).
You can then automatically detect and register them via CK as follows:

```
$ ck detect soft --tags=compiler,icc
```

Note that if Intel compiler was not automatically found, you can provide a path to Intel installation as follows:
```
$ ck detect soft --tags=compiler,icc --search_dirs={INSTALLATION_PATH}
```

If automatic detection is too slow (on NFS), use the following command:
```
$ ck detect soft --tags=compiler,icc --full_path={full path to compilervars.sh}
```
### Detecting Intel MPI library

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




## Using stable dependencies

The main concept of CK is to automatically detect already installed 
dependencies for a given workflow to [automatically adapt it](https://github.com/ctuning/ck/wiki/Portable-workflows)
to evolving and latest environments on diverse user machines!

While very flexible, such approach may sometimes result 
in selecting inappropriate and incompatible dependencies.
In such case, we would also like to be able to pre-install
and use stable (validated) dependencies. This can be done via 
[spack](https://spack.io) and [EasyBuild](https://easybuild.readthedocs.io).





### Installing dependencies via Spack

CK allows you to use (stable) packages installed by [spack](https://spack.io)
to build and customize SeisSol via CK. 

If you already use spack, you can install required dependencies as follows:
```
$ spack install openmpi@1.10.7 %gcc
$ spack install netcdf@4.4.1 %gcc +mpi +dap -pic -shared ^openmpi@1.10.7 ^hdf5@1.10.4 +mpi +fortran -shared -pic
```

You can then use CK software detection plugins to register these packages for CK workflows:
```
$ ck detect soft:lib.mpi --extra_tags=vspack --extra_name="(spack)" --search_dir={PATH TO spack packages}
$ ck detect soft:lib.hdf5.static --extra_tags=vparallel,vmpi,vspack --extra_name="(spack)" --search_dir={PATH TO spack packages}
$ ck detect soft:lib.netcdf --extra_tags=vspack --extra_name="(spack)" --search_dir={PATH TO spack packages}
```

You can also update the following CK kernel variable to avoid specifying --search_dir all the time:
```
$ ck set kernel var.soft_search_dirs="{PATH to spack packages}"
```

You can then rebuild SeisSol package as before while just selecting new spack packages.

We also provided sample scripts to install spack with dependencies needed by SeisSol,
and then automatically detect them by CK to be used in the program workflow.
You can find them using the following command:
```
$ cd `ck find script:install-seissol-deps-via-spack`
```

It has 2 scripts:
* ./install-deps.sh (installing spack and deps)
* ./detect-deps.sh (registering spack packages in CK)

Note that this is an experimental functionality!
                                                 


### Installing dependencies via EasyBuild

We also provided a way to reuse dependencies installed via [EasyBuild](https://easybuild.readthedocs.io).

If you have packages installed by EasyBuild such as GCC, you can reuse them 
in a similar way as described in previous sub-section:

```
$ ck detect soft:compiler.gcc --extra_tags=veasybuild --extra_name="(easybuild)" --search_dir={PATH TO EasyBuild packages}
$ ck detect soft:lib.mpi --extra_tags=veasybuild --extra_name="(easybuild)" --search_dir={PATH TO EasyBuild packages}
$ ck detect soft:lib.hdf5.static --extra_tags=vparallel,vmpi,veasybuild --extra_name="(easybuild)" --search_dir={PATH TO EasyBuild packages}
$ ck detect soft:lib.netcdf --extra_tags=veasybuild --extra_name="(easybuild)" --search_dir={PATH TO EasyBuild packages}
```

We successfully recompiled and run SeisSol using GCC 6.4.0 from EasyBuild package installed on "Piz Daint" 
using [EasyBuild installation notes](https://easybuild.readthedocs.io/en/latest/Installation.html) as follows:

```
$ export EASYBUILD_PREFIX={PATH where EasyBuild will be installed}

$ wget https://raw.githubusercontent.com/easybuilders/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py

$ python bootstrap_eb.py $EASYBUILD_PREFIX

$ export EASYBUILD_MODULES_TOOL=EnvironmentModulesC

$ module use $EASYBUILD_PREFIX/modules/all

$ module load EasyBuild

$ eb --module-syntax=Tcl foss-2018a.eb --robot --ignore-osdeps

$ ck detect soft:compiler.gcc --extra_tags=veasybuild --extra_name="(easybuild)" --search_dir=${EASYBUILD_PREFIX}/software
```

We also provided sample scripts to install EasyBuild and then automatically 
detect GCC by CK to be used in the program workflow.
You can find them using the following command:
```
$ cd `ck find script:install-seissol-deps-via-eb`
```

It has 2 scripts:
* ./install-deps.sh (installing EasyBuild and GCC)
* ./detect-deps.sh (registering EasyBuild GCC in CK)

Note that this is an experimental functionality!







## Using different platforms to run SeisSol

### Using "SuperMUC Phase 2" platform

```
$ ck run program:seissol-netcdf --cmd_key=mpi --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=54 --env.KMP_AFFINITY="compact,granularity=thread"
```

### Using "Shaheen II" platform

```
$ ck run program:seissol-netcdf --cmd_key=mpi --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=62 --env.KMP_AFFINITY="compact,granularity=thread"
```

### Using "Cori" platform

```
$ ck run program:seissol-netcdf --cmd_key=mpi --env.MPI_NUM_PROCESSES=<<processes>> --env.OMP_NUM_THREADS=65 --env.KMP_AFFINITY="proclist =[2-66],explicit,granularity=thread"
```

### Using "Piz Daint" platform

We managed to compile and run SeisSol (SCC18 branch) via CK but we did not yet optimize it.



## Changing other parameters

You can update the following parameters from bash

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





## Running SeisSol binary without CK
You can also try to manually run SeisSol binary using CK virtual environment as follows:

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





## Creating a self-contained snapshot of this workflow


You can create a snapshot of this workflow with all dependencies as follows:
```
$ ck snapshot artifact --repo=ck-scc18
```

This command will create a self-contained zip file with this repository, 
all CK sub-repositories, CK framework, and a few environment scripts 
allowing you to share your stable workflow with others.

Further details:
* [Preparing CK snapshots](https://github.com/ctuning/ck/wiki/Adding-new-workflows#preparing-ck-artifact-pack-for-digital-libraries)
* [Preparing CK docker images](https://github.com/ctuning/ck/wiki/Adding-new-workflows#preparing-docker-image)
* [Sharing CK workflows via Digital Libraries along with publications](https://dl.acm.org/reproducibility.cfm)






## Adding new workflows and components

Please follow this [guide](https://github.com/ctuning/ck/wiki/Adding-new-workflows) (will be updated in Q1 2019)
and feel free to get in touch with the [CK community](https://github.com/ctuning/ck/wiki/Contacts)!








# Contacting the CK community

If you still encounter problems, please feel free to get in touch with the 
[CK community](https://github.com/ctuning/ck/wiki/Contacts) and we will help you fix them. 
You feedback is very important since the whole point of CK is to continuously and collaboratively 
improve all shared research workflows and components thus gradually improving 
their stability and reproducibility across diverse platforms and environments!




# Acknowledgments

We would like to thank colleagues from TUM, LLNL and UGent for very productive discussions and feedback.
We are also thankful to [CSCS](https://www.cscs.ch) for providing resources to test this CK workflow.





# Future work

* LLNL+dividiti: automate execution of SeisSol MPI via [Flux](https://github.com/flux-framework/flux-core)
* UGent+dividiti: check installation of dependencies via [easybuild](https://easybuild.readthedocs.io/en/latest)
* dividiti (currently overbooked - need to find resources):
  * add public [CK scoreboard](http://cKnowledge.org/repo) to exchange results
  * automatically generate reproducible article based on [this CK example](http://cKnowledge.org/rpi-crowd-tuning)
  * build and run latest SeisSol version with the new mesh structure and data sets via [ck-graph-analytics](https://github.com/ctuning/ck-graph-analytics) repository
  * improve CK documentation with all APIs and a better guide for contributors
* Test automatic generation of a reproducible article via CK based on this [example](http://cKnowledge.org/rpi-crowd-tuning)
* Add optimized versions from SCC18 participants
