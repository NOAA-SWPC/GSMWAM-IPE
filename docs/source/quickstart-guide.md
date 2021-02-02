# Building & Running WAM-IPE

## Obtaining the source code

The source code for WAM-IPE utilizes Git submodules, which need
to be checked out in addition to the code in the main repository. The
easiest way to do that is with the `--recursive` flag when cloning the
repository.

For example, for the **default branch**

```{code-block} bash
git clone --recursive https://github.com/CU-SWQU/GSMWAM-IPE.git
```

for a feature branch you want called **my_feature**,

```{code-block} bash
git clone -b my_feature --recursive https://github.com/CU-SWQU/GSMWAM-IPE.git
```

## Building the models

The model is compiled and built with the NEMS app builder. To select different
build and compile options, you can specify a different application with
the `app=` option to make.

For example, to build the **Coupled WAM-IPE** model the following make command would be used.

```{code-block} bash
cd GSMWAM-IPE/NEMS
gmake -j8 app=coupledWAM_IPE build
```

If you want to include **SWIO** output, you can add that component to the `app=` call.

```{code-block} bash
gmake -j8 app=coupledWAM_IPE_SWIO build
```

To build standalone WAM (without IPE).

```{code-block} bash
gmake -j8 app=standaloneWAM build
```

The instructions for running standalone IPE can be found in {ref}`building IPE <ipe_build>` section.

## Cleaning and rebuilding the project

If you make changes to source code or want to change configurations, you may need to clean and
rebuild the NEMS components. To do this, you need to specify the component you want in
the `app=` command line argument.

```{code-block} bash
gmake -j8 app=standaloneWAM clean
gmake -j8 app=standaloneWAM distclean
```

You may also clean/distclean individual components by adding the `_<COMPONENT>` suffix to the Makefile target.
For instance, to distclean WAM before rebuilding GSMWAM-IPE, you may type:

```{code-block} bash
gmake -j8 app=coupledWAM_IPE distclean_WAM
```

## Working with submodules

Submodules are Git repositories nested inside (or linked to) a parent repository at a given commit (SHA).

When switching to a different GSMWAM-IPE branch with `git checkout` make sure to update all included submodules. For example:

```{code-block} bash
cd GSMWAM-IPE
git checkout my_feature
git submodule update --recursive
```

Note that when cloning a repository that includes submodules, or checking out a given branch/revision, Git checks out each submodule in a '**detached HEAD**' state. This is because a submodule points to a commit (not a branch), and that commit may belong to multiple branches. If you commit changes within a submodule in a 'detached HEAD' state and try to push them to the remote repository, you will get the following error message:

```{code-block} bash
fatal: You are not currently on a branch.
To push the history leading to the current (detached HEAD)
state now, use

    git push origin HEAD:<name-of-remote-branch>
```

Therefore, make sure to check the submodule's status using `git status` **_before_** starting to work in a submodule. If the submodule is in a 'detached HEAD' state, Git will output a message like the one reported below:

```{code-block} bash
$ git status
* (HEAD detached at 4cc1840)
```

You should then checkout your corresponding work branch before proceeding. To find out which branch a given commit belongs to, you may use the following command:

```{code-block} bash
git branch -a --contains 4cc1840
```

which returns a list of all branches containing the commit:

```{code-block} bash
* (HEAD detached from 4cc1840)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/master
  remotes/origin/netcdf_output
```

If you accidentally added a number of commits to your submodule repository before realizing it was in 'detached HEAD' state, you may either:

1. create a temporary branch (_e.g._ `temp`), then checkout your feature branch and merge the temporary branch into it: 

    ```{code-block} bash
    git checkout -b temp       # (your commits are now saved in branch 'temp')
    git checkout my_feature    # (checkout your proper work branch)
    git merge temp             # (merge your commits into your work branch)
    git branch -d temp         # (delete the temporary branch)
    ```

2. or use `git cherry-pick` to individually select those commits (_e.g._ `17de781`) you want to transfer to your feature branch (_e.g._ `my_feature`)

    ```{code-block} bash
    git log                    # (list your latest commits)
    git checkout my_feature
    git cherry-pick 17de781    # (add commit 17de781 to your work branch)
    ```

## Debugging

GSMWAM-IPE and its components can be built in debug mode by adding the following component-specific settings to the `*.appBuilder` files for NEMS, IPE, and WAM, respectively.

```{code-block} bash
NEMS_BUILDOPT=DEBUG=Y
IPE_MAKEOPT=DEBUG=Y
WAM_MAKEOPT=DEBUG=Y
```

For instance, to build the coupled WAM-IPE system in debug mode, the `coupledWAM_IPE.appBuilder` file should look as follows:

```{code-block} bash
# Coupled WAM-IPE
#
## NEMS Application Builder file

COMPONENTS=( WAM IPE )

NEMS_BUILDOPT=DEBUG=Y
IPE_MAKEOPT=DEBUG=Y
WAM_MAKEOPT=DEBUG=Y
```

## Running the model

The current WAM-IPE scripts can be used to run GSMWAM-IPE coupled and standalone WAM or IPE.

A default script for NSF's Cheyenne supercomputer exists such that you can `./submit.sh cheyenne.config` in `scripts/compsets` and it will create a job.

```{note}
The SWPC mediator _only_ supports ESMF coupling fields whose data is distributed over _one_ Decomposition Element (DE) on the local Persistent Execution Thread (PET). This means that data associated with each imported and exported field should be distributed over the mediator's MPI tasks in a 1:1 fashion. This is ensured by setting **NPROCMED** at least equal to the maximum between **NPROCIPE** and **NPROCWAM** in your compset script before running a coupled simulation.
```

1. To obtain, compile, and run the WAM-IPE, please follow the following steps on Cheyenne.

    ```{code-block} bash
    git clone --recursive https://github.com/CU-SWQU/GSMWAM-IPE.git
    cd GSMWAM-IPE/NEMS
    gmake -j8 app=coupledWAM_IPE_SWIO build
    cd ..scripts/compsets
    ./submit.sh cheyenne.config
    ```

2. To change the NetCDF model output parameters, please modify the swio.ipe.rc and swio.wam.rc files under GSMWAM-IPE/scripts/compsets/parm folder.

3. To change the output cadence, please modify the file swio.config under GSMWAM-IPE/scripts/compsets/config. The numbers in the file are in seconds.

## SWIO output cadence

1. In 'GSMWAM-IPE/scripts/compsets/*.config':

   Reset the value of the following runSeq variables,
   > export IO_CADENCE=cadence_desired      (in seconds, for IPE output )
   > export AIO_CADENCE=cadence_desired    (in seconds, for WAM output)

2. In 'GSMWAM-IPE/scripts/compsets/parm/nems.configure.WAM-IPE_io':

In part of **Run Sequence**, change the time cadence value (in seconds) into the desired ones, the following is a code example for that:

```{code-block} bash
    runSeq::
      @180.0
        ATM -> MED :remapMethod=redist
        MED
        MED -> IPM :remapMethod=redist
          @60.0
            ATM
          @
        IPM
        AIO
        ATM -> AIO
        IO
        IPM -> IO
      @
    ::
```
