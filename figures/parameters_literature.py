from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from vt import vt
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


if __name__ == '__main__':
    stars = ('Arcturus.dat', '10Leo.dat', 'HD20010.dat')
    df_all = pd.read_csv('stellar_parameters.csv')
    df_all['star'] = map(lambda x: x.lower(), df_all['star'])

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, sharex=True)
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
        # Get the obtained parameters
        star_name = star.replace('.dat', '').lower()
        df_star = df_all[df_all['star'] == star_name]
        df_star1 = df_star[df_star.fixlogg]
        df_star2 = df_star[~df_star.fixlogg]

        # Get the literature values
        df = pd.read_table(star, na_values='--')
        df['vt'] = [vt(t, g, f) for t, g, f in df.loc[:, ('teff', 'logg', 'feh')].values]
        df.drop(['author', 'bibcode'], inplace=True, axis=1)
        d1 = df.loc[:, 'teff':'vt':2].apply(np.nanmedian)
        d2 = df.loc[:, 'teff':'vt':2].apply(np.nanstd)

        print 'Star: %s' % star.split('.')[0]
        print u'Teff = %d\u00B1%d' % (d1.teff, d2.teff)
        print u'logg = %.2f\u00B1%.2f' % (d1.logg, d2.logg)
        print u'feh = %.2f\u00B1%.2f' % (d1.feh, d2.feh)
        print u'vt = %.2f\u00B1%.2f\n' % (d1.vt, d2.vt)

        ax1.errorbar(number-0.1, d1.teff,       yerr=d2.teff*3,     fmt='o', color='C0')
        ax1.errorbar(number,     df_star1.teff, yerr=df_star1.tefferr, fmt='o', color='C1')
        ax1.errorbar(number+0.1, df_star2.teff, yerr=df_star2.tefferr, fmt='o', color='C2')

        ax2.errorbar(number-0.1, d1.logg,       yerr=d2.logg*3,     fmt='o', color='C0')
        ax2.errorbar(number,     df_star1.logg, yerr=df_star1.loggerr, fmt='o', color='C1')
        ax2.errorbar(number+0.1, df_star2.logg, yerr=df_star2.loggerr, fmt='o', color='C2')

        ax3.errorbar(number-0.1, d1.feh,       yerr=d2.feh*3,     fmt='o', color='C0')
        ax3.errorbar(number,     df_star1.feh, yerr=df_star1.feherr, fmt='o', color='C1')
        ax3.errorbar(number+0.1, df_star2.feh, yerr=df_star2.feherr, fmt='o', color='C2')

        ax4.errorbar(number-0.1, d1.vt,       yerr=d2.vt*3,     fmt='o', color='C0')
        ax4.errorbar(number,     df_star1.vt, yerr=df_star1.vterr, fmt='o', color='C1')
        ax4.errorbar(number+0.1, df_star2.vt, yerr=df_star2.vterr, fmt='o', color='C2')

    # Labels
    ax4.set_xticks(range(len(stars)))
    ax4.set_xticklabels(map(lambda x: x.replace('.dat', ''), stars))
    ax1.set_ylabel('Teff [K]')
    ax2.set_ylabel('logg')
    ax3.set_ylabel('[Fe/H]')
    ax4.set_ylabel(r'$\xi_\mathrm{micro}$ [km/s]')

    plt.tight_layout()
    # plt.savefig('parameters.pdf')
    plt.show()
