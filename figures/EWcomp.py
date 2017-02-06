import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')
sns.set_context('paper', font_scale=1.7)


def read_moog(fname):
    n = ['w', 'e', 'ep', 'gf', 'ew']
    return pd.read_csv(fname, delimiter=r'\s+', names=n, skiprows=1)


if __name__ == '__main__':
    df_ares = read_moog('arcturus.moog')
    df_summer = read_moog('ArcturusSummer.moog')
    df_winter = read_moog('ArcturusWinter.moog')

    # Summer winter comparison (IRAF)
    df1 = pd.merge(df_summer, df_winter, left_on='w', right_on='w')
    # Summer ARES comparison
    df2 = pd.merge(df_summer, df_ares, left_on='w', right_on='w')

    plt.subplot(211)
    plt.plot(df1.ew_x, df1.ew_y, 'o')
    plt.plot([0, 1.1*max(df1.ew_x)], [0, 1.1*max(df1.ew_x)], '--k')
    y = plt.ylim()
    plt.title(r'Winter vs. summer, EW [m$\AA$]')

    plt.subplot(212)
    plt.plot(df2.ew_x, df2.ew_y, 'o')
    plt.plot([0, 1.1*max(df2.ew_x)], [0, 1.1*max(df2.ew_x)], '--k')
    plt.ylim(y)
    plt.xlabel(r'Summer observation, EW [m$\AA$]')
    plt.title(r'Automatic vs. summer, EW [m$\AA$]')

    plt.tight_layout()
    # plt.savefig('EWcomp.pdf')
    plt.show()
