help([[
  loads NEMS WAM-IPE prerequisites for Hera/Intel"
]])

setenv("NCEPLIBS", "/scratch2/NCEPDEV/nwprod/NCEPLIBS")
prepend_path("MODULEPATH", "/contrib/sutils/modulefiles")
load("sutils")

intel_ver=os.getenv("intel_ver") or "18.0.5.274"
load(pathJoin("intel", intel_ver))

impi_ver=os.getenv("impi_ver") or "2018.0.4"
load(pathJoin("impi", impi_ver))

hdf5parallel_ver=os.getenv("hdf5parallel_ver") or "1.10.5"
load(pathJoin("hdf5parallel", hdf5parallel_ver))

netcdf_ver=os.getenv("netcdf_ver") or "4.7.0"
load(pathJoin("netcdf", netcdf_ver))

prepend_path("MODULEPATH", "/scratch2/NCEPDEV/nwprod/NCEPLIBS/modulefiles")

bacio_ver=os.getenv("bacio_ver") or "2.0.3"
load(pathJoin("bacio", bacio_ver))

nemsio_ver=os.getenv("nemsio_ver") or "2.2.4"
load(pathJoin("nemsio", nemsio_ver))

sp_ver=os.getenv("sp_ver") or "2.0.3"
load(pathJoin("sp", sp_ver))

w3emc_ver=os.getenv("w3emc_ver") or "2.3.1"
load(pathJoin("w3emc", w3emc_ver))

w3nco_ver=os.getenv("w3nco_ver") or "2.0.7"
load(pathJoin("w3nco", w3nco_ver))

szip_ver=os.getenv("szip_ver") or "2.1"
load(pathJoin("szip", szip_ver))

prepend_path("MODULEPATH", "/scratch1/NCEPDEV/nems/emc.nemspara/soft/modulefiles")
esmf_ver=os.getenv("esmf_ver") or "8.0.0"
load(pathJoin("esmf", esmf_ver))

pnetcdf_ver=os.getenv("pnetcdf_ver") or "1.11.2"
load(pathJoin("pnetcdf", pnetcdf_ver))

prepend_path("MODULEPATH", "/scratch1/NCEPDEV/swpc/Adam.Kubaryk/modulefiles")
comio_ver=os.getenv("comio_ver") or "0.0.8"
load(pathJoin("comio", comio_ver))

anaconda_ver=os.getenv("anaconda_ver") or "anaconda3-2019.10"
load(pathJoin("anaconda", anaconda_ver))

setenv("I_MPI_ADJUST_ALLTOALLV", "0")

whatis("Description: WAM-IPE build environment")
