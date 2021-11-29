import numpy as np
import matplotlib.pyplot as plt



logpath = '../results/actuator_1.log'
delays = []
with open(logpath, 'r') as file:
    for line in file.readlines():
        if len(line.split(', ')) >= 3:
            delay = float(line.split(', ')[2].rstrip())
            delays.append(delay)

delays = np.array(delays)
delays /= (10**6)

size = delays.shape[0]
period = 0.1
duration = size * period
times = np.linspace(0, duration, size)

delay_avg = np.mean(delays[20:])
print("Average delay (in secoonds) is", delay_avg)

fig, ax = plt.subplots(1, 1)
ax.plot(times, delays, 'o-', label='Delays')
ax.set_xlabel('System Running Time (s)')
ax.set_ylabel('Delay Time (s)')
ax.set_title('Delays')

plt.legend()
plt.grid()
plt.show()
fig.savefig('../results/delays.png')

fig, ax = plt.subplots(1, 1)

# Normalize the data to a proper PDF
delays = delays[20:]
delay_max = np.max(delays)
delay_sorted = np.sort(delays, axis=None)
delay_normalized = delay_sorted/(delay_sorted).sum()
delay_cdf = np.cumsum(delay_normalized)

# Compute the CDF
ax.plot(delay_sorted, delay_cdf, 'o-', label='Delays CDF')
ax.set_xlabel('Delay Times (s)')
ax.set_ylabel('Percentile')
ax.set_title('Delay CDF')

plt.legend()
plt.grid()
plt.show()
fig.savefig('../results/delay_cdf.png')