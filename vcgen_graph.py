import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import sys
from datetime import datetime as dt

INTERVAL_TIME = 30


args = sys.argv

csv_data = pd.read_csv(args[1])

#csv_data = pd.read_csv("./log/20200629_1658.csv")

time_data = np.array(csv_data[["time"]])
time_data = time_data.flatten()
Freq_data = np.array(csv_data[["Frequency"]])
Freq_data = Freq_data.flatten()
Temp_data = np.array(csv_data[["Temperature"]])
Temp_data = Temp_data.flatten()
Volt_data = np.array(csv_data[["Power Consumption"]])
Volt_data = Volt_data.flatten()
CpuRate_data = np.array(csv_data[["Cpu Rate"]])
CpuRate_data = CpuRate_data.flatten()

time_data = [dt.strptime(d, '%m/%d %H:%M:%S,%f') for d in time_data]


fig = plt.figure()

a = fig.add_subplot(411, title="Frequency", ylabel="MHz")
b = fig.add_subplot(412)
c = fig.add_subplot(413)
d = fig.add_subplot(414)
#e = fig.add_subplot(515)

a.plot(time_data, Freq_data)
#a.set_title('Frequency')
a.xaxis.set_major_locator(mdates.SecondLocator(interval=INTERVAL_TIME))
a.xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))

b.plot(time_data, Temp_data)
b.set_title('Temperature')
b.set_ylabel("℃")
b.xaxis.set_major_locator(mdates.SecondLocator(interval=INTERVAL_TIME))
b.xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))

c.plot(time_data, Volt_data)
c.set_title('Volts')
c.xaxis.set_major_locator(mdates.SecondLocator(interval=INTERVAL_TIME))
c.xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))

d.plot(time_data, CpuRate_data)
d.set_title('Cpu Rate')
d.xaxis.set_major_locator(mdates.SecondLocator(interval=INTERVAL_TIME))
d.xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))

plt.subplots_adjust(hspace=1.0)


plt.show()
