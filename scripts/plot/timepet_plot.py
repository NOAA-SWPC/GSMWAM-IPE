#!/usr/bin/env python
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('agg') # cannot plt.show() with this, but pyplot fails on the compute nodes without an X Server
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import path
from datetime import datetime, timedelta

def make_plot(data):
	fontfam='serif'
	fig = plt.figure()
	ax = fig.gca()
	if args.date:
		datetimes = [datetime.strptime(args.date, "%Y%m%d%H") + timedelta(seconds=args.timestep*i) for i in range(len(data))]
		plt.plot(datetimes,data)
		myFmt = mdates.DateFormatter('%m/%d %HZ')
		ax.xaxis.set_major_formatter(myFmt)
		plt.xticks(rotation=45)
		plt.xlabel('Integration Time', fontsize=16, fontname=fontfam)
	else:
		plt.plot(range(1,len(data)+1),data)
		plt.xlabel('Integration Step', fontsize=16, fontname=fontfam)
	# standard labeling
	plt.ylabel('Time (minutes)',  fontsize=16, fontname=fontfam)
	plt.title('IPE Integration Length from '+datetimes[0].strftime("%Y/%m/%d %HZ"), fontsize=18, fontname=fontfam)
	# output
	plt.savefig(path.join(args.output_directory,'timepet.eps'))
	#plt.show()
	plt.close()

def output_statistics(data):
	with open(path.join(args.output_directory,'timepet.stat'),'w') as f:
		f.write(str(data.mean())+","+str(data.std()))

def read_timepet(file):
	return np.genfromtxt(file)
	
def main():
	data = read_timepet(path.join(args.input_directory,'timepet.out'))
	output_statistics(data)
	make_plot(data)

## parsing options
parser = ArgumentParser(description='Make simple line-plot of input file', formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input_directory',  help='directory containing timepet.out', type=str, required=True)
parser.add_argument('-o', '--output_directory', help='directory where plot is stored. default: input_directory', type=str)
parser.add_argument('-d', '--date',             help='YYYYMMDDHH (CDATE) of run', type=str)
parser.add_argument('-t', '--timestep',         help='model timestep (seconds)', type=int, default=180)
args = parser.parse_args()
args.output_directory = args.output_directory if args.output_directory else args.input_directory

## run the program
main()
