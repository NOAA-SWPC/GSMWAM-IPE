import parse_realtime as prt
from datetime import datetime, timedelta
from time import sleep
from glob import glob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

SLEEP_TIME = 60

def touch(dt):
    pass

def proceed(dt):
    return (datetime.now() - dt).seconds // 60 >= prt.MAX_WAIT

def latest_date(path):
    sw_search = '{}/*/swpc/geospace_input*.xml'.format(path)
    hp_search = '{}/*/swpc/wam/swpc_aurora_power*.txt'.format(path)

    sw_files = glob(sw_search)
    hp_files = glob(hp_search)

    sw_files.sort(reverse=True)
    hp_files.sort(reverse=True)

    sw_date = get_sw_date(sw_files[0].split('/')[-1])
    hp_date = get_hp_date(open(hp_files[0], 'r'))

    return min(sw_date, hp_date)

def get_sw_date(filename):
    return datetime.strptime(filename,'geospace_input-%Y%m%dT%H%M.xml') + \
           timedelta(minutes = prt.DELAY_INTERVAL)

def get_hp_date(fp):
    last_line = fp.readlines()[-1].split()
    return datetime.strptime("{}{}".format(last_line[0],last_line[1]),'%Y-%m-%d%H:%M') + \
           timedelta(minutes = prt.L1_DELAY)

def get_last_date(outfile):
    with open(outfile, 'r') as f:
        return datetime.strptime(f.readlines()[-1].split()[0],prt.WAM_INPUT_FMT)

def main():
    parser = ArgumentParser( \
               description='Parse KP, F10.7, 24hr average Kp, and hemispheric power files into binned data', \
               formatter_class=ArgumentDefaultsHelpFormatter \
             )
    parser.add_argument('-e', '--end_date',   help='end date of run (YYYYMMDDhh)', type=str, default='202006010559')
    parser.add_argument('-d', '--duration',   help='duration (mins) of each segment',   type=int, default=15)
    parser.add_argument('-p', '--path',       help='path to input parameters', type=str, default=prt.DEFAULT_PATH)
    parser.add_argument('-o', '--output',     help='full path to output file', type=str, default=prt.DEFAULT_NAME)
    args = parser.parse_args()

    end_date = datetime.strptime(args.end_date,'%Y%m%d%H%M')

    current_date = get_last_date(args.output) + timedelta(minutes=1)
    target_date = current_date + timedelta(minutes=args.duration)

    ip = prt.InputParameters(current_date, args.duration, args.path, args.output, True)
    ip.parse()

    while current_date < end_date:
        if latest_date(args.path) >= target_date or proceed(target_date):
            try:
                ip.date_list   = [ current_date + timedelta(minutes=x) for x in range(args.duration+prt.MAX_WAIT)  ]
                ip.output_list = [ current_date + timedelta(minutes=x) for x in range(args.duration) ]
                # parse
                ip.parse()
                # write
                ip.output()
                # touch and advance
                touch(target_date)                
                current_date += timedelta(minutes=args.duration)
                target_date  += timedelta(minutes=args.duration)
            except Exception as e:
                print(e)
                pass
        else:
            sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
