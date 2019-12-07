#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
from sw_from_f107_kp import *
import numpy
import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def compare_timestamp(date1,date2):
  if datetime.datetime.strptime(date1,'%Y%m%d%H') == datetime.datetime.strptime(date2,'%Y-%m-%dT%H:%M:%SZ'):
    return True
  else:
    return False

def output_timestamp(start_date,delta=0):
  return (datetime.datetime.strptime(start_date,'%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(minutes=delta)).strftime('%Y-%m-%dT%H:%M:%SZ')

def compare_create(start_date):
  return datetime.datetime.strptime(start_date,'%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H')

def interpolate(arr, mins_per_segment):
  ## arr: array of values to linearly interpolate between
  ## mins_per_segment: integer number of values per interpolation pair
  output = [] # initialize
  for pair in zip(arr, arr[1:]): # pair the values in the array
    output = numpy.append(output, numpy.linspace(pair[0], pair[1], mins_per_segment+1)[:-1]) # take the linspace, dropping off the last value
  output = numpy.append(output, arr[-1]) # add the last value
  return output

parser = ArgumentParser(description='Parse KP, F10.7, 24hr average Kp, and hemispheric power files into binned data', formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--start_date', help='starting date of run (YYYYMMDDhh)',     type=str, default='')
parser.add_argument('-d', '--duration', help='duration (hours) of run', type=int, default=24)
args = parser.parse_args()

input = 'wam_input2.xsd'
output = 'wam_input.asc'
mins_per_f107_segment = 3*60

tree = ET.parse(input)
root = tree.getroot()

old_format = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'] == 'wam_input.xsd'

f = open(output,'w')

date  = []
f107  = []
kp    = []
f107d = []
kpa   = []

for child in root.findall('data-item'):
  date.append( child.get('time-tag'))
  try:    f107.append( float(child.find('f10').text))
  except: f107.append( 0.0 )
  kp.append(   float(child.find('kp').text))
  if old_format:
    f107d.append(float(tree.find('f10-81-avg-currentday').text))
    kpa.append(  float(child.find('kp').text))
  else:
    f107d.append(float(child.find('f10-41-avg').text))
    kpa.append(  float(child.find('kp-24-hr-avg').text))

if args.start_date == '':
  args.start_date = compare_create(date[0])

kp    = interpolate(cap_min_max(kp,4,False),    mins_per_f107_segment)
f107  = interpolate(cap_min_max(f107,66,True,f107d[0]),  mins_per_f107_segment)
f107d = interpolate(cap_min_max(f107d,66,True), mins_per_f107_segment)
kpa   = interpolate(cap_min_max(kpa,4,False),   mins_per_f107_segment)

swbt, swangle, swvel, swden, swbz, hemi_pow, hemi_pow_idx = calc_solar_data(kp, f107)

f.write('Issue Date          '+tree.find('issue-date').text+"\n")
f.write('Flags:  0=Forecast, 1=Estimated, 2=Observed \n\n')

f.write(" Date_Time                   F10          Kp     F10Flag      KpFlag  F10_41dAvg   24HrKpAvg    NHemiPow NHemiPowIdx    SHemiPow SHemiPowIdx       SW_Bt    SW_Angle SW_Velocity       SW_Bz      SW_Den   \n")
f.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   \n")

write_output = False

for i in range(0,len(kp)):
  if not write_output:
    write_output = compare_timestamp(args.start_date,output_timestamp(date[0],i))
    if write_output: flip = i
  if write_output:
    f.write("{0}{1:>12.7f}{2:>12.7f}{3:>12}{4:>12}{5:>12.7f}{6:>12.7f}{7:>12.7f}{8:>12}{9:>12.7f}{10:>12.7}{11:>12.7f}{12:>12.7f}{13:>12.7f}{14:>12.7f}{15:>12.7f}\n".format( \
             output_timestamp(date[0],i), \
             f107[i],                     \
             kp[i],                       \
             '2','1',                     \
             f107d[i],                    \
             kpa[i],                      \
             hemi_pow[i],                 \
             hemi_pow_idx[i],             \
             hemi_pow[i],                 \
             hemi_pow_idx[i],             \
             swbt[i],                     \
             swangle[i],                  \
             swvel[i],                    \
             swbz[i],                     \
             swden[i]))

for i in range(len(kp),args.duration*60+flip):
  f.write("{0}{1:>12.7f}{2:>12.7f}{3:>12}{4:>12}{5:>12.7f}{6:>12.7f}{7:>12.7f}{8:>12}{9:>12.7f}{10:>12.7}{11:>12.7f}{12:>12.7f}{13:>12.7f}{14:>12.7f}{15:>12.7f}\n".format( \
           output_timestamp(date[0],i), \
           f107[-1],                    \
           kp[-1],                      \
           '2','1',                     \
           f107d[-1],                   \
           kpa[-1],                     \
           hemi_pow[-1],                \
           hemi_pow_idx[-1],            \
           hemi_pow[-1],                \
           hemi_pow_idx[-1],            \
           swbt[-1],                    \
           swangle[-1],                 \
           swvel[-1],                   \
           swbz[-1],                    \
           swden[-1]))
