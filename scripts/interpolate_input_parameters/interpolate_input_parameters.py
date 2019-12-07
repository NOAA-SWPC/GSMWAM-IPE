#!/usr/bin/env python
import numpy
#numpy.set_printoptions(threshold='nan')
from os import path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import datetime
from itertools import chain
import math
from sw_from_f107_kp import *

## takes 3hr-avg Kp, daily F10.7, and minute-binned hemispheric power and 24hr-avg Kp
## and translates them all to the same cadence (hard-coded 1 minute)

## future todo
# implement variable cadence
# turn the YYYYMMDDHH strings into a class rather than having a mess of functions all over the place

### weak failure handling

def failure(fail_point):
  ## fail_point: string
  print('error during '+fail_point)
  exit(0)

### YYYYMMDDHH functions

def hourless(string):
  ## convert YYYYMMDDHH string to YYYYMMDD
  return string[:-2]

def doy(date):
  ## date: YYYYMMDDHH string to return DOY for
  return datetime.datetime.strptime(date,'%Y%m%d%H').timetuple().tm_yday

def new_timestamp(init, diff):
  ## init: YYYYMMDDHH string
  ## diff: integer hours
  # get new YYYYMMDDHH for date + delta_hours
  dt = datetime.datetime.strptime(init, '%Y%m%d%H')
  return (dt+datetime.timedelta(0, 60*60*diff)).strftime('%Y%m%d%H')

def time_diff(start, compare):
  ## start:   YYYYMMDDHH
  ## compare: YYYYMMDDHH
  # get number of minutes between two YYYYMMDDHH strings
  start_time = datetime.datetime.strptime(start,   '%Y%m%d%H%M')
  comp_time  = datetime.datetime.strptime(compare, '%Y%m%d%H%M')
  return int((start_time-comp_time).total_seconds()/60)

def get_dates(start,end):
  ## get all dates YYYYMMDD(HH) encompassing start and end timestamps
  dates = [start]                        # start with the start day
  if hourless(start) != hourless(end):
    next = new_timestamp(dates[-1], 24)    # add 24 hours
    while hourless(next) != hourless(end): # check YYYYMMDD against the end day
      dates.append(next)                   # add string         ^
      next = new_timestamp(dates[-1], 24)  # add 24 hours ------^
    dates.append(end)
  return dates

### interpolation

def interpolate(arr, mins_per_segment):
  ## arr: array of values to linearly interpolate between
  ## mins_per_segment: integer number of values per interpolation pair
  output = [] # initialize
  for pair in zip(arr, arr[1:]): # pair the values in the array
    output = numpy.append(output, numpy.linspace(pair[0], pair[1], mins_per_segment+1)[:-1]) # take the linspace, dropping off the last value
  output = numpy.append(output, arr[-1]) # add the last value
  return output

### parsing

def get_f107d(dates):
  f107 = []
  try:
    for cdate in dates:
      with open(path.join(args.path, 'KP_AP_F107', cdate[:4])) as file:
        for line in file:
          if line[:6] == hourless(cdate[2:]):
            f107 = numpy.append(f107, float(line[65:71]))
            break
  except:
    failure('f107d read')

  return numpy.mean(f107)

def get_kp_f107(dates):
  ## start: YYYYMMDDHH string for starting date
  ## end:   YYYYMMDDHH string for ending date
  # initialize
  kp    = []
  f107  = []
  f107d = []
  try:
    for cdate in dates:                                    # for each date to pull info for, open database file
      f107d = numpy.append(f107d, get_f107d(get_dates(new_timestamp(cdate,-24*40),new_timestamp(cdate,24*40))))
      with open(path.join(args.path, 'KP_AP_F107', cdate[:4])) as file:
        for line in file:                                  # for each line
          if line[:6] == hourless(cdate[2:]):              # match date, and append to lists
            kp = numpy.append(kp, [float(line[i:i+2])/10 for i in range(12, 28, 2)])
            f107 = numpy.append(f107, float(line[65:71]))
            break # break out of the current file
  except:
    failure('yearly kp_ap database read')
  # return the interpolated values
  return interpolate(kp, mins_per_kp_segment), interpolate(f107, mins_per_f107_segment), interpolate(f107d, mins_per_f107_segment)

def kp_avg_date_fmt(date):
   return date[:4] + '_doy' + "{:03d}".format(doy(date)) + '_avgkp.dat'

def get_24hr_kp_avg(dates):
  kp_avg = []
  try:
    for cdate in dates:
      with open(path.join(args.path, '24HR_KP_AVG', cdate[:4], kp_avg_date_fmt(cdate))) as file:
        for line in file:
          kp_avg = numpy.append(kp_avg,float(line.rstrip()[-10:]))
  except:
    failure('24hr_kp_avg database read')

  return kp_avg

def hemi_date_fmt(date):
  return datetime.datetime.strptime(date,'%Y%m%d%H').strftime('%Y-%m-%d') + '-input.txt'

def get_solar_data(dates):
  swbt         = []
  swangle      = []
  swvel        = []
  swden        = []
  bz           = []
  hemi_pow     = []
  hemi_pow_idx = []

  try:
    for cdate in dates:
      with open(path.join(args.path, 'AURORA_POWER', cdate[:4], hemi_date_fmt(cdate))) as file:
        for i, line in enumerate(file):
          if i > 94:
            split_line = line.split(' ')
            swbt         = numpy.append(swbt,         float(split_line[0] ))
            swangle      = numpy.append(swangle,      float(split_line[1] ))
            swvel        = numpy.append(swvel,        float(split_line[3] ))
            swden        = numpy.append(swden,        float(split_line[4] ))
            bz           = numpy.append(bz,           float(split_line[5] ))
            hemi_pow     = numpy.append(hemi_pow,     float(split_line[-1]))
            hemi_pow_idx = numpy.append(hemi_pow_idx,       split_line[-2] )
  
  except:
    failure('hemispheric power read')
  
  return swbt, swangle, swvel, swden, bz, hemi_pow, hemi_pow_idx

def start_fixed_data(mduration):
  # read f107, kp
  with open(args.fixed,'r') as f:
    lines = f.read().splitlines()
    return numpy.ones(mduration)*float(lines[0]), numpy.ones(mduration)*float(lines[1])

def finish_fixed_data(mduration):
  # read swvel, swden, swby, swbz, gwatts, HPI
  with open(args.fixed,'r') as f:
    lines = f.read().splitlines()
    return numpy.ones(mduration)*float(lines[2]), numpy.ones(mduration)*float(lines[3]), \
           numpy.ones(mduration)*float(lines[4]), numpy.ones(mduration)*float(lines[5]), \
           numpy.ones(mduration)*float(lines[6]), numpy.ones(mduration)*float(lines[7])

def parse(start_date, end_date, hduration):
  ## start_date: YYYYMMDDHH string
  ## end_date:   YYYYMMDDHH string
  ## hduration:  integer hours to forecast, convert immediately to minutes+1 mduration
  mduration = hduration*60+1

  starting_min = float(start_date[-2:])*60
  ending_min   = float(end_date[-2:]  )*60

  # first determine which dates we need to pull data for
  # the F10.7 is the dominating factor as the daily value, so we just check against that for Kp/F10.7
  if float(starting_min) / mins_per_f107_segment > midpoint_f107_fraction: # start interpolation from current day
    min_f107 = start_date
  else:                                                                    # start interpolation from prior day
    min_f107 = new_timestamp(start_date, -24)
  
  if float(ending_min) / mins_per_f107_segment > midpoint_f107_fraction:   # end interpolation at next day
    max_f107 = new_timestamp(end_date,    24)
  else:                                                                    # end interpolation at current day
    max_f107 = end_date

  # KP/F107
  if args.mode[:4] == 'time':
    kp_offset     = time_diff(start_date+'00', hourless(min_f107) + kp_midpoint_string)
    f107_offset   = time_diff(start_date+'00', hourless(min_f107) + f107_midpoint_string)
    kp_avg_offset = time_diff(start_date+'00', hourless(start_date) + '0000')
    kp, f107, f107d = get_kp_f107(get_dates(min_f107, max_f107))
    kp_avg          = get_24hr_kp_avg(get_dates(start_date,end_date))
  else: # fixed kp/f107
    kp_offset     = 0
    f107_offset   = 0
    kp_avg_offset = 0
    f107, kp = start_fixed_data(mduration)
    kp_avg = kp ; f107d = f107 # 24hr avg kp = kp, f10.7 daily = f10.7
  f107  = cap_min_max(f107,66,True)
  f107d = cap_min_max(f107d,66,True)
  # SOLAR WIND DATA
  if args.mode[-6:] != 'derive': # either timeobs (equation) or fixall (0)
    hemi_offset = kp_avg_offset
    if args.mode[-3:] == 'obs': # get solar data from obs
      swbt, swangle, swvel, swden, swbz, hemi_pow, hemi_pow_idx = get_solar_data(get_dates(start_date,end_date))
    else: # values are fixed from input
      swvel, swden, swby, swbz, hemi_pow, hemi_pow_idx = finish_fixed_data(mduration)
      swbt = numpy.sqrt(swby**2 + swbz**2)
      swangle = numpy.arcsin(swby/swbt)/math.pi*180
  else: # use Tim's algorithms: https://github.com/SWPC-IPE/WAM-IPE/issues/126#issuecomment-374304207
    hemi_offset = 0
    swbt, swangle, swvel, swden, swbz, hemi_pow, hemi_pow_idx = calc_solar_data(kp[kp_offset:kp_offset+mduration], f107[f107_offset:f107_offset+mduration])

  # return our subarrays
  return kp[kp_offset:kp_offset+mduration], f107[f107_offset:f107_offset+mduration], f107d[f107_offset:f107_offset+mduration], \
         kp_avg[kp_avg_offset:kp_avg_offset+mduration], swbt[hemi_offset:hemi_offset+mduration], \
         swangle[hemi_offset:hemi_offset+mduration], swvel[hemi_offset:hemi_offset+mduration], \
         swden[hemi_offset:hemi_offset+mduration], swbz[hemi_offset:hemi_offset+mduration], \
         hemi_pow[hemi_offset:hemi_offset+mduration], hemi_pow_idx[hemi_offset:hemi_offset+mduration]

### output

def output_timestamp(start_date,delta=0):
  return (datetime.datetime.strptime(start_date,'%Y%m%d%H') + datetime.timedelta(minutes=delta)).strftime('%Y-%m-%dT%H:%M:%SZ')


def output(file, start_date, kp, f107, f107d, kp_avg, swbt, swangle, swvel, swbz, hemi_pow, hemi_pow_idx, swden, swby):
  ## simply
  f = open(file,'w')

  f.write("Issue Date          "+output_timestamp(start_date)+"\n")
  f.write("Flags:  0=Forecast, 1=Estimated, 2=Observed \n\n")

  f.write(" Date_Time                   F10          Kp     F10Flag      KpFlag  F10_81dAvg   24HrKpAvg    NHemiPow NHemiPowIdx    SHemiPow SHemiPowIdx       SW_Bt    SW_Angle SW_Velocity       SW_Bz      SW_Den   \n")
  f.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   \n")
  for i in range(0,len(kp)):
    k = i-offset
    j = k-averaging_mins
    if k < 1 : k = 1
    if j < 0 : j = 0
    bz = numpy.average(swbz[j:k])
    by = numpy.average(swby[j:k])
    bt = swbt_calc(by,bz)
    ang = swang_calc(by,bz)
    f.write("{0}{1:>12.7f}{2:>12.7f}{3:>12}{4:>12}{5:>12.7f}{6:>12.7f}{7:>12.7f}{8:>12}{9:>12.7f}{10:>12.7}{11:>12.7f}{12:>12.7f}{13:>12.7f}{14:>12.7f}{15:>12.7f}\n".format( \
            output_timestamp(start_date,i), \
            f107[i],                    \
            kp[i],                      \
            '2','1',                    \
            f107d[i],                   \
            kp_avg[i],                  \
            hemi_pow[i],                \
            hemi_pow_idx[i],            \
            hemi_pow[i],                \
            hemi_pow_idx[i],            \
            bt,                         \
            ang,                        \
            numpy.average(swvel[j:k]),  \
            bz,                         \
            numpy.average(swden[j:k])))

### main function
                    
def run(start_date, duration, output_filename):
  end_date = new_timestamp(start_date, duration)
  kp, f107, f107d, kp_avg, swbt, swangle, swvel, swden, swbz, hemi_pow, hemi_pow_idx = parse(start_date, end_date, duration)
  swby = swbt * numpy.sin(swangle*math.pi/180)
  output(output_filename, start_date, kp, f107, f107d, kp_avg, swbt, swangle, swvel, swbz, hemi_pow, hemi_pow_idx, swden, swby)

### we start below

## parsing options
parser = ArgumentParser(description='Parse KP, F10.7, 24hr average Kp, and hemispheric power files into binned data', formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--interval',   help='interval length (minutes) (default=1)', type=int, default=1) # this feature doesn't work yet
parser.add_argument('-d', '--duration',   help='duration of run (hours) (default=24)',  type=int, default=24)
parser.add_argument('-s', '--start_date', help='starting date of run (YYYYMMDDhh)',     type=str, required=True)
parser.add_argument('-p', '--path',       help='path to database files',                type=str, required=True)
parser.add_argument('-o', '--output',     help='path to output file',                   type=str, default='wam_input_f107_kp.txt')
parser.add_argument('-m', '--mode', help='timeobs (time-varying from obs), timederive (time-varying kp/f10.7, derived solar wind drivers), '+\
                                         'fixderive (fixed kp/f10.7, derived solar wind drivers), or fixall (everything fixed)', type=str, default='timeobs')
parser.add_argument('-f', '--fixed', help='full path to file containing fixed data for run', type=str, default='')

## global variables
args = parser.parse_args()

mins_per_kp_segment    = 3*60
mins_per_f107_segment  = 24*60
midpoint_f107          = 15*60
midpoint_f107_fraction = float(midpoint_f107)/mins_per_f107_segment
f107_midpoint_string   = '1500'
kp_midpoint_string     = '0130'
averaging_mins         = 20
offset         = 20

## __MAIN__
run(args.start_date, args.duration, args.output)
