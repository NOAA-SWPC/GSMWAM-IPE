help([[
  loads NEMS WAM-IPE prerequisites for Cheyenne/Intel and MPT"
]])

-- Netcdf conflicts with loads later on, unloading.
unload("netcdf")

ncarenv_ver=os.getenv("ncarenv_ver") or "1.3"
load(pathJoin("ncarenv", ncarenv_ver))

intel_ver=os.getenv("intel_ver") or "19.1.1"
load(pathJoin("intel", intel_ver))

mkl_ver=os.getenv("mkl_ver") or "2020.0.1"
load(pathJoin("mkl", mkl_ver))

ncarcompilers_ver=os.getenv("ncarcompilers_ver") or "0.5.0"
load(pathJoin("ncarcompilers", ncarcompilers_ver))

mpt_ver=os.getenv("mpt_ver") or "2.22"
load(pathJoin("mpt", mpt_ver))

prepend_path("MODULEPATH", "/glade/work/akubaryk/modulefiles")

esmf_ver=os.getenv("esmf_ver") or "8.4.2"
load(pathJoin("esmf", esmf_ver))

netcdf_mpi_ver=os.getenv("netcdf_mpi_ver") or "4.7.4"
load(pathJoin("netcdf-mpi", netcdf_mpi_ver))

pnetcdf_ver=os.getenv("pnetcdf_ver") or "1.12.1"
load(pathJoin("pnetcdf", pnetcdf_ver))

nemsio_ver=os.getenv("nemsio_ver") or "2.5.2"
load(pathJoin("nemsio", nemsio_ver))

sp_ver=os.getenv("sp_ver") or "2.3.3"
load(pathJoin("sp", sp_ver))

pio_ver=os.getenv("pio_ver") or "2.5.10"
load(pathJoin("pio", pio_ver))

prepend_path("MODULEPATH", "/glade/work/akubaryk/modulefiles")
anaconda_ver=os.getenv("anaconda_ver") or "anaconda3-2019.10"
load(pathJoin("anaconda", anaconda_ver))

prepend_path("MODULEPATH", "/glade/work/akubaryk/noscrub/modulefiles")
comio_ver=os.getenv("comio_ver") or "v0.0.10"
load(pathJoin("comio", comio_ver))

whatis("Description: WAM-IPE build environment")
