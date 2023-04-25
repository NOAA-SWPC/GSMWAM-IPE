help([[
  loads NEMS WAM-IPE prerequisites for Hera/Intel"
]])

prepend_path("MODULEPATH", "/contrib/sutils/modulefiles")
load("sutils")

intel_ver=os.getenv("intel_ver") or "18.0.5.274"
load(pathJoin("intel", intel_ver))

impi_ver=os.getenv("impi_ver") or "2018.0.4"
load(pathJoin("impi", impi_ver))

prepend_path("MODULEPATH", "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack")

hpc_ver=os.getenv("hpc_ver") or "1.1.0"
load(pathJoin("hpc", hpc_ver))

hpc_intel_ver=os.getenv("hpc_intel_ver") or "18.0.5.274"
load(pathJoin("hpc-intel", hpc_intel_ver))

hpc_impi_ver=os.getenv("hpc_impi_ver") or "2018.0.4"
load(pathJoin("hpc-impi", hpc_impi_ver))

hdf5_ver=os.getenv("hdf5_ver") or "1.10.6"
load(pathJoin("hdf5", hdf5parallel_ver))

netcdf_ver=os.getenv("netcdf_ver") or "4.7.4"
load(pathJoin("netcdf", netcdf_ver))

bacio_ver=os.getenv("bacio_ver") or "2.4.1"
load(pathJoin("bacio", bacio_ver))

nemsio_ver=os.getenv("nemsio_ver") or "2.5.2"
load(pathJoin("nemsio", nemsio_ver))

sp_ver=os.getenv("sp_ver") or "2.3.3"
load(pathJoin("sp", sp_ver))

w3nco_ver=os.getenv("w3nco_ver") or "2.4.1"
load(pathJoin("w3nco", w3nco_ver))

esmf_ver=os.getenv("esmf_ver") or "8.4.0b08"
load(pathJoin("esmf", esmf_ver))

pnetcdf_ver=os.getenv("pnetcdf_ver") or "1.11.2"
load(pathJoin("pnetcdf", pnetcdf_ver))


setenv("CC", "mpiicc")
setenv("CXX", "mpiicpc")
setenv("FC", "mpiifort")

prepend_path("MODULEPATH", "/scratch1/NCEPDEV/swpc/Adam.Kubaryk/modulefiles")
comio_ver=os.getenv("comio_ver") or "0.0.8"
load(pathJoin("comio", comio_ver))

anaconda_ver=os.getenv("anaconda_ver") or "anaconda3-2019.10"
load(pathJoin("anaconda", anaconda_ver))

setenv("I_MPI_ADJUST_ALLTOALLV", "0")

whatis("Description: WAM-IPE build environment")
