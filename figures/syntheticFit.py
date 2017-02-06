
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from PyAstronomy import pyasl
import os
import sys
sys.path.append('/home/daniel/Documents/Uni/phdproject/programs/FASMA')
from interpolation import interpolator
from plot_fits import get_wavelength, dopplerShift
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)


def create_synthetic(star):
    if star == 'Arcturus':
        os.system('cp arc.atm out.atm')
    else:
        os.system('cp 10Leo.atm out.atm')
    os.system('MOOGSILENT < stupid.tmp')
    w, f = np.loadtxt('synth.asc', skiprows=2, unpack=True)
    os.system('rm -f out?')
    return w, f



if __name__ == '__main__':
    region = [10130, 10227]
    lines = np.loadtxt('/home/daniel/.plotfits/linelist.moog', usecols=(0,))


    # 10 Leo (4821, 2.41, 0.04, 1.26)
    w10Leo = get_wavelength(fits.getheader('10LeoYJ.fits'))
    f10Leo = fits.getdata('10LeoYJ.fits')
    f10Leo, w10Leo = dopplerShift(w10Leo, f10Leo, -82.53)
    idx = (region[0] <= w10Leo) & (w10Leo <= region[1])
    w10Leo, f10Leo = w10Leo[idx], f10Leo[idx]
    w1, f1 = create_synthetic('10 Leo')
    f1 = pyasl.rotBroad(w1, f1, 0.40, 5)

    # Arcturus (4269, 1.69, 1.41, -0.46)
    warc = get_wavelength(fits.getheader('ArcturusSummer.fits'))
    farc = fits.getdata('ArcturusSummer.fits')
    idx = (region[0] <= warc) & (warc <= region[1])
    warc, farc = warc[idx], farc[idx]
    w2, f2 = create_synthetic('Arcturus')
    f2 = pyasl.rotBroad(w2, f2, 0.40, 4.5)

    plt.figure(figsize=(12, 5))
    plt.subplot(211)
    plt.plot(warc, farc, label='Arcturus')
    plt.plot(w2, f2, '--r', label='Synthetic')
    plt.legend(loc='lower left', frameon=False)

    plt.subplot(212)
    plt.plot(w10Leo, f10Leo, label='10 Leo')
    plt.plot(w1, f1, '--r', label='Synthetic')
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.legend(loc='lower left', frameon=False)
    plt.tight_layout()

    # plt.savefig('syntheticFit.pdf')
    plt.show()
