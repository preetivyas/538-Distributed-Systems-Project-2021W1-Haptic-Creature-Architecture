import numpy as np
import matplotlib.pyplot as plt



filename = 'b32768'
logpath = '../results/'
delays = []
times = []
with open(logpath+filename+'.log', 'r') as file:
    for line in file.readlines():
        if len(line.split(', ')) >= 3:
            time = float(line.split(', ')[1].rstrip())
            delay = float(line.split(', ')[2].rstrip())
            delays.append(delay)
            times.append(time)

delays = np.array(delays)
delays /= (10**6)

times = np.array(times)
times /= (10**6)
times = times - times[0]

delay_avg = np.mean(delays[20:])
print("Average delay (in seconds) is", delay_avg)

fig, ax = plt.subplots(1, 1)
ax.plot(times, delays, 'o-', label='Delays')
ax.set_xlabel('System Running Time (s)')
ax.set_ylabel('Delay Time (s)')
ax.set_title('Delays')

plt.legend()
plt.grid()
plt.show()
fig.savefig('../results/delays_'+filename+'.png')

fig, ax = plt.subplots(1, 1)

# Normalize the data to a proper PDF
delays = delays[20:]
delay_max = np.max(delays)
delay_sorted = np.sort(delays, axis=None)
delay_normalized = delay_sorted/(delay_sorted).sum()
delay_cdf = np.cumsum(delay_normalized) * 100

# Compute the CDF
ax.plot(delay_sorted, delay_cdf, 'o-', label='Delays CDF')
ax.set_xlabel('Delay Times (s)')
ax.set_ylabel('Percentile')
ax.set_title('Delay CDF')

plt.legend()
plt.grid()
plt.show()
fig.savefig('../results/delay_cdf_'+filename+'.png')