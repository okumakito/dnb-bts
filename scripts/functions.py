import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys
import subprocess
import networkx as nx
import graphviz as gv
from scipy import stats
from scipy.cluster.hierarchy import distance, linkage, fcluster
from matplotlib import patches, patheffects
from utils import calculate_deg, calculate_q

mpl.rcParams['font.sans-serif'] = 'DejaVu Sans'

# short functions ----------------------------------------

def in_ipython():
  return 'TerminalIPythonApp' in get_ipython().config

def corr_inter(X, Y):
  # X (n x p1), Y (n x p2)
  X_normed = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
  Y_normed = (Y - Y.mean(axis=0)) / Y.std(axis=0, ddof=0)
  return np.dot(X_normed.T, Y_normed) / X.shape[0]

def plot_gene(gene_name):
  long_form_df = data_df.loc[gene_name].reset_index()
  fig, ax = plt.subplots()
  sns.swarmplot(data=long_form_df, x='week', y=gene_name,
                hue='condition', dodge=True)

def correlation_adjust():
  p1 = 10**4
  p2 = 10**3
  for n in [3,4,5]:
    res = np.abs(corr_inter(np.random.randn(n, p1), np.random.randn(n, p2)))
    print('n={}, correlation strength = {:.4f} +- {:.4f}'.
          format(n, np.mean(res), stats.sem(res, axis=None)))

# BTS part ----------------------------------------

def fisher_exact_test_dnb(data_df, dnb_idx, df):
  set_pop = data_df.index # 24217
  set1    = dnb_idx       # 147
  set2    = df.index      # 696
  print('p-val =', stats.hypergeom.sf(len(np.intersect1d(set1, set2)) -1,
                                      len(set_pop), len(set1), len(set2)))
  print('expected overlap =', len(set1) * len(set2) / len(set_pop))

def merge_dnb_and_deg(data_df, dnb_idx, clust_sr):
  deg6, deg7 = [calculate_deg(data_df['TSOD',t], data_df['TSOD-BTS',t]) \
                for t in list('67')]
  deg67 = np.intersect1d(deg6, deg7)
  print('deg at 6 w', len(deg6))
  print('deg at 7 w', len(deg7))
  print('deg at 6w and 7w', len(deg67))
  c1 = clust_sr[clust_sr==1].index
  deg67c1 = np.intersect1d(deg67, c1)
  print('deg at cluster 1', len(c1))
  print('deg at 6w, 7w, and cluster 1', len(deg67c1))
  print('overlap with dnb', np.intersect1d(dnb_idx, deg67c1))
  pd.Series(np.union1d(dnb_idx, deg67c1)).to_csv('tmp.txt', index=False)

def dnb_std_count(data_df, dnb_idx):
  sr1 = data_df.loc[dnb_idx, ('TSOD','5')].std(axis=1)
  sr2 = data_df.loc[dnb_idx, ('TSNO','5')].std(axis=1)
  sr3 = data_df.loc[dnb_idx, ('TSOD-BTS','5')].std(axis=1)

  fig, ax = plt.subplots()
  sns.distplot(sr1/sr2, ax=ax, kde=False)
  sns.distplot(sr3/sr2, ax=ax, kde=False)
  fig.show()
  
  fig2, ax2 = plt.subplots()
  sns.distplot(sr3/sr1, ax=ax2, kde=False)
  fig2.show()

  print(sr3.mean()/sr1.mean())
  print(sr3[sr3 < sr1].shape, sr3[sr3 > sr1].shape)
  print(sr3[sr3 < 0.5*sr1].shape, sr3[sr3 > 2*sr1].shape)
  

if __name__ == '__main__':
  pass
