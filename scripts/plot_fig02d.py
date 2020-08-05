def plot_fig02d(file_name, width=6, height=6, wrap='y'):
  df = pd.read_csv(file_name, sep='\t',
                   usecols=['Category', 'Term', 'Count'])
  df = df.sort_values(by='Count', ascending=False).iloc[:10]
  category = df['Category'].iat[0]

  if 'GO' in category:
    df['Term'] = df['Term'].str.split('~').str[1]
    label = 'GO Term (Biological Process)'
    color = 'xkcd:steel blue'
    
  if 'KEGG' in category:
    df['Term'] = df['Term'].str.split(':').str[1]
    label = 'KEGG Pathway'
    color = 'xkcd:sand'

  if wrap == 'y':
    df['Term'] = df['Term'].str.wrap(30)
  df = df.rename(columns={'Term':label})

  with sns.axes_style('whitegrid'), sns.plotting_context('talk'):
    fig, ax = plt.subplots(figsize=(width,height))
    sns.barplot(data   = df,
                x      = 'Count',
                y      = label,
                orient = 'h',
                ci     = None,
                ax     = ax,
                color  = color)
    fig.tight_layout()
    if in_ipython():
      fig.show()
      fig.savefig('tmp.png')
    
  #print(df)
      
if __name__ == '__main__':
  file_name = sys.argv[1]
  width  = int(sys.argv[2])
  height = int(sys.argv[3])
  wrap = sys.argv[4]  # 'y' or 'n'
  plot_fig02d(file_name, width, height, wrap)
