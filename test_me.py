import os
import datetime
import multiprocessing
import re
import subprocess
import time
import itertools
import threading
import sys
from colorama import Fore

os.system("git config --global credential.https://github.com.username da2i2")
os.system("git config --global credential.https://github.com.password Aiub@123456")
os.system("git pull")

now_time = datetime.datetime.now()
now_time = str(now_time)

size = os.path.getsize('device_list_s3.txt')



with open('device_list_s3.txt', 'r') as f:
    last_line = f.readlines()[-1]


if(size > 0):
    
    dname,dnum = last_line.split("_")

    dnum = int(dnum)

    dnum += 1

    dnum = str(dnum)

    Device_name =  "sd03_" + dnum   
else:
    pass
    




print("Running test for Device - " + Device_name)


print("")

print("============================================")
print("Device Internet Test will start now")
print("============================================")

os.system("speedtest")

print("")

speed_file = Device_name + "_speedtest.csv"
response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('\((.*?)\s.+jitter\)\s', response, re.MULTILINE)

ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

try:
    f = open(speed_file, 'a+')
    if os.stat(speed_file).st_size == 0:
            f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
except:
    pass
f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)')
f.write('{},{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload))
f.close()


print("================== Internet Test Done ====================")


print("")

print("============================================")
print("Connected USB Devices")
print("============================================")

print("")

myCmd = r'sudo lsusb > /home/pi/Desktop/device_test_s3/'+Device_name+'_USB.txt'
os.system(myCmd)


#os.system("lsusb")

print("")


print("================== USB Test Done ====================")


print("============================================")
print("Device stress test will start now")
print("============================================")



#os.system('/home/pi/.local/bin/stressberry-run -n "Temp" -d 30 -i 30 -c 4 ' + Device_name + '.dat' )
#os.system('MPLBACKEND=Agg /home/pi/.local/bin/stressberry-plot ' + Device_name + '.dat ' + '-f -d 300 -f -l 400 2200 -t 0 90 -o ' + Device_name + '.png')

print("")

with open('device_list_s3.txt', 'a') as f:
    f.writelines('\n')
    f.writelines(Device_name)

print("================== Stress Test Done ====================")

print(Fore.GREEN + "============================================")
print("PASSWORD: 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")
print("============================================" + Fore.RESET)


os.system("git add *")
os.system('git commit -m "' + Device_name + ' added"')
os.system("git push")
#os.system("git pull")

