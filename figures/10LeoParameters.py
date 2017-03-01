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
    std1 = np.sqrt(np.sum((1/weights)**2))/len(weights)
    return average, std, std1


def make_scatter(lit, df, parameter):

    df1 = df[df.fixlogg]
    df2 = df[~df.fixlogg]
    v1, e1, x1 = weighted_avg_and_std(df1[parameter], 1/df1[parameter+'err'])
    v2, e2, x2 = weighted_avg_and_std(df2[parameter], 1/df2[parameter+'err'])
    e1 = max([e1, x1])
    e2 = max([e2, x2])

    values, errors = lit[parameter], lit[parameter+'err']

    N = len(lit)
    plt.errorbar(range(N), values, yerr=errors, fmt='o')
    if parameter == 'logg':
        plt.errorbar([N+0, N+1], [v1, v2], yerr=[0, e2], fmt='o')
    else:
        plt.errorbar([N+0, N+1], [v1, v2], yerr=[e1, e2], fmt='o')
    _, y = plt.ylim()
    return y



if __name__ == '__main__':
    lit = pd.read_csv('10Leo_lit.csv')
    ref = ['Ref [%i]'%(i+1) for i in range(len(lit))]
    df = pd.read_csv('10Leo.csv', delimiter=r'\s+')


    plt.subplot(311)
    y = make_scatter(lit, df, 'teff')
    plt.ylabel(r'T$_\mathrm{eff}$')
    plt.xticks(range(len(ref)+2), [''*7])

    plt.subplot(312)
    y = make_scatter(lit, df, 'logg')
    plt.ylabel(r'$\log(g)$')
    plt.xticks(range(len(ref)+2), [''*7])

    plt.subplot(313)
    y = make_scatter(lit, df, 'feh')
    plt.ylabel('[Fe/H]')
    xtext = ref + ['fix logg', 'free logg']
    plt.xticks(range(len(ref)+2), xtext, rotation=45)

    plt.tight_layout()
    plt.savefig('10LeoParams.pdf')
    # plt.show()
