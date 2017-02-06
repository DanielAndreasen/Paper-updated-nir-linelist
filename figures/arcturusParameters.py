import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)
# sns.set_context('talk')


def weighted_avg_and_std(values, weights=None):
    """Get the weighted average and standard deviation.

    Input
    -----
    values : ndarray
      The list of values from which to calculate the weighted
      average and standard deviation

    Output
    ------
    average : float
      The weighted average
    std : float
      The weighted standard deviation
    """
    values = np.array(values)
    if weights is None:
        weights = (np.abs(values-np.median(values))/(np.std(values)+1E-13)+0.25)**(-1)
    average = round(np.average(values, weights=weights), 3)
    std = np.sqrt(np.average((values-average)**2, weights=weights))
    return average, std


def make_histogram(lit, val, err):

    lit = lit[~np.isnan(lit)]
    value, error = weighted_avg_and_std(val, 1/err)
    plt.hist(lit)
    _, y = plt.ylim()
    height = 0.90*y
    plt.vlines(value, 0, height)
    x1, x2 = value-error, value+error
    y1, y2 = 0, height
    plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], 'k', alpha=0.3)
    return y



if __name__ == '__main__':
    lit = pd.read_csv('arcturus_lit.csv')
    df = pd.read_csv('arcturus.csv')

    df1 = df[df.fixlogg]
    df2 = df[~df.fixlogg]
    params = ('teff', 'logg', 'feh', 'vt')
    for param in params:
        v1, e1 = weighted_avg_and_std(df1[param], 1/df1[param+'err'])
        v2, e2 = weighted_avg_and_std(df2[param], 1/df2[param+'err'])
        print 'Fixed logg'
        print param, round(v1, 2), round(e1, 2)
        print 'Free logg'
        print param, round(v2, 2), round(e2, 2)
        print ' '

    plt.subplot(311)
    y = make_histogram(lit.teff.values, df.teff, df.tefferr)
    plt.text(3800, 0.6*y, r'T$_\mathrm{eff}$', fontsize=20)
    plt.subplot(312)
    y = make_histogram(lit.logg.values, df.logg, df.loggerr)
    plt.text(0.88, 0.6*y, r'$\log(g)$', fontsize=20)
    plt.subplot(313)
    y = make_histogram(lit.feh.values, df.feh, df.feherr)
    plt.text(-0.82, 0.6*y, '[Fe/H]', fontsize=20)

    plt.tight_layout()
    # plt.savefig('ArcturusParams.pdf')
    plt.show()
