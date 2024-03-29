from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)
from plot_fits import get_wavelength, dopplerShift
from scipy.interpolate import interp1d
plt.rcParams['xtick.direction'] = 'in'

"""
Compare the spectrum of Arcturus with 10 Leo, plus have some Fe lines
identified.
"""


def get_ymin(center, d1, d2):

    w1, f1 = d1
    i1 = np.argmin(abs(w1-center))
    v1 = f1[i1]

    w2, f2 = d2
    i2 = np.argmin(abs(w2-center))
    v2 = f2[i2]

    return min([v1])


if __name__ == '__main__':
    regions = [[10000, 10100], [10130, 10230], [12200, 12300]]

    lines = np.loadtxt('Felines.moog', usecols=(0,))
    wArcturus = get_wavelength(fits.getheader('ArcturusSummer.fits'))
    fArcturus = fits.getdata('ArcturusSummer.fits')

    w10Leo1 = get_wavelength(fits.getheader('10LeoYJ.fits'))
    f10Leo1 = fits.getdata('10LeoYJ.fits')
    w10Leo2 = get_wavelength(fits.getheader('10LeoH.fits'))
    f10Leo2 = fits.getdata('10LeoH.fits')
    w10Leo3 = get_wavelength(fits.getheader('10LeoK.fits'))
    f10Leo3 = fits.getdata('10LeoK.fits')

    f10Leo1, w10Leo1 = dopplerShift(w10Leo1, f10Leo1, -82.53)
    f10Leo2, w10Leo2 = dopplerShift(w10Leo2, f10Leo2, -81.82)
    f10Leo3, w10Leo3 = dopplerShift(w10Leo3, f10Leo3, -81.37)

    for i, region in enumerate(regions):
        if i != 1:
            continue
        if (w10Leo1[0] <= region[0]) and (w10Leo1[-1] >= region[1]):
            w10Leo = w10Leo1
            f10Leo = f10Leo1
        elif (w10Leo2[0] <= region[0]) and (w10Leo2[-1] >= region[1]):
            w10Leo = w10Leo2
            f10Leo = f10Leo2
        elif (w10Leo3[0] <= region[0]) and (w10Leo3[-1] >= region[1]):
            w10Leo = w10Leo3
            f10Leo = f10Leo3
        else:
            continue
        i1 = (region[0] <= wArcturus) & (wArcturus <= region[1])
        i2 = (region[0] <= w10Leo) & (w10Leo <= region[1])
        i3 = (region[0] <= lines) & (lines <= region[1])

        w1, f1 = wArcturus[i1], fArcturus[i1]
        w2, f2 = w10Leo[i2], f10Leo[i2]
        plines = lines[i3]

        w0 = w1[0] if w1[0] != min((w1[0], w2[0])) else w2[0]
        wn = w1[-1] if w1[-1] != max((w1[-1], w2[-1])) else w2[-1]

        interp1 = interp1d(w1, f1, kind='linear')
        interp2 = interp1d(w2, f2, kind='linear')
        w = np.linspace(w0, wn, len(w1))
        f1 = interp1(w)
        f2 = interp2(w)

        fig = plt.figure(figsize=(12, 5))
        ax = fig.add_subplot(111)
        ax.tick_params('y', labelcolor='w', left='off')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        ax.plot(w, f1, label='Arcturus')
        ax.plot(w, f2-0.15, label='10 Leo')
        ax.plot(w, f1-f2+0.15, label='Difference')
        for j, line in enumerate(plines):
            if j%2 == 0:
                dy = -0.02
            else:
                dy = 0.02
            if j == 6:
                dy = 0.02
            elif j == 7:
                dy = -0.02
            ymin = get_ymin(line, (w1, f1), (w2, f2))
            plt.vlines(line, ymin, 1.04+dy, linestyles='dashed')
            plt.text(line, 1.04+dy, 'Fe')
        ax.set_xlabel(r'Wavelength [$\AA$]')
        ax.set_ylabel('Normalized flux')

        y1, _ = plt.ylim()
        plt.ylim(y1, 1.15)
        plt.legend(loc='best', frameon=False)
        plt.tight_layout()
    # plt.savefig('bothspectra.pdf')
    plt.show()
