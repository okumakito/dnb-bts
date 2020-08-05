def plot_fig02b(data_df):
  col_list = list('4567')
  deg_all_list = [calculate_deg(data_df['TSOD',t], data_df['TSOD-BTS',t]) \
                  for t in col_list]

  df = pd.DataFrame(0, index=data_df.index, columns=col_list)
  for week, deg_arr in zip(col_list, deg_all_list):
    print('{}w: {:>5d} genes'.format(week, len(deg_arr)))
    df.loc[deg_arr,week] = 1
  df = df[df.sum(axis=1) > 0]
  count_sr = df.apply(lambda x:''.join(x.astype(str)), axis=1).value_counts()
  
  d = 0.35 # short edge length
  d2 = d / np.sqrt(2) / 2 # unit
  cx, cy = (0.5, 0.5)

  # -------------------------------------------------------------------
  def draw_box(x, y, theta, ax, color):
    box = patches.FancyBboxPatch((x, y), d, 2*d,
                                 boxstyle='round,pad=0,rounding_size=0.05',
                                 alpha=0.3, fc=color, lw=0)
    trans = mpl.transforms.Affine2D().rotate_deg_around(x, y, theta) \
            + ax.transData
    box.set_transform(trans)
    ax.add_patch(box)

  def draw_edge(x, y, theta, ax, color):
    box = patches.FancyBboxPatch((x, y), d, 2*d,
                                 boxstyle='round,pad=0,rounding_size=0.05',
                                 fc='none', ec=color, lw=3)
    trans = mpl.transforms.Affine2D().rotate_deg_around(x, y, theta) \
            + ax.transData
    box.set_transform(trans)
    ax.add_patch(box)

  def put_text(x, y, s, ax):
    ax.text(x, y, s, ha='center', va='center', fontsize=15, color='k',
            path_effects=[patheffects.withStroke(linewidth=3,foreground='w')])

  # -------------------------------------------------------------------
  fig, ax = plt.subplots(figsize=(4,4))
  pal = sns.color_palette('tab10', 4)
  draw_box(  cx         , cy - 4 * d2,  45, ax, pal[1])
  draw_box(  cx - 2 * d2, cy - 2 * d2, -45, ax, pal[2])
  draw_edge( cx +     d2, cy - 3 * d2,  45, ax, pal[0])
  draw_edge( cx - 3 * d2, cy -     d2, -45, ax, pal[3])

  put_text(cx -     d2, cy + 2 * d2, count_sr.get('0100',0), ax)
  put_text(cx +     d2, cy + 2 * d2, count_sr.get('0010',0), ax)
  put_text(cx - 2 * d2, cy +     d2, count_sr.get('1100',0), ax)
  put_text(cx         , cy +     d2, count_sr.get('0110',0), ax)
  put_text(cx + 2 * d2, cy +     d2, count_sr.get('0011',0), ax)
  put_text(cx - 3 * d2, cy,          count_sr.get('1000',0), ax)
  put_text(cx - 1 * d2, cy,          count_sr.get('1110',0), ax)
  put_text(cx + 1 * d2, cy,          count_sr.get('0111',0), ax)
  put_text(cx + 3 * d2, cy,          count_sr.get('0001',0), ax)
  put_text(cx - 2 * d2, cy -     d2, count_sr.get('1010',0), ax)
  put_text(cx,          cy -     d2, count_sr.get('1111',0), ax)
  put_text(cx + 2 * d2, cy -     d2, count_sr.get('0101',0), ax)
  put_text(cx -     d2, cy - 2 * d2, count_sr.get('1011',0), ax)
  put_text(cx +     d2, cy - 2 * d2, count_sr.get('1101',0), ax)
  put_text(cx,          cy - 3 * d2, count_sr.get('1001',0), ax)

  put_text(cx - 3.8 * d2, cy +       d2, '4 w'  , ax)
  put_text(cx - 2   * d2, cy + 2.8 * d2, '5 w'  , ax)
  put_text(cx + 2   * d2, cy + 2.8 * d2, '6 w'  , ax)
  put_text(cx + 3.8 * d2, cy +       d2, '7 w'  , ax)

  ax.set_xticks([])
  ax.set_yticks([])
  sns.despine(left=True,bottom=True)

  fig.tight_layout()
  if in_ipython():
    fig.show()
    fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_fig02b(data_df)
