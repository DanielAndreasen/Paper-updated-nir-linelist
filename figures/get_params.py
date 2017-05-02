import numpy as np
import pandas as pd


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


if __name__ == '__main__':

    stars = ('10Leo.csv', 'arcturus.csv', 'HD20010.csv')
    columns = 'star,teff,tefferr,logg,loggerr,feh,feherr,vt,vterr,fixlogg'.split(',')
    df = pd.DataFrame(index=range(2*len(stars)), columns=columns)
    df.fillna(0, inplace=True)

    idx = 0
    for star in stars:
        df_star = pd.read_csv(star)
        df1 = df_star[df_star.fixlogg]
        df2 = df_star[~df_star.fixlogg]
        df.loc[idx, 'star'] = star.replace('.csv', '')
        df.loc[idx+1, 'star'] = star.replace('.csv', '')
        for parameter in df_star.loc[:, 'teff':'vt':2].columns:
            v1, e1, x1 = weighted_avg_and_std(df1[parameter], 1/df1[parameter+'err'])
            v2, e2, x2 = weighted_avg_and_std(df2[parameter], 1/df2[parameter+'err'])
            e1 = max([e1, x1])
            e2 = max([e2, x2])

            df.loc[idx, parameter] = v1
            df.loc[idx, parameter+'err'] = e1
            df.loc[idx, 'fixlogg'] = False

            df.loc[idx+1, parameter] = v2
            df.loc[idx+1, parameter+'err'] = e2
            df.loc[idx+1, 'fixlogg'] = True

        idx += 2
    df.to_csv('stellar_parameters.csv', index=False)
