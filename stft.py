import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
import numpy as np
import math

def dataread(datapath):
	"""
	Read single wavform at datapath
	Args: 
        datapath(str) Path of the wavform
    Return:
        sig(list) wavform
        fs(int) sampling rate

	"""    
	# DIY
	fs, sig = wavfile.read(datapath)
	return sig, fs
    

def stft(x, fs, win, ov):
	"""
	Calculate stft of the signal
	Args:
 	    x(list) wavform
        win(int) the length of the frame
        ov(int) overlap between adjacent frames
	return:
        spectrogram(ndarray) 
        t(list) temporal axis
        f(list) frequency axis
	"""

	# DIY

    # hint)
    # for frame in x with overlap:
    #   x' = hanning(x)
    #   X = fft(x)
    #   stack X along with t axis

	# f : maximum value = Fs/2, gap between samples = Fs/2N
	# t : maximum value = len(x)/Fs, gap between samples = 1/Fs

	#set varible
	f = []
	t = []

	for i in range(win):
		f.append(fs/2*(i+1))

	for i in range(x.size):
		t.append(1/fs*(i+1))

	x_scale = int(x.size/win)
	x_index = 0
	hWindow = np.hanning(win)
	step_size = int(win - ov)

	spectrogram = np.zeros((x_scale, math.ceil(win/2)))
	x_hanned = np.empty(win)

	#calculate x' apply fft
	while x_index < x_scale:
		
		#calculate x'
		index_in_window = 0

		while index_in_window < win:
		
			i = win*x_index + index_in_window
	
			x_hanned[index_in_window] = x[i] * hWindow[index_in_window]
			index_in_window += 1

		#apply fft
		
		x_fft = np.fft.fft(x_hanned)
		x_fft = np.absolute(x_fft)

		spectrogram[x_index, :] = x_fft[:math.ceil(win/2)]

		if x_index == 0:
			print(x_fft)

		x_index += 1
	
	return spectrogram, t, f


def plot_stft(spectrogram, t, f): 
	"""
    Plot 2D image of spectrogram
    Args:
        spectrogram(ndarray):
	"""
	# DIY
	fig = plt.figure()
	spectrogram = spectrogram.T
	mini = spectrogram.min()
	maxi = spectrogram.max()

	im = plt.imshow(spectrogram, cmap=matplotlib.cm.coolwarm, origin='lower', vmin=mini, vmax=maxi)
	bar = plt.colorbar(im, ticks=[mini, maxi])
	fig.savefig('origin.png')

if __name__=='__main__':
    # Hyperparameters
	datapath = 'harvey_gonads.wav'
	sig, fs = dataread(datapath)
	win_size = int(25*1e-3*fs)
	overlap_size = int(10*1e-3*fs)

	print(sig.size/fs, fs/2)
	spec, t, f = stft(sig, fs, win_size, overlap_size)
	plot_stft(spec, t, f)
