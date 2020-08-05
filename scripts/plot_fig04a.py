def label_format(node_name):
  if len(node_name) <= 8:
    label = node_name
  else:
    label = node_name[:6] + '\\n' + node_name[6:]
  return label

def plot_fig04a(network_file, gene_file, dnb_idx):
  layout = 'fdp'  # dot(default), twopi, fdp, sfdp(bad), neato
  color_dnb    = 'white:#f5da81'
  color_deg    = 'white:#a9d0f5'
  color_border = 'gray'
  color_edge   = mpl.colors.to_hex('xkcd:medium grey')

  nw_df = pd.read_csv(network_file, sep='\t',
                      usecols=['#node1', 'node2'])
  nw_df.columns = ['src', 'dst']

  # correct alias names
  gene_sr = pd.read_csv(gene_file, header=None)
  gene_arr = np.unique(np.reshape(nw_df.values, -1))
  print(np.setdiff1d(gene_arr, gene_sr))
  alias_dict = {'Dnajb8':             '1700031F10Rik',
                'ENSMUSG00000040163': '1700034J05Rik',
                'ENSMUSG00000045330': '4933402E13Rik',
                'Gm13308':            'Gm20878',
                'H2-T3':              'H3-T18',
                'Ppyr1':              'Npy4r'}
  nw_df.replace(alias_dict, inplace=True)

  # take dnbs and degs included in the network
  gene_arr = np.unique(np.reshape(nw_df.values, -1))
  dnb_arr  = dnb_idx.values.copy()
  dnb_arr  = np.intersect1d(dnb_arr, gene_arr)
  deg_arr  = np.setdiff1d(gene_arr, dnb_arr)

  # take connected components that contains both dnb(s) and deg(s).
  G = nx.from_pandas_edgelist(nw_df, 'src', 'dst')
  G2 = G.copy()
  for node_set in nx.connected_components(G):
    if ~np.in1d(list(node_set), dnb_arr).any() or \
       ~np.in1d(list(node_set), deg_arr).any() or \
       len(node_set) <= 2:
      G2.remove_nodes_from(node_set)
    elif 'Il31' in node_set:
      pd.Series(list(node_set)).to_csv('tmp.txt', index=False)
  G = G2.copy()
  del G2

  g = gv.Graph(format='png', engine=layout)
  g.body.extend(['size="7"', 'overlap="false"', 'splines="false"', 
                 'outputorder="edgesfirst"'])
  g.node_attr.update(shape='circle', fixedsize='true', width='1.2', 
                     style='filled', fontsize='16',
                     fontname='monospace Italic',
                     gradientangle='315', color=color_border)
  g.edge_attr.update(penwidth='3', color=color_edge)

  for src, dst in G.edges():
    g.edge(src, dst)

  for node in G.nodes():
    if node in dnb_arr:
      g.node(node, label=label_format(node), fillcolor=color_dnb)
    else:
      g.node(node, label=label_format(node), fillcolor=color_deg)

  g.render(filename='tmp')

  return G
  

if __name__ == '__main__':
  network_file = sys.argv[1]  # ../data/network/network.tsv
  gene_file    = sys.argv[2]  # ../data/network/gene_list.txt
  G = plot_fig04a(network_file, gene_file, dnb_idx)
