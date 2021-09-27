#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import subprocess
import sys
import datetime
import csv

def GetCpuFreq():
    Cmd = 'vcgencmd measure_clock arm'
    result = subprocess.run(Cmd, shell = True, capture_output=True, universal_newlines=True)
    CpuFreq = int(result.stdout.split('=')[1])
    return int(CpuFreq)

def GetCpuTemp():
    Cmd = 'vcgencmd measure_temp'
    result = subprocess.run(Cmd, shell=True,  capture_output=True, universal_newlines=True)
    CpuTemp = result.stdout.split("=")[1]
    CpuTemp = float(CpuTemp.split("'C")[0])
    return CpuTemp

def GetCpuVolt():
    Cmd = 'vcgencmd measure_volts'
    result = subprocess.run(Cmd, shell=True,  capture_output=True, universal_newlines=True)
    CpuVolt = result.stdout.split("=")[1]
    CpuVolt = float(CpuVolt.split("V")[0])
    return CpuVolt

def GetCpuStat():
    Cmd = 'cat /proc/stat | grep cpu'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    LineList = Rstdout.splitlines()
    #
    TckList = []
    for Line in LineList:
        ItemList = Line.split()
        TckIdle = int(ItemList[4])
        TckBusy = int(ItemList[1])+int(ItemList[2])+int(ItemList[3])
        TckAll  = TckBusy + TckIdle
        TckList.append( [ TckBusy ,TckAll ] )
    return  TckList


class CpuUsage:
    def __init__(self):
        self._TckList    = GetCpuStat()

    def get(self):
        TckListPre       = self._TckList
        TckListNow       = GetCpuStat()
        self._TckList    = TckListNow
        CpuRateList = []
        for (TckNow, TckPre) in zip(TckListNow, TckListPre):
            TckDiff = [ Now - Pre for (Now , Pre) in zip(TckNow, TckPre) ]
            TckBusy = TckDiff[0]
            TckAll  = TckDiff[1]
            CpuRate = float(TckBusy*100/TckAll)
            CpuRateList.append( CpuRate )
        return CpuRateList


if __name__=='__main__':

    gCpuUsage = CpuUsage()      #initialize class CpuUsage
    vcgencmd_array = [[]]       #initialize vcgencmd_array
    #now_time_if = time.time()
    #start_time = time.time()
    #pre_time_if = 0
    try:
        while True:
            vcgencmd_array_tmp = []
            time.sleep(1.0)
            #get time
            now = datetime.datetime.now()
            now_str = now.strftime("%m/%d %H:%M:%S,%f")
            #now_time_if = time.time()
            #about cpu rate
            CpuRateList = gCpuUsage.get()
            CpuRate     = CpuRateList[0]
            CpuRate_str = "  CPU:%3d   " % CpuRate
            del CpuRateList[0]          #delete array for information of CpuRate
            #about Temp
            CpuTemp     = GetCpuTemp()
            CpuTemp_str = "Temp: %3.2f  ℃  " % CpuTemp
            #about Frequency
            CpuFreq     = float(GetCpuFreq()/1000000)
            CpuFreq_str = "ARM %4.5fMHz  " % CpuFreq
            #about volt
            CpuVolt     = GetCpuVolt()
            CpuVolt_str = "Volt: %3.6f  V" % CpuVolt
            #summarize all information
            Info_str = now_str + "   "+ CpuFreq_str + CpuTemp_str + CpuVolt_str + CpuRate_str  + "%"
            now = time.time()
            #if(start_time + 300 <= now):
            #    break
            #if(pre_time_if+2 <= now_time_if):
            print (Info_str, CpuRateList)
            #    pre_time_if = time.time()

            #make array for csv file
            #vcgencmd_array_tmp = [[now_str, CpuFreq, CpuTemp, CpuVolt, CpuRate]]
            if not any(vcgencmd_array):
                vcgencmd_array_tmp = [[now_str, CpuFreq, CpuTemp, CpuVolt, CpuRate]]
                vcgencmd_array = vcgencmd_array_tmp
            else:
                vcgencmd_array_tmp = [now_str, CpuFreq, CpuTemp, CpuVolt, CpuRate]
                vcgencmd_array.append(vcgencmd_array_tmp)


    except KeyboardInterrupt:
        print("interrputed")
        print(vcgencmd_array)
        print(len(vcgencmd_array))
        now = datetime.datetime.now()

        filename = "./log/" + now.strftime("%Y%m%d_%H%M") + ".csv"
        print(filename)
        with open(filename, "w") as f:
            writer = csv.writer(f, lineterminator='\n')
            field_names = ["time", "Frequency", "Temperature", "Power Consumption", "Cpu Rate"]

            writer.writerow(field_names)
            writer.writerows(vcgencmd_array)
