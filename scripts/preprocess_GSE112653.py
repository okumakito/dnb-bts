import numpy as np
import pandas as pd

def preprocess_GSE112653():

  # NOTE: the mapping relations between probe names and gene symbols
  # were extracted from 028005_D_GeneList_20171030.txt obtained at
  # https://earray.chem.agilent.com/earray/catalogGeneLists.do?action=displaylist
  # It was the latest at the momemnt of the paper submission.
  data_file_name = '../data/GSE112653_series_matrix.txt'
  mapping_file_name = '../data/id_mapping.tsv' 
  output_file_name = '../data/data.tsv'

  # find !Sample_title ----------------------------------------

  with open(data_file_name, 'r') as f:
    for i, line in enumerate(f):
      if line.startswith('!Sample_title'):
        break
  header_lines = [i -1, i + 35] # '!Sample_title', 'ID_REF'

  # load expression data file ---------------------------------

  df = pd.read_csv(data_file_name, sep='\t', index_col=0,
                   low_memory=False, header=header_lines)
  df.drop('!series_matrix_table_end', inplace=True) # => 62976 x 64
  df.index = df.index.astype(int)

  # rename columns ------------------------------------------------

  col_idx         = df.columns.get_level_values(0)
  condition_idx   = col_idx.str.split('_').str[0]
  week_idx        = col_idx.str.split('_').str[1].str.replace('w','')
  df.columns = [np.arange(len(col_idx)), condition_idx, week_idx]
  df.columns.names = ['sample_no', 'condition', 'week']
  
  # id conversion -------------------------------------------------

  mapping_sr = pd.read_csv(mapping_file_name, sep='\t',
                           usecols=['FeatureNum', 'GeneSymbol'],
                           index_col=0, squeeze=True).dropna()
  df = df.loc[mapping_sr.index].rename(mapping_sr)
  df = df.groupby(axis=0,level=0).mean()
  df.index.name = 'gene_symbol'

  # save to file -------------------------------------------------

  df.to_csv(output_file_name, sep='\t')

if __name__ == '__main__':
  preprocess_GSE112653()
