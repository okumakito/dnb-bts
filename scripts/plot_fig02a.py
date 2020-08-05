def plot_fig02a_sub(df, col_name, idx):

  sr = df[col_name]

  with sns.plotting_context('talk'):

    fig, ax = plt.subplots(figsize=(3,4))
    sns.boxplot(data      = df,
                x         = 'condition',
                y         = col_name,
                ax        = ax,
                showcaps  = False,
                palette   = ['xkcd:windows blue', 'xkcd:rose'])

    # significance
    t, p  = stats.ttest_ind(sr[df.condition == 'untreated'],
                            sr[df.condition == 'BTS'],
                            equal_var=False)
    y_max = sr.max()
    y_min = sr.min()
    y     = y_max + (y_max - y_min) * 0.1
    dy    = (y_max - y_min) * 0.05
    ax.plot([0,0,1,1],[y,y+dy,y+dy,y], c='0.35')
    ax.text(0.5, y+1.5*dy, 'p = {:.1E}'.format(p), ha='center', va='bottom',
            fontsize=12)

    ax.set_xlabel('')
    sns.despine()
    fig.tight_layout()
    if in_ipython():
      fig.show()
      fig.savefig('tmp{}.png'.format(idx))


def plot_fig02a(info_df):
  sub_df = info_df[info_df.condition != 'TSNO'].copy()
  sub_df.condition = sub_df.condition.str.replace('TSOD-BTS','BTS').\
                     str.replace('TSOD','untreated')
  sub_df = sub_df[sub_df.week == 7]
  for idx, col_name in enumerate(info_df.columns[4:6]):
    plot_fig02a_sub(sub_df, col_name, idx)

if __name__ == '__main__':
  plot_fig02a(info_df)
