def plot_fig03(data_df, dnb_idx):

  shift_dic = {3:0.64, 4:0.50, 5:0.42}

  stat_df = pd.DataFrame(index=['condition',
                                'week',
                                'average standard deviation $I_s$',
                                'average correlation strength $I_r$'])
  for i, (col, df) in enumerate(data_df.groupby(axis=1, level=[0,1])):

    shift   = shift_dic[df.shape[1]]
    std_val = df.loc[dnb_idx].std(axis=1).mean()
    corr_df = df.loc[dnb_idx].T.corr().abs()
    np.fill_diagonal(corr_df.values, None)
    corr_val = corr_df.mean().mean() - shift
    stat_df[i] = [col[0], col[1], std_val, corr_val]

  stat_df = stat_df.T
  stat_df = stat_df[stat_df['condition'] != 'TSNO']
  stat_df.condition = stat_df.condition.str.replace('TSOD-BTS','BTS').\
                      str.replace('TSOD','untreated')
   
  with sns.plotting_context('talk'):

    w, h = (5,4)
    kws = dict(data=stat_df,
               x='week',
               hue='condition', 
               legend=False,
               hue_order = ['untreated', 'BTS'], 
               palette   = ['xkcd:windows blue', 'xkcd:rose'],
               aspect=w/h,
               size=h)
    g1 = sns.factorplot(y=stat_df.columns[2], **kws)
    g2 = sns.factorplot(y=stat_df.columns[3], **kws)
    for i, g in enumerate([g1, g2]):
      g.ax.legend(frameon=False, loc='upper left')
      if in_ipython():
        g.fig.show()
        g.fig.savefig('tmp{}.png'.format(i))

      
if __name__ == '__main__':
  plot_fig03(data_df, dnb_idx)
