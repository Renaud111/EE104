# Supraventricular tachycardia infant heart rate
#import packages
import heartpy as hp
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sample_rate = 50000

data = hp.get_data('output.csv')

plt.figure(figsize=(12,4))
plt.plot(data)
plt.show()

#run analysis
wd, m = hp.process(data, sample_rate)

#visualise in plot of custom size
plt.figure(figsize=(12,4))
hp.plotter(wd, m)
plt.show()
#display computed measures
for measure in m.keys():
    print('%s: %f' %(measure, m[measure]))

plt.show()