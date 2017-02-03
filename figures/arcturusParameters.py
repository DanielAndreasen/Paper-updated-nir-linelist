import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)
# sns.set_context('talk')


def make_histogram(lit, val, err):

    lit = lit[~np.isnan(lit)]

    plt.hist(lit)
    _, y = plt.ylim()
    height = 0.90*y
    plt.vlines(val, 0, height)
    for error, value in zip(err, val):
        x1, x2 = value-error, value+error
        y1, y2 = 0, height
        plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], 'k', alpha=0.3)
    return y



if __name__ == '__main__':
    lit = pd.read_csv('arcturus_lit.csv')
    df = pd.read_csv('arcturus.csv')

    plt.subplot(311)
    y = make_histogram(lit.teff.values, df.teff, df.tefferr)
    plt.text(3800, 0.6*y, r'T$_\mathrm{eff}$', fontsize=20)
    plt.subplot(312)
    y = make_histogram(lit.logg.values, df.logg, df.loggerr)
    plt.text(-1.30, 0.6*y, r'$\log(g)$', fontsize=20)
    plt.subplot(313)
    y = make_histogram(lit.feh.values, df.feh, df.feherr)
    plt.text(-0.82, 0.6*y, '[Fe/H]', fontsize=20)

    plt.tight_layout()
    # plt.savefig('ArcturusParams.pdf')
    plt.show()
