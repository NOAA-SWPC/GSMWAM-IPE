help([[
  loads NEMS WAM-IPE prerequisites for Cheyenne/Intel and MPT"
]])

ncarenv_ver=os.getenv("ncarenv_ver") or "1.3"
load(pathJoin("ncarenv", ncarenv_ver))

intel_ver=os.getenv("intel_ver") or "18.0.5"
load(pathJoin("intel", intel_ver))

mkl_ver=os.getenv("mkl_ver") or "2018.0.5"
load(pathJoin("mkl", mkl_ver))

ncarcompilers_ver=os.getenv("ncarcompilers_ver") or "0.5.0"
load(pathJoin("ncarcompilers", ncarcompilers_ver))

mpt_ver=os.getenv("mpt_ver") or "2.22"
load(pathJoin("mpt", mpt_ver))

pnetcdf_ver=os.getenv("pnetcdf_ver") or "1.12.1"
load(pathJoin("pnetcdf", pnetcdf_ver))

hdf5_mpi_ver=os.getenv("hdf5_mpi_ver") or "1.10.5"
load(pathJoin("hdf5-mpi", hdf5_mpi_ver))

prepend_path("MODULEPATH", "/gpfs/u/home/sishen/modulefiles")
bacio_ver=os.getenv("bacio_ver") or "2.0.1"
load(pathJoin("bacio", bacio_ver))

nemsio_ver=os.getenv("nemsio_ver") or "2.2.1"
load(pathJoin("nemsio", nemsio_ver))

sigio_ver=os.getenv("sigio_ver") or "2.0.1"
load(pathJoin("sigio", sigio_ver))

sp_ver=os.getenv("sp_ver") or "2.0.2"
load(pathJoin("sp", sp_ver))

w3emc_ver=os.getenv("w3emc_ver") or "2.2.0"
load(pathJoin("w3emc", w3emc_ver))

w3nco_ver=os.getenv("w3nco_ver") or "2.0.6"
load(pathJoin("w3nco", w3nco_ver))

prepend_path("MODULEPATH", "/gpfs/fs1/work/akubaryk/modulefiles")
anaconda_ver=os.getenv("anaconda_ver") or "anaconda3-2019.10"
load(pathJoin("anaconda", anaconda_ver))

prepend_path("MODULEPATH", "/glade/work/montuoro/swpc/swpc.spacepara/modulefiles")
esmf_ver=os.getenv("esmf_ver") or "8.0.1"
load(pathJoin("esmf", esmf_ver))

comio_ver=os.getenv("comio_ver") or "0.0.8"
load(pathJoin("comio", comio_ver))

whatis("Description: WAM-IPE build environment")
