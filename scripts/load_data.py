def load_data():
  file_name = '../data/data.tsv'
  data_df = pd.read_csv(file_name, sep='\t', header=[0,1,2], index_col=0)
  data_df.columns = data_df.columns.droplevel(0)
  data_df = (data_df / stats.trim_mean(data_df, 0.02)).apply(np.log2)
  return data_df

def load_info():
  file_name = '../data/info.tsv'
  return pd.read_csv(file_name, sep='\t')

def load_dnb_list():
  file_name = '../data/dnb_list.txt'
  return pd.read_csv(file_name, header=None, index_col=0).index

if __name__ == '__main__':
  data_df = load_data()
  info_df = load_info()
  dnb_idx = load_dnb_list()
  
