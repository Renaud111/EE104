import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy.fftpack import fft
from scipy.io import wavfile
import sys, os, os.path
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import scipy.io.wavfile
(rate,snd)=scipy.io.wavfile.read("268074__skowm001__3-tone-chime.wav")
plt.plot(snd)



'''plot the frequency domain graph of wav'''
fs_rate, signal = wavfile.read("268074__skowm001__3-tone-chime.wav")
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print ("Channels", l_audio)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2
N = signal.shape[0]
print ("Complete Samplings N", N)
secs = N / float(fs_rate)
print ("secs", secs)
Ts = 1.0/fs_rate # sampling interval in time
print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts) # time vector as scipy arange field / numpy.ndarray
FFT = abs(scipy.fft(signal))
FFT_side = FFT[range(N//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)] # one side frequency range
fft_freqs_side = np.array(freqs_side)
plt.subplot(311)
p1 = plt.plot(t, signal, "g") # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.subplot(312)
p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')
plt.subplot(313)
p3 = plt.plot(freqs_side, abs(FFT_side), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
plt.show()

ssize=2**16
fwin=np.hamming(ssize)

ff=np.fft.rfft(snd[:ssize])
def ffunc(ix,cutoff):
    if ix < cutoff:
        return 1.0
    return 0.0

filt=[ffunc(ix,len(ff)/20) for ix in range(len(ff))]
plt.plot(filt)
plt.show()

ff=[ff[ix]*filt[ix] for ix in range(len(ff))]

fsamp=np.fft.irfft(ff)

plt.plot(fsamp[:ssize])
plt.show()
filt_res=np.array([])
def fft_slice(startloc,fracbw):
    global filt_res
    ff=np.fft.rfft(snd[startloc:ssize+startloc])
    filt=[ffunc(ix,len(ff)/fracbw) for ix in range(len(ff))]
    ff=[ff[ix]*filt[ix] for ix in range(len(ff))]
    fsamp=np.fft.irfft(ff)
    filt_res=np.append(filt_res,fsamp)


filt_res=np.array([])
for startit in range(0,len(snd),ssize):
    fft_slice(startit,50)



plt.plot(filt_res)
plt.show()
sf=max(snd)
filt_scale=[filt_res[ix]/sf for ix in range(len(filt_res))]
filt_scale=np.array(filt_scale)
scipy.io.wavfile.write("changed_268074__skowm001__3-tone-chime.wav",rate,filt_scale)

filt_scale[3]





'''plot the changed wav'''
fs_rate, signal = wavfile.read("changed_268074__skowm001__3-tone-chime.wav")
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print ("Channels", l_audio)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2
N = signal.shape[0]
print ("Complete Samplings N", N)
secs = N / float(fs_rate)
print ("secs", secs)
Ts = 1.0/fs_rate # sampling interval in time
print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts) # time vector as scipy arange field / numpy.ndarray
FFT = abs(scipy.fft(signal))
FFT_side = FFT[range(N//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)] # one side frequency range
fft_freqs_side = np.array(freqs_side)
plt.subplot(311)
p1 = plt.plot(t, signal, "g") # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.subplot(312)
p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')
plt.subplot(313)
p3 = plt.plot(freqs_side, abs(FFT_side), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
plt.show()




'''convert changed wav to csv'''
input_filename = "changed_268074__skowm001__3-tone-chime.wav"
if input_filename[-3:] != 'wav':
    print('WARNING!! Input File format should be *.wav')
    sys.exit()

samrate, data = wavfile.read(str(input_filename))
print('Load is Done! \n')

wavData = pd.DataFrame(data)

if len(wavData.columns) == 2:
    print('Stereo .wav file\n')
    wavData.columns = ['R', 'L']
    stereo_R = pd.DataFrame(wavData['R'])
    stereo_L = pd.DataFrame(wavData['L'])
    print('Saving...\n')
    stereo_R.to_csv(str(input_filename[:-4] + "_Output_stereo_R.csv"), mode='w')
    stereo_L.to_csv(str(input_filename[:-4] + "_Output_stereo_L.csv"), mode='w')
    # wavData.to_csv("Output_stereo_RL.csv", mode='w')
    print('Save is done ' + str(input_filename[:-4]) + '_Output_stereo_R.csv , '
                          + str(input_filename[:-4]) + '_Output_stereo_L.csv')

elif len(wavData.columns) == 1:
    print('Mono .wav file\n')
    wavData.columns = ['M']

    wavData.to_csv(str(input_filename[:-4] + "_Output_mono.csv"), mode='w')

    print('Save is done ' + str(input_filename[:-4]) + '_Output_mono.csv')

else:
    print('Multi channel .wav file\n')
    print('number of channel : ' + len(wavData.columns) + '\n')
    wavData.to_csv(str(input_filename[:-4] + "Output_multi_channel.csv"), mode='w')

    print('Save is done ' + str(input_filename[:-4]) + 'Output_multi_channel.csv')

plt.show()
