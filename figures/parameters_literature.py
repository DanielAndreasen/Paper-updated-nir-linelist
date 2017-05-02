from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from vt import vt


if __name__ == '__main__':
    stars = glob('*.dat')

    for star in stars:
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
