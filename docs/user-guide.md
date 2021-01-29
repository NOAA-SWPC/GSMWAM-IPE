##### 

##### Joseph Schoonover, Zhuxiao Li, Tzu-Wei Fang, Naomi Maruyama, George Millward

Table Of Contents
=================

> [Joseph Schoonover, Zhuxiao Li, Tzu-Wei Fang, Naomi Maruyama, George
> Millward](#joseph-schoonover-zhuxiao-li-tzu-wei-fang-naomi-maruyama-george-millward)
> 1

**[Table Of Contents](#table-of-contents) 2**

**[User Guide](#user-guide) 4**

> [Getting Started](#getting-started) 4
>
> [Model & Source Code Overview](#model-source-code-overview) 4
>
> [Source Code Dependencies](#source-code-dependencies) 4
>
> [Downloading Code](#downloading-code) 4
>
> [Downloading Input Decks](#downloading-input-decks) 4
>
> [Building IPE](#building-ipe) 6
>
> [On Theia](#on-theia) 6
>
> [Setting the model input
> parameters](#setting-the-model-input-parameters) 7
>
> [Running IPE](#running-ipe) 8
>
> [On Theia](#on-theia-1) 9

**[Developer Guide](#developer-guide) 10**

> [Development Workflow](#development-workflow) 10
>
> [Submitting Issues](#submitting-issues) 10
>
> [Branching Strategy](#branching-strategy) 10
>
> [Pull Requests](#pull-requests) 10
>
> [Model Testing](#model-testing) 11
>
> [Build Tests](#build-tests) 11
>
> [Run Tests](#run-tests) 11
>
> [WAM ( Standalone )](#wam-standalone) 11
>
> [IPE ( Standalone )](#ipe-standalone) 11
>
> [WAM-IPE](#wam-ipe) 11
>
> [Plots](#plots) 11
>
> [WAM](#wam) 12
>
> [IPE](#ipe) 12
>
> [Model output](#model-output) 14
>
> [IPE Native HDF5 files](#ipe-native-hdf5-files) 14
>
> [IPE Geographic (Post-Processed) NetCDF
> files](#ipe-geographic-post-processed-netcdf-files) 14
>
> [Baseline Files](#baseline-files) 17
>
> [Baseline File Management System](#baseline-file-management-system) 17
>
> [Procedure for establishing new Baseline
> Files](#procedure-for-establishing-new-baseline-files) 17

 

User Guide
==========

Getting Started
---------------

### Model & Source Code Overview

### Source Code Dependencies

The IPE source code makes use of both **HDF5** and **NetCDF** libraries.
Additionally, parallelism is supported using MPI (via **OpenMPI** or
**MPICH** ). In order to build and run IPE, you will need to have HDF5
and NetCDF installed on your system. For parallel builds of IPE, you
will need to have parallel HDF5 and parallel NetCDF installed.

### Downloading Code

IPE source code is currently hosted as a subdirectory of the WAM-IPE
code-base at
[[https://github.com/SWPC-IPE/WAM-IPE]{.underline}](https://github.com/SWPC-IPE/WAM-IPE)

Code can be downloaded using

  ---------------------------------------------------
  **git clone https://github.com/SWPC-IPE/WAM-IPE**
  ---------------------------------------------------

Alternatively, you can download tar-balls of [[previous
releases]{.underline}](https://github.com/SWPC-IPE/WAM-IPE/releases).

### Downloading Input Decks

IPE depends on a set of files that are needed for the accompanying
empirical models, specify the model grid, specify model runtime
parameters, and specify initial conditions. These files, along with a
description and where it is used in the source code is listed in the
table at the end of this section.

Input decks can be downloaded using the provided python script under
**WAM-IPE/IPELIB/scripts/download\_ipe-data.py**

This script uses **wget** to download data over https.

To download the data

+---------------------------------------------+
| **cd IPELIB/run**                           |
|                                             |
| **python ../scripts/download\_ipe-data.py** |
+---------------------------------------------+

**CAUTION : If you are on theia, the python script will not work.
Instead, you will need to copy files from
/scratch3/NCEPDEV/swpc/refactored\_ipe\_input\_decks/**

+----------------------------------------------------------------------+
| **cd IPELIB/run**                                                    |
|                                                                      |
| **cp /scratch3/NCEPDEV/swpc/noscrub/refactored\_ipe\_input\_decks/\* |
| ./**                                                                 |
+----------------------------------------------------------------------+

+----------------------+----------------------+----------------------+
| **File Name**        | **Description**      | **Source Code**      |
+======================+======================+======================+
| gd2qd.dat            |                      |                      |
+----------------------+----------------------+----------------------+
| global\_id           |                      |                      |
| ea\_coeff\_hflux.dat |                      |                      |
+----------------------+----------------------+----------------------+
| global\              |                      |                      |
| _idea\_wei96.cofcnts |                      |                      |
+----------------------+----------------------+----------------------+
| wei96.cofcnts        |                      |                      |
+----------------------+----------------------+----------------------+
| hwm123114.bin        | Binary file (        | msise00/hwm14.f90    |
|                      | little-endian        |                      |
|                      | containing a mix of  | S/R initqwm          |
|                      | 4-byte integers and  |                      |
|                      | double precision )   |                      |
|                      | containing data      |                      |
|                      | needed for the 2014  |                      |
|                      | Horizontal Wind      |                      |
|                      | Model                |                      |
+----------------------+----------------------+----------------------+
| dwm07b104i.dat       | Binary file (        | msise00/hwm14.f90    |
|                      | little-endian        |                      |
|                      | containing a mix of  | S/R initdwm          |
|                      | 4-byte integers and  |                      |
|                      | double precision )   |                      |
|                      | containing data      |                      |
|                      | needed for the 2014  |                      |
|                      | Disturbance Wind     |                      |
|                      | Model                |                      |
+----------------------+----------------------+----------------------+
| ionprof              | ASCII file           | IP                   |
|                      | containing values    | E\_Plasma\_Class.F90 |
|                      | used for calculating |                      |
|                      | ionization rates.    | S/R                  |
|                      |                      | Au                   |
|                      |                      | roral\_Precipitation |
+----------------------+----------------------+----------------------+
| tiros\_spectra       | ASCII file           | IP                   |
|                      | containing values    | E\_Plasma\_Class.F90 |
|                      | used for calculating |                      |
|                      | ionization rates.    | S/R                  |
|                      |                      | Au                   |
|                      |                      | roral\_Precipitation |
+----------------------+----------------------+----------------------+
| IPE\_Grid.nc         | NetCDF file          | IPE\_Grid\_Class.F90 |
|                      | containing IPE Grid  |                      |
|                      | information and      | S/R                  |
|                      | mapping weights onto | Rea                  |
|                      | geographic grid      | d\_NetCDF\_IPE\_Grid |
+----------------------+----------------------+----------------------+
| IPE.inp              | Namelist file used   | IPE\_M               |
|                      | for specifying IPE   | odel\_Parameters.F90 |
|                      | parameters,          |                      |
|                      | including timestep,  |                      |
|                      | file IO frequency,   |                      |
|                      | and forcing          |                      |
|                      | parameters.          |                      |
+----------------------+----------------------+----------------------+

### Building IPE

IPE's uses autoconf as it's make system. To build the code, execute the
following from the **IPELIB/** directory, replacing **/path/to/install**
with the path where you would like to install IPE binaries and
libraries.

+--------------------------------------------+
| **INSTALL\_DIR=/path/to/install**          |
|                                            |
| **./configure \--prefix=\${INSTALL\_DIR}** |
|                                            |
| **make install**                           |
+--------------------------------------------+

This process will create a directory **\${INSTALL\_DIR}** with **bin/**,
**lib/**, and **include/** subdirectories.

#### On Theia

**NOTE :** If you are working on Theia, you can use the provided
build\_ipe\_from\_scratch.csh script to build the code

+-------------------------------------+
| **cd IPELIB/**                      |
|                                     |
| **./build\_ipe\_from\_scratch.csh** |
+-------------------------------------+

+------------------+------------------------+------------------------+
| **Subdirectory** | Description            | Files                  |
+==================+========================+========================+
| **bin/**         | Contains binaries      | **ipe,                 |
|                  | (programs) for running | ipe\_postprocess,      |
|                  | IPE (standalone), a    | eregrid**              |
|                  | post-processor to      |                        |
|                  | generate diagnostics   |                        |
|                  | on a geographic grid,  |                        |
|                  | and a program for      |                        |
|                  | regridding electric    |                        |
|                  | field data from an     |                        |
|                  | external model         |                        |
|                  | (Geospace or OpenGGCM) |                        |
|                  | onto the IPE Grid.     |                        |
+------------------+------------------------+------------------------+
| **lib/**         | Contains library and   | **\*.a \*.o**          |
|                  | object files from the  |                        |
|                  | compilation process.   |                        |
|                  | This directory should  |                        |
|                  | be added to the linker |                        |
|                  | when coupling IPE with |                        |
|                  | another code or in     |                        |
|                  | developing additional  |                        |
|                  | tools using the IPE    |                        |
|                  | API.                   |                        |
|                  |                        |                        |
|                  | **-                    |                        |
|                  | L/\${INSTALL\_DIR}/lib |                        |
|                  | -lipe**                |                        |
+------------------+------------------------+------------------------+
| **include/**     | Contains the .mod      | **\*.mod**             |
|                  | files, generated by    |                        |
|                  | the Fortran source     |                        |
|                  | code compiliation.     |                        |
|                  | This directory should  |                        |
|                  | be passed as an        |                        |
|                  | includes directory at  |                        |
|                  | compile time for       |                        |
|                  | coupling IPE with      |                        |
|                  | another code or in     |                        |
|                  | developing additional  |                        |
|                  | tools using the IPE    |                        |
|                  | API.                   |                        |
|                  |                        |                        |
|                  | **-I/\${I              |                        |
|                  | NSTALL\_DIR}/include** |                        |
+------------------+------------------------+------------------------+

### Setting the model input parameters

Modify IPE.inp

  **Parameter Name**               **Namelist**          **Description**
  -------------------------------- --------------------- -----------------
  **NetCDF\_Grid\_File**           **SpaceManagement**   
  **NLP**                          **SpaceManagement**   
  **NMP**                          **SpaceManagement**   
  **NPTS2D**                       **SpaceManagement**   
  **NFluxTube**                    **SpaceManagement**   
  **Time\_Step**                   **TimeStepping**      
  **Start\_Time**                  **TimeStepping**      
  **End\_Time**                    **TimeStepping**      
  **Initial\_TimeStamp**           **TimeStepping**      
  **Solar\_Forcing\_Time\_Step**   **Forcing**           
  **F107\_kp\_size**               **Forcing**           
  **F107\_kp\_interval**           **Forcing**           
  **F107\_kp\_skip\_size**         **Forcing**           
  **F107\_kp\_data\_size**         **Forcing**           
  **f107**                         **Forcing**           
  **f107\_flag**                   **Forcing**           
  **f107\_81day\_avg**             **Forcing**           
  **kp**                           **Forcing**           
  **kp\_flag**                     **Forcing**           
  **kp\_1day\_avg**                **Forcing**           
  **ap**                           **Forcing**           
  **ap\_1day\_avg**                **Forcing**           
  **nhemi\_power**                 **Forcing**           
  **nhemi\_power\_index**          **Forcing**           
  **shemi\_power**                 **Forcing**           
  **shemi\_power\_index**          **Forcing**           
  **FILE\_OUTPUT\_FREQUENCY**      **FileIO**            
  **WRITE\_APEX\_NEUTRALS**        **FileIO**            

### Running IPE

To run IPE, it's important that you've [[downloaded the input decks
necessary to run IPE]{.underline}](#downloading-input-decks). The input
decks should be placed in a directory where you wish to run the IPE
source code ( e.g. WAM-IPE/IPELIB/run )

To run the code in serial, simply do

  --------------------------
  \${INSTALL\_DIR}/bin/ipe
  --------------------------

In the directory where all of the input decks are located.

To run in parallel, make sure that the appropriate MPI tools are in your
search path. Then

  ----------------------------------------
  mpirun -np 20 \${INSTALL\_DIR}/bin/ipe
  ----------------------------------------

To run the model with 20 ranks. Note that, you can change the number of
ranks to any value between 1 and 40.[^1]

#### On Theia

Underneath the IPELIB/run/ directory, batch submission scripts are
provided for running the serial and parallel versions through a PBS job
scheduler. These scripts can be modified to change the submission queue,
the wall time, and the number of ranks.

If you are on theia, you can use the provided job submission scripts to
run the code. For a parallel run

+------------------------+
| cd ipelib/run          |
|                        |
| qsub ipe\_parallel.pbs |
+------------------------+

For serial,

+----------------------+
| cd ipelib/run        |
|                      |
| qsub ipe\_serial.pbs |
+----------------------+

For testing both serial and parallel, and comparing the results

+--------------------+
| cd ipelib/run      |
|                    |
| qsub ipe\_test.pbs |
+--------------------+

 

Developer Guide
===============

Development Workflow
--------------------

Making changes to the code is executed through the following steps

1.  Document the change you want to make by [[opening an
    > issue]{.underline}](https://github.com/SWPC-IPE/WAM-IPE/issues/new).

2.  Discuss with developers and subtask issues

    a.  Potential conflicts with other ongoing work

    b.  Ideal strategies for addressing the issue

    c.  What the conditions for satisfaction[^2] are.

3.  Regularly schedule work from backlog to "to do"

When beginning work on a task,

4.  Make a feature branch off development and begin your work

5.  Perform standard runs , make standard plots, and document the
    > changes in the issue tracker to help your reviewers assess the
    > impact of your changes.

6.  Open a Pull Request, referencing the issue number(s) you were
    > working on, and respond to any concerns brought up by your Pull
    > Request reviewers.

### Submitting Issues

In general, tracking issues and tasks related to our code base is meant
to help document the changes we are making to the code, and help us plan
code changes that will have minimal conflicts amongst all of the
developers.

### Branching Strategy

### Pull Requests

To bring your changes into the common development branch

Model Testing
-------------

### Build Tests

Must compile :

-   NEMSAppBuilder : app=standalone\_gsm

-   NEMSAppBuilder : app=wam-ipe

-   IPELIB build system : run build\_ipe\_from\_scratch.csh \-- must
    > show PASS for serial and parallel builds

### Run Tests

Several sets of plots need to be created for WAM and IPE in order to
meet the science requirements and to evaluate the model performance. In
general, when there are changes to baseline files, or pull requests that
need to be approved, **10 day runs of WAM, IPE, and/or WAM-IPE** should
be conducted.

#### WAM ( Standalone )

Plots every 6 hours UT

Fixed drivers (F10.7=120, Kp=3)

Time-varying drivers

Run Dates : 2013/03/16 to 2013/03/21

#### IPE ( Standalone )

Fixed drivers (F10.7=120, Kp=3)

Time-varying drivers

Run Dates: 2013/03/16 to 2013/03/21

#### WAM-IPE 

Fixed drivers (F10.7=120, Kp=3)

Time-varying drivers

Run Dates: 2013/03/16 to 2013/03/21

### Plots

Several sets of plots need to be created for WAM and IPE in order to
meet the science requirements and to evaluate the model performance.
Domain experts evaluate the impact of source code changes by looking at
a set of plots/figures that help them make the assessment during review
of pull requests. Code is provided to generate these plots for you; it
is your job (presently) to get these plots posted to the appropriate
issue tracker and/or pull request for your reviewers.

#### WAM

  Plot                                              Plot Type
  ------------------------------------------------- --------------------
  Thermosphere temperature ( level 135 / 350 km )   Lat-Lon Map
  Global mean temperature (vs NRL-MSIS)             Vertical Profile
  Mean mass ( level 135 / 350 km)                   Lat-Lon Map
  Global mean O, O2, N2 (vs NRL-MSIS)               Vertical Profile
  Thermosphere Winds ( level 135 /350 km )          Lat-Lon Map
  Zonal mean temperature                            Lat-Pressure Level
  Zonal mean mean mass                              Lat-Pressure Level

#### IPE 

  **Plot**                                          **Range**         **Plot Type**
  ------------------------------------------------- ----------------- ---------------
  TEC ( hourly )                                    \[0, 100\]        Lat-Lon Map
  NmF2 ( hourly )                                   \[\]              Lat-Lon Map
  HmF2 ( hourly )                                   \[\]              Lat-Lon Map
  Electron Temperature ( hourly )                   \[\]              Lat-Lon Map
  Ion Temperature ( hourly )                        \[\]              Lat-Lon Map
  Electron Density ( hourly @ 300km )               \[\]              Lat-Lon Map
  Neutral Wind (U geographic) ( hourly @ 350 km )   \[-250, 250\]     Lat-Lon Map
  Neutral Wind (V geographic) ( hourly @ 350 km )   \[-200, 200\]     Lat-Lon Map
  Neutral Wind (W geographic) ( hourly @ 350 km )   0, 20\]           Lat-Lon Map
  Neutral Temperature ( hourly @ 350 km )           \[900, 1200\]     Lat-Lon Map
  Oxygen ( hourly @ 350 km )                        \[3.2, 6.0\]E14   Lat-Lon Map
  Molecular Nitrogen ( hourly @ 350 km )            \[0.4, 1.8\]E14   Lat-Lon Map

#### Leveraging our plotting script

Under the **scripts/plot** directory, we have provided a python plotting
utility, **plot.py**, and a dictionary of plots and their settings,
**plot\_settings.yaml** .

The python plotting utility is can be executed using

  ---------------------------------------------------------------
  python plot.py -i \[input directory\] -o \[output-directory\]
  ---------------------------------------------------------------

Where the input directory is the directory containing the WAM or IPE
NetCDF files and the output directory is the path where you would like
to save the plots.

The python plotting utility parses the plot\_settings.yaml file to

####  

Model output
------------

### IPE Native HDF5 files

When running the IPE driver program, HDF5 files are written that store
IPE's model state at intervals specifed by the FILE\_OUTPUT\_FREQUENCY
parameter in IPE.inp. The fields stored in the HDF5 file correspond to
the data values on the IPE Apex Grid.

### IPE Geographic (Post-Processed) NetCDF files

The IPE post-processor reads in the HDF5 files, interpolates the IPE
model state to a geographic grid ( latitude, longitude, altitude ), and
writes the interpolated fields to NetCDF files. These files have
metadata that explain what information is contained within the file.
This metadata can be reported using the ncdump utility.

For reference, a list of fields and their units are provided, as
reported from ncdump on the post-processed, geographic netcdf files

+----------------------------------------------------------------------+
| double helium(time, Z, latitude, longitude) ;                        |
|                                                                      |
| helium:long\_name = \"NeutralHelium Density\" ;                      |
|                                                                      |
| helium:units = \"kg m\^{-3}\" ;                                      |
|                                                                      |
| double oxygen(time, Z, latitude, longitude) ;                        |
|                                                                      |
| oxygen:long\_name = \"NeutralOxygen Density\" ;                      |
|                                                                      |
| oxygen:units = \"kg m\^{-3}\" ;                                      |
|                                                                      |
| double molecular\_oxygen(time, Z, latitude, longitude) ;             |
|                                                                      |
| molecular\_oxygen:long\_name = \"Neutral Molecular Oxygen Density\"  |
| ;                                                                    |
|                                                                      |
| molecular\_oxygen:units = \"kgm\^{-3}\" ;                            |
|                                                                      |
| double molecular\_nitrogen(time, Z, latitude, longitude) ;           |
|                                                                      |
| molecular\_nitrogen:long\_name = \"Neutral Molecular Nitrogen        |
| Density\" ;                                                          |
|                                                                      |
| molecular\_nitrogen:units = \"kgm\^{-3}\" ;                          |
|                                                                      |
| double nitrogen(time, Z, latitude, longitude) ;                      |
|                                                                      |
| nitrogen:long\_name = \"NeutralNitrogen Density\" ;                  |
|                                                                      |
| nitrogen:units = \"kg m\^{-3}\" ;                                    |
|                                                                      |
| double hydrogen(time, Z, latitude, longitude) ;                      |
|                                                                      |
| hydrogen:long\_name = \"NeutralHydrogen Density\" ;                  |
|                                                                      |
| hydrogen:units = \"kg m\^{-3}\" ;                                    |
|                                                                      |
| double temperature(time, Z, latitude, longitude) ;                   |
|                                                                      |
| temperature:long\_name = \"Thermosphere Temperature\" ;              |
|                                                                      |
| temperature:units = \"K\" ;                                          |
|                                                                      |
| double u(time, Z, latitude, longitude) ;                             |
|                                                                      |
| u:long\_name = \"Apex1 Velocity\" ;                                  |
|                                                                      |
| u:units = \"m s\^{-1}\" ;                                            |
|                                                                      |
| double v(time, Z, latitude, longitude) ;                             |
|                                                                      |
| v:long\_name = \"Apex2 Velocity\" ;                                  |
|                                                                      |
| v:units = \"m s\^{-1}\" ;                                            |
|                                                                      |
| double w(time, Z, latitude, longitude) ;                             |
|                                                                      |
| w:long\_name = \"Apex3 Velocity\" ;                                  |
|                                                                      |
| w:units = \"m s\^{-1}\" ;                                            |
|                                                                      |
| double phi(time, latitude, longitude) ;                              |
|                                                                      |
| phi:long\_name = \"Electric Potential\" ;                            |
|                                                                      |
| phi:units = \"\[Unknown\]\" ;                                        |
|                                                                      |
| double mhd\_phi(time, latitude, longitude) ;                         |
|                                                                      |
| mhd\_phi:long\_name = \"Electric Potential - MHD Component\" ;       |
|                                                                      |
| mhd\_phi:units = \"\[Unknown\]\" ;                                   |
|                                                                      |
| double exb\_u(time, latitude, longitude) ;                           |
|                                                                      |
| exb\_u:long\_name = \"Zonal component of ExB drift velocity\" ;      |
|                                                                      |
| exb\_u:units = \"\[Unknown\]\" ;                                     |
|                                                                      |
| double exb\_v(time, latitude, longitude) ;                           |
|                                                                      |
| exb\_v:long\_name = \"Meridional component of ExB drift velocity\" ; |
|                                                                      |
| exb\_v:units = \"\[Unknown\]\" ;                                     |
|                                                                      |
| double hc(time, latitude, longitude) ;                               |
|                                                                      |
| hc:long\_name = \"Hall Conductivity\" ;                              |
|                                                                      |
| hc:units = \"\[Unknown\]\" ;                                         |
|                                                                      |
| double pc(time, latitude, longitude) ;                               |
|                                                                      |
| pc:long\_name = \"Pedersen Conductivity\" ;                          |
|                                                                      |
| pc:units = \"\[Unknown\]\" ;                                         |
|                                                                      |
| double bc(time, latitude, longitude) ;                               |
|                                                                      |
| bc:long\_name = \"Magnetic Field Aligned Conductivity\" ;            |
|                                                                      |
| bc:units = \"\[Unknown\]\" ;                                         |
|                                                                      |
| double O+(time, Z, latitude, longitude) ;                            |
|                                                                      |
| O+:long\_name = \"Atomic oxygen ion number density (ground state)\"  |
| ;                                                                    |
|                                                                      |
| O+:units = \" m\^{-3}\" ;                                            |
|                                                                      |
| double H+(time, Z, latitude, longitude) ;                            |
|                                                                      |
| H+:long\_name = \"Hydrogen ion number density\" ;                    |
|                                                                      |
| H+:units = \" m\^{-3}\" ;                                            |
|                                                                      |
| double He+(time, Z, latitude, longitude) ;                           |
|                                                                      |
| He+:long\_name = \"Helium ion number density\" ;                     |
|                                                                      |
| He+:units = \" m\^{-3}\" ;                                           |
|                                                                      |
| double N+(time, Z, latitude, longitude) ;                            |
|                                                                      |
| N+:long\_name = \"Nitrogen ion number density\" ;                    |
|                                                                      |
| N+:units = \" m\^{-3}\" ;                                            |
|                                                                      |
| double NO+(time, Z, latitude, longitude) ;                           |
|                                                                      |
| NO+:long\_name = \"Nitrosonium ion number density\" ;                |
|                                                                      |
| NO+:units = \" m\^{-3}\" ;                                           |
|                                                                      |
| double O2+(time, Z, latitude, longitude) ;                           |
|                                                                      |
| O2+:long\_name = \"Molecular Oxygen ion number density\" ;           |
|                                                                      |
| O2+:units = \" m\^{-3}\" ;                                           |
|                                                                      |
| double N2+(time, Z, latitude, longitude) ;                           |
|                                                                      |
| N2+:long\_name = \"Molecular Nitrogen ion number density\" ;         |
|                                                                      |
| N2+:units = \" m\^{-3}\" ;                                           |
|                                                                      |
| double O+\\(2D\\)(time, Z, latitude, longitude) ;                    |
|                                                                      |
| O+\\(2D\\):long\_name = \"Atomic oxygen ion number density (first    |
| excited state)\" ;                                                   |
|                                                                      |
| O+\\(2D\\):units = \" m\^{-3}\" ;                                    |
|                                                                      |
| double O+\\(2P\\)(time, Z, latitude, longitude) ;                    |
|                                                                      |
| O+\\(2P\\):long\_name = \"Atomic oxygen ion number density (second   |
| excited state)\" ;                                                   |
|                                                                      |
| O+\\(2P\\):units = \" m\^{-3}\" ;                                    |
|                                                                      |
| double ion\_temp(time, Z, latitude, longitude) ;                     |
|                                                                      |
| ion\_temp:long\_name = \"Ion temperature\" ;                         |
|                                                                      |
| ion\_temp:units = \"K\" ;                                            |
|                                                                      |
| double e(time, Z, latitude, longitude) ;                             |
|                                                                      |
| e:long\_name = \"Electron number density\" ;                         |
|                                                                      |
| e:units = \" m\^{-3}\" ;                                             |
|                                                                      |
| double aur\_precip(time, Z, latitude, longitude) ;                   |
|                                                                      |
| aur\_precip:long\_name = \"Total Ionization Rate from Auroral        |
| Precipitation\" ;                                                    |
|                                                                      |
| aur\_precip:units = \"\[Unknown\]\" ;                                |
|                                                                      |
| double O+\_precip(time, Z, latitude, longitude) ;                    |
|                                                                      |
| O+\_precip:long\_name = \"Oxygen Ionization Rate from Auroral        |
| Precipitation\" ;                                                    |
|                                                                      |
| O+\_precip:units = \"\[Unknown\]\" ;                                 |
|                                                                      |
| double O2+\_precip(time, Z, latitude, longitude) ;                   |
|                                                                      |
| O2+\_precip:long\_name = \"Molecular Oxygen Ionization Rate from     |
| Auroral Precipitation\" ;                                            |
|                                                                      |
| O2+\_precip:units = \"\[Unknown\]\" ;                                |
|                                                                      |
| double N2+\_precip(time, Z, latitude, longitude) ;                   |
|                                                                      |
| N2+\_precip:long\_name = \"Molecular Nitrogen Ionization Rate from   |
| Auroral Precipitation\" ;                                            |
|                                                                      |
| N2+\_precip:units = \"\[Unknown\]\" ;                                |
+----------------------------------------------------------------------+

 

Baseline Files
--------------

Baseline files are files that are associated with an accepted version
release of the WAM-IPE code base. These files are used to compare with
subsequent versions of the model. They help assess impacts of changes in
the model dynamical cores or physics packages. Additionally, they can be
used to compare against future versions that should not impact model
output.

This section documents the tools used for storing and updating baseline
files in addition to the procedures for establishing new baseline files.

### Baseline File Management System

### Procedure for establishing new Baseline Files

[^1]: 

[^2]: Conditions for satisfaction refer to the criteria we believe will
    be sufficient to close the issue and merge in your changes.
