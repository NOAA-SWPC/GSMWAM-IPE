# Developer Guide

```{contents}
:depth: 2
:local:
```

## Development Workflow

Making changes to the code is executed through the following steps

1. Document the change you want to make by [opening an issue](https://github.com/CU-SWQU/GSMWAM-IPE/issues/new).

    In general, tracking issues and tasks related to our code base is meant
    to help document the changes we are making to the code, and help us plan
    code changes that will have minimal conflicts amongst all of the
    developers.

2. Discuss with developers and subtask issues

    a.  Potential conflicts with other ongoing work

    b.  Ideal strategies for addressing the issue

    c.  What the conditions for satisfaction are

3. Regularly schedule work from backlog to "to do"

4. Make a feature branch off development and begin your work

5. Perform standard runs , make standard plots, and document the
    changes in the issue tracker to help your reviewers assess the
    impact of your changes.

6. Open a Pull Request, referencing the issue number(s) you were
    working on, and respond to any concerns brought up by your Pull
    Request reviewers.

## Testing

### Build Tests

The following items must compile,

- NEMSAppBuilder : app=standalone_gsm
- NEMSAppBuilder : app=wam-ipe
- IPELIB build system : run build_ipe_from_scratch.csh -- must show PASS for serial and parallel builds

### Run Tests

Several sets of plots need to be created for WAM and IPE in order to meet the science requirements and to evaluate the model performance. In general, when there are changes to baseline files, or pull requests that need to be approved, 10 day runs of WAM, IPE, and/or WAM-IPE should be conducted.

WAM, IPE, and WAM-IPE should be run with

1. Fixed drivers (F10.7=120, Kp=3)
2. Time-varying drivers
3. Run dates (2013/03/16 to 2013/03/21)

additionally, WAM runs should output plots every 6 hours UT.

### Plots

Several sets of plots need to be created for WAM and IPE in order to meet the science requirements and to evaluate the model performance. Domain experts evaluate the impact of source code changes by looking at a set of plots/figures that help them make the assessment during review of pull requests. Code is provided to generate these plots for you; it is your job (presently) to get these plots posted to the appropriate issue tracker and/or pull request for your reviewers.

Under the **scripts/plot** directory, we have provided a python plotting utility, **plot.py**, and a dictionary of plots and their settings, **plot_settings.yaml**.

The python plotting utility can be executed using

```{code-block} bash
python plot.py -i [input directory] -o [output-directory]
```

where the input directory is the directory containing the WAM or IPE NetCDF files and the output directory is the path where you would like to save the plots. The python plotting utility parses the **plot_settings.yaml** file to generate the proper plots.

#### WAM

```{list-table}
:header-rows: 1

* - Plot
  - Plot Type
* - Thermosphere temperature (level 135 / 350 km)
  - Lat-Lon Map
* - Global mean temperature (vs NRL-MSIS)
  - Vertical Profile
* - Mean mass (level 135 / 350 km)
  - Lat-Lon Map
* - Global mean O, O2, N2 (vs NRL-MSIS)
  - Vertical Profile
* - Thermosphere Winds (level 135 /350 km)
  - Lat-Lon Map
* - Zonal mean temperature
  - Lat-Pressure Level
* - Zonal mean mean mass
  - Lat-Pressure Level
```

#### IPE

```{list-table}
:header-rows: 1

* - Plot
  - Range
  - Plot Type
* - TEC (hourly)
  - [0, 100]
  - Lat-Lon Map
* - NmF2 (hourly)
  - []
  - Lat-Lon Map
* - HmF2 (hourly)
  - []
  - Lat-Lon Map
* - Electron Temperature (hourly)
  - []
  - Lat-Lon Map
* - Ion Temperature (hourly)
  - []
  - Lat-Lon Map
* - Electron Density (hourly @ 300km)
  - []
  - Lat-Lon Map
* - Neutral Wind (U geographic) (hourly @ 350 km)
  - [-250, 250]
  - Lat-Lon Map
* - Neutral Wind (V geographic) (hourly @ 350 km)
  - [-200, 200]
  - Lat-Lon Map
* - Neutral Wind (W geographic) (hourly @ 350 km)
  - [0, 20]
  - Lat-Lon Map
* - Neutral Temperature (hourly @ 350 km)
  - [900, 1200]
  - Lat-Lon Map
* - Oxygen (hourly @ 350 km)
  - [3.2, 6.0]E14
  - Lat-Lon Map
* - Molecular Nitrogen  (hourly @ 350 km)
  - [0.4, 1.8]E14
  - Lat-Lon Map
```

### Baseline Files

Baseline files are files that are associated with an accepted version release of the WAM-IPE code base. These files are used to compare with subsequent versions of the model. They help assess impacts of changes in the model dynamical cores or physics packages. Additionally, they can be used to compare against future versions that should not impact model output.

This section documents the tools used for storing and updating baseline files in addition to the procedures for establishing new baseline files.

#### Baseline File Management System

#### Procedure for establishing new Baseline Files

## Model Output

### IPE Native HDF5 files

When running the IPE driver program, HDF5 files are written that store IPE’s model state at intervals specifed by the *FILE_OUTPUT_FREQUENCY* parameter in **IPE.inp**. The fields stored in the HDF5 file correspond to the data values on the IPE Apex Grid.

### IPE Geographic (Post-Processed) NetCDF files

The IPE post-processor reads in the HDF5 files, interpolates the IPE model state to a geographic grid (latitude, longitude, altitude), and writes the interpolated fields to NetCDF files. These files have metadata that explain what information is contained within the file. This metadata can be reported using the ncdump utility.

For reference, a list of fields and their units are provided, as reported from ncdump on the post-processed, geographic netcdf files

```{code-block} bash

double helium(time, Z, latitude, longitude) ;
    helium:long_name = "NeutralHelium Density" ;
    helium:units = "kg m^{-3}" ;

double oxygen(time, Z, latitude, longitude) ;
    oxygen:long_name = "NeutralOxygen Density" ;
    oxygen:units = "kg m^{-3}" ;

double molecular_oxygen(time, Z, latitude, longitude) ;
    molecular_oxygen:long_name = "Neutral Molecular Oxygen Density" ;
    molecular_oxygen:units = "kgm^{-3}" ;

double molecular_nitrogen(time, Z, latitude, longitude) ;
    molecular_nitrogen:long_name = "Neutral Molecular Nitrogen Density" ;
    molecular_nitrogen:units = "kgm^{-3}" ;

double nitrogen(time, Z, latitude, longitude) ;
    nitrogen:long_name = "NeutralNitrogen Density" ;
    nitrogen:units = "kg m^{-3}" ;

double hydrogen(time, Z, latitude, longitude) ;
    hydrogen:long_name = "NeutralHydrogen Density" ;
    hydrogen:units = "kg m^{-3}" ;

double temperature(time, Z, latitude, longitude) ;
    temperature:long_name = "Thermosphere Temperature" ;
    temperature:units = "K" ;

double u(time, Z, latitude, longitude) ;
    u:long_name = "Apex1 Velocity" ;
    u:units = "m s^{-1}" ;

double v(time, Z, latitude, longitude) ;
    v:long_name = "Apex2 Velocity" ;
    v:units = "m s^{-1}" ;
double w(time, Z, latitude, longitude) ;
    w:long_name = "Apex3 Velocity" ;
    w:units = "m s^{-1}" ;

double phi(time, latitude, longitude) ;
    phi:long_name = "Electric Potential" ;
    phi:units = "[Unknown]" ;

double mhd_phi(time, latitude, longitude) ;
    mhd_phi:long_name = "Electric Potential - MHD Component" ;
    mhd_phi:units = "[Unknown]" ;

double exb_u(time, latitude, longitude) ;
    exb_u:long_name = "Zonal component of ExB drift velocity" ;
    exb_u:units = "[Unknown]" ;

double exb_v(time, latitude, longitude) ;
    exb_v:long_name = "Meridional component of ExB drift velocity" ;
    exb_v:units = "[Unknown]" ;

double hc(time, latitude, longitude) ;
    hc:long_name = "Hall Conductivity" ;
    hc:units = "[Unknown]" ;

double pc(time, latitude, longitude) ;
    pc:long_name = "Pedersen Conductivity" ;
    pc:units = "[Unknown]" ;

double bc(time, latitude, longitude) ;
    bc:long_name = "Magnetic Field Aligned Conductivity" ;
    bc:units = "[Unknown]" ;

double O+(time, Z, latitude, longitude) ;
    O+:long_name = "Atomic oxygen ion number density (ground state)" ;
    O+:units = " m^{-3}" ;

double H+(time, Z, latitude, longitude) ;
    H+:long_name = "Hydrogen ion number density" ;
    H+:units = " m^{-3}" ;

double He+(time, Z, latitude, longitude) ;
    He+:long_name = "Helium ion number density" ;
    He+:units = " m^{-3}" ;

double N+(time, Z, latitude, longitude) ;
    N+:long_name = "Nitrogen ion number density" ;
    N+:units = " m^{-3}" ;

double NO+(time, Z, latitude, longitude) ;
    NO+:long_name = "Nitrosonium ion number density" ;
    NO+:units = " m^{-3}" ;

double O2+(time, Z, latitude, longitude) ;
    O2+:long_name = "Molecular Oxygen ion number density" ;
    O2+:units = " m^{-3}" ;

double N2+(time, Z, latitude, longitude) ;
    N2+:long_name = "Molecular Nitrogen ion number density" ;
    N2+:units = " m^{-3}" ;

double O+\(2D\)(time, Z, latitude, longitude) ;
    O+\(2D\):long_name = "Atomic oxygen ion number density (first excited state)" ;
    O+\(2D\):units = " m^{-3}" ;

double O+\(2P\)(time, Z, latitude, longitude) ;
    O+\(2P\):long_name = "Atomic oxygen ion number density  (second excited state)" ;
    O+\(2P\):units = " m^{-3}" ;

double ion_temp(time, Z, latitude, longitude) ;
    ion_temp:long_name = "Ion temperature" ;
    ion_temp:units = "K" ;

double e(time, Z, latitude, longitude) ;
    e:long_name = "Electron number density" ;
    e:units = " m^{-3}" ;

double aur_precip(time, Z, latitude, longitude) ;
    aur_precip:long_name = "Total Ionization Rate from Auroral Precipitation" ;
    aur_precip:units = "[Unknown]" ;

double O+_precip(time, Z, latitude, longitude) ;
    O+_precip:long_name = "Oxygen Ionization Rate from Auroral Precipitation" ;
    O+_precip:units = "[Unknown]" ;

double O2+_precip(time, Z, latitude, longitude) ;
    O2+_precip:long_name = "Molecular Oxygen Ionization Rate from Auroral Precipitation" ;
    O2+_precip:units = "[Unknown]" ;

double N2+_precip(time, Z, latitude, longitude) ;
    N2+_precip:long_name = "Molecular Nitrogen Ionization Rate from Auroral Precipitation" ;
    N2+_precip:units = "[Unknown]" ;
```
