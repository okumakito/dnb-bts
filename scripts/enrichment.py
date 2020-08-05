def enrichment(file_name):
  df = pd.read_csv(file_name, sep='\t',
                   usecols=['Category', 'Term','Count','List Total',
                            'Pop Hits','Pop Total'])
  n_test = df.shape[0]
  p_list = []
  for i, (_, term, x, n1, n2, N) in df.iterrows():
      p_list.append(stats.hypergeom.sf(x-1, N, n1, n2))
  q_arr = calculate_q(p_list)
  df['p-value'] = p_list
  df['q-value'] = q_arr
  df = df[df['q-value'] <= 0.05]
  df.sort_values('Count', inplace=True, ascending=False)
  df.to_csv('tmp.tsv', sep='\t', index=False)
    
if __name__ == '__main__':
  file_name = sys.argv[1]
  enrichment(file_name)
