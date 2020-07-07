import math
import numpy

def hpi_from_gw(gw):
  if gw <= 2.5:
    return '1'
  elif gw <= 3.94:
    return '2'
  elif gw <= 6.22:
    return '3'
  elif gw <= 9.82:
    return '4'
  elif gw <= 15.49:
    return '5'
  elif gw <= 24.44:
    return '6'
  elif gw <= 38.56:
    return '7'
  elif gw <= 60.85:
    return '8'
  elif gw <= 96.0:
    return '9'
  else:
    return '10'

def swbt_calc(swbz,swby,swbx=0):
  return math.sqrt(swbz**2+swby**2+swbx**2)

def swden_calc(): # this isn't used?
  return 5.0

def swvel_calc(kp):
  return 317.0+55.84*kp-2.71*kp**2

def swang_calc(by,bz):
  ang = math.atan2(by,bz)/math.pi*180
  if ang < 0: ang+= 360
  return ang

def swby_calc():
  return 0.0

def swbz_calc(kp,f107):
  return -0.085*kp**2 - 0.08104*kp + 0.4337 + 0.00794 * f107 - 0.00219 * kp * f107

def hemi_pow_calc(kp):
  return 1.29 + 15.60*kp - 4.93*kp**2 + 0.64*kp**3

def calc_solar_data(kp,f107):
  mylen = len(f107)
  swbt     = numpy.ones(mylen)
  swangle  = numpy.ones(mylen)
  swvel    = numpy.ones(mylen)
  swden    = numpy.ones(mylen)
  swbz     = numpy.ones(mylen)
  hemi_pow = numpy.ones(mylen)
  hemi_pow_idx = numpy.ones(mylen)
  for i in range(len(f107)):
    swbz[i]         = swbz_calc(kp[i],f107[i])
    swbt[i]         = swbt_calc(swbz[i],swby_calc())
    hemi_pow[i]     = hemi_pow_calc(kp[i])
    swangle[i]      = swang_calc(swby_calc(),swbz[i])
    swvel[i]        = swvel_calc(kp[i])
    swden[i]        = swden_calc()
    hemi_pow_idx[i] = hpi_from_gw(hemi_pow[i])
  return swbt,swangle,swvel,swden,swbz,hemi_pow,hemi_pow_idx


def cap_min_max(mylist,value,lt_flag=True,f107d=66.0):
  for i,x in enumerate(mylist):
    if lt_flag:
      if x < value:
        if i == 0: mylist[i] = f107d
        else:      mylist[i] = mylist[i-1]
    else:
      if x > value: mylist[i] = value
  return mylist
