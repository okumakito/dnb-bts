import numpy as np
import pandas as pd
from utils import calculate_q
from scipy import stats

def calculate_deg_fold_change(data1_df, data2_df, fc_cutoff=1, 
                              alternative='two-sided'):
  """
  This function calculates differentially expressed genes (DEGs) 
  between two DataFrames or Series based on fold-change.

  Parameters
  ----------
  data1_df : DataFrame or Series
    gene expression data 1 (row: genes, col: samples)
  data2_df : DataFrame or Series
    gene expression data 2 (row: genes, col: samples)
  fc_cutoff : float, optional
    log2 fold-change cutoff. Default is 1.
  alternative : {'greater', 'less', 'two-sided'}, optional
    indicates the way to compare the two data. Default is 'two-sided'.

  Returns
  -------
  gene_arr : ndarray
    differentially expressed genes.
  
  """
  if data1_df.ndim == 2:
    diff_sr = data1_df.mean(axis=1) - data2_df.mean(axis=1)
  else:
    diff_sr = data1_df - data2_df
  if alternative == 'two-sided':
    gene_arr = diff_sr[diff_sr.abs() > fc_cutoff].index.values
  elif alternative == 'greater':
    gene_arr = diff_sr[diff_sr > fc_cutoff].index.values
  elif alternative == 'less':
    gene_arr = diff_sr[diff_sr < -fc_cutoff].index.values
  else:
    raise ValueError("<alternative> must be 'greater', 'less', or 'two-sided'.")
  return gene_arr

def calculate_deg_t_test(data1_df, data2_df, fdr=0.05,
                         alternative='two-sided'):
  """
  This function calculates differentially expressed genes (DEGs) 
  between two DataFrames based on T-test. False discovery rate 
  (FDR) control is used.

  Parameters
  ----------
  data1_df : DataFrame
    gene expression data 1 (row: genes, col: samples)
  data2_df : DataFrame
    gene expression data 2 (row: genes, col: samples)
  fdr : float, optional
    acceptable FDR. Default is 0.05.
  alternative : {'greater', 'less', 'two-sided'}, optional
    indicates the way to compare the two data. Default is 'two-sided'.

  Returns
  -------
  gene_arr : ndarray
    differentially expressed genes.
  
  """
  t_arr, p_arr = stats.ttest_ind(data1_df.T, data2_df.T, equal_var=False)
  if alternative == 'two-sided':
    pass
  elif alternative == 'greater':
    p_arr /= 2
    p_arr[t_arr < 0] = 1 - p_arr[t_arr < 0]
  elif alternative == 'less':
    p_arr /= 2
    p_arr[t_arr > 0] = 1 - p_arr[t_arr > 0]
  else:
    raise ValueError("<alternative> must be 'greater', 'less', or 'two-sided'.")
  return data1_df.index.values[calculate_q(p_arr) <= fdr]

def calculate_deg(data1_df, data2_df, fc_cutoff=1, fdr=0.05, 
                  alternative='two-sided', 
                  func=np.intersect1d):
  """
  This function calculates differentially expressed genes (DEGs) 
  between two DataFrames based on both fold-change and  T-test.
  T-test uses false discovery rate (FDR) control.

  Parameters
  ----------
  data1_df : DataFrame
    gene expression data 1 (row: genes, col: samples)
  data2_df : DataFrame
    gene expression data 2 (row: genes, col: samples)
  fc_cutoff : float, optional
    log2 fold-change cutoff. Default is 1.
  fdr : float, optional
    acceptable FDR. Default is 0.05.
  alternative : {'greater', 'less', 'two-sided'}, optional
    indicates the way to compare the two data. Default is 'two-sided'.
  func : callable, optional
    indicates the way to combine the genes obtained from fold-change
    analysis and T-test. Default is np.intersect1d.

  Returns
  -------
  gene_arr : ndarray
    differentially expressed genes.
  
  """
  gene_fc_arr = calculate_deg_fold_change(data1_df, data2_df, fc_cutoff, 
                                          alternative)
  gene_tt_arr = calculate_deg_t_test(data1_df, data2_df, fdr,
                                     alternative)
  return func(gene_fc_arr, gene_tt_arr)

  
if __name__ == '__main__':
  data1_df = pd.DataFrame(np.random.randn(1000,5))
  data2_df = pd.DataFrame(np.random.randn(1000,5) + 1.5)
  print(len(calculate_deg(data1_df, data2_df)))

