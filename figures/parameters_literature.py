from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from vt import vt
# import seaborn as sns
# sns.set_style('ticks')
# sns.set_context('paper', font_scale=1.7)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'



arcturus = {'lit':      [4247,  37, 1.59, 0.04, -0.54, 0.04, 1.30, 0.12],
            'loggFree': [4439,  62, 1.20, 0.20, -0.58, 0.06, 1.55, 0.10],
            'loggFix':  [4357,  74, 1.60, 0.14, -0.55, 0.04, 1.55, 0.10]}
leo      = {'lit':      [4741,  60, 2.76, 0.17, -0.03, 0.02, 1.45, 0.08],
            'loggFree': [4761, 118, 2.76, 0.48,  0.01, 0.07, 1.25, 0.11],
            'loggFix':  [4805,  98, 2.42, 0.61, -0.01, 0.07, 1.23, 0.10]}
hd20010  = {'lit':      [6152,  95, 3.96, 0.19, -0.27, 0.06, 1.17, 0.24],
            'loggFree': [6161, 164, 3.96, 0.53, -0.18, 0.11, 1.72, 0.44],
            'loggFix':  [6162, 184, 4.08, 0.77, -0.18, 0.11, 1.59, 0.49]}
stars = [arcturus, leo, hd20010]

fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(6, 8))
ax1.tick_params('x', labelcolor='w')
ax2.tick_params('x', labelcolor='w')
ax3.tick_params('x', labelcolor='w')
ax1.spines['top'].set_color('none')
ax1.spines['right'].set_color('none')
ax2.spines['top'].set_color('none')
ax2.spines['right'].set_color('none')
ax3.spines['top'].set_color('none')
ax3.spines['right'].set_color('none')
ax4.spines['top'].set_color('none')
ax4.spines['right'].set_color('none')

for number, star in enumerate(stars):
    ax1.errorbar(number-0.1, 0,                                  yerr=star['lit'][1],      fmt='o', color='C0')
    ax1.errorbar(number,     star['loggFix'][0] -star['lit'][0], yerr=star['loggFix'][1],  fmt='o', color='C1')
    ax1.errorbar(number+0.1, star['loggFree'][0]-star['lit'][0], yerr=star['loggFree'][1], fmt='o', color='C2')

    ax2.errorbar(number-0.1, 0,      yerr=star['lit'][3],      fmt='o', color='C0')
    ax2.errorbar(number,     star['loggFix'][2]-star['lit'][2],  yerr=star['loggFix'][3],  fmt='o', color='C1')
    ax2.errorbar(number+0.1, star['loggFree'][2]-star['lit'][2], yerr=star['loggFree'][3], fmt='o', color='C2')

    ax3.errorbar(number-0.1, star['lit'][4],      yerr=star['lit'][5],      fmt='o', color='C0')
    ax3.errorbar(number,     star['loggFix'][4],  yerr=star['loggFix'][5],  fmt='o', color='C1')
    ax3.errorbar(number+0.1, star['loggFree'][4], yerr=star['loggFree'][5], fmt='o', color='C2')

    ax4.errorbar(number-0.1, star['lit'][6],      yerr=star['lit'][7],      fmt='o', color='C0')
    ax4.errorbar(number,     star['loggFix'][6],  yerr=star['loggFix'][7],  fmt='o', color='C1')
    ax4.errorbar(number+0.1, star['loggFree'][6], yerr=star['loggFree'][7], fmt='o', color='C2')

# Labels
stars = ['Arcturus', '10 Leo', 'HD20010']
ax4.set_xticks(range(len(stars)))
ax4.set_xticklabels(map(lambda x: x.replace('.dat', ''), stars))
ax1.set_ylabel('Teff [K]')
ax2.set_ylabel('logg')
ax3.set_ylabel('[Fe/H]')
ax4.set_ylabel(r'$\xi_\mathrm{micro}$ [km/s]')

plt.tight_layout()
# plt.savefig('parameters.pdf')
plt.show()
