# Check GPU memory usage, and send email to you once the memory usage
# is low, which means the training is done or raising errors
#
# Author: Yuliang Zou
#         ylzou@umich.edu

from pynvml import *
import smtplib
from email.mime.text import MIMEText
from time import sleep
import argparse

def parse_args():
    """ 
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Real-time GPU memory usage monitor')
    parser.add_argument('--receiver', dest='receiver',
                        help='Specify which email address you want to send',
                        type=str)
    parser.add_argument('--GPU', dest='gpu_id',
                        help='GPU device id to minitor', type=int)
    parser.add_argument('--rate', dest='rate',
                        help='Send an email if usage rate lower than this',
                        default=0.8, type=float)
    parser.add_argument('--interval', dest='interval',
                        help='Time interval (minutes) between two checks',
                        default=5, type=int)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args     = parse_args()
    receiver = args.receiver
    gpu_id   = args.gpu_id
    rate     = args.rate
    interval = args.interval

    nvmlInit()    # Necessary step
    deviceCount = nvmlDeviceGetCount()

    # Sanity check
    if gpu_id + 1 > deviceCount:
        print 'Invalid GPU id!'
        raise Exception
    sec = interval * 60

    handle = nvmlDeviceGetHandleByIndex(gpu_id)
    text = 'Device' + str(gpu_id) + ':' + nvmlDeviceGetName(handle) + '\n'
    print text

    while True:
        info = nvmlDeviceGetMemoryInfo(handle)
        print '\n'
        print 'Total memory: ', info.total
        print 'Free memory: ', info.free
        print 'Used memory: ', info.used

        # Memory usage if too low
        if 1.0 * info.used / info.total < rate:
            break

        sleep(sec)

    # Send email
    text += 'Used memory: ' + str(info.used/1024/1024) + 'MB \n'
    text += 'Total memory: ' + str(info.total/1024/2014) + 'MB \n'
    text += 'Memory usage is too low! Completed or interrupted??!'

    msg = MIMEText(text)
    msg['Subject'] = 'GPU usage report'
    msg['From'] = receiver
    msg['To'] = receiver

    s = smtplib.SMTP('localhost')
    s.sendmail(receiver, [receiver], msg.as_string())
    s.quit()