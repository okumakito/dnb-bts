import numpy as np

def calculate_q(p_seq):
  """
  Benjamini-Hochberg method
  """
  p_arr          = np.array(p_seq)
  n_genes        = len(p_arr)
  sort_index_arr = np.argsort(p_arr)
  p_sorted_arr   = p_arr[sort_index_arr]
  q_arr          = p_sorted_arr * n_genes / (np.arange(n_genes) + 1)
  q_min          = q_arr[-1]
  q_list         = [q_min]
  for q in q_arr[-2::-1]:
    if q < q_min:
      q_min = q
    q_list.append(q_min)
  q_arr = np.array(q_list)[::-1]
  q_arr[sort_index_arr] = q_arr.copy()
  return q_arr

if __name__ == '__main__':
  p_arr = np.random.rand(5)
  q_arr = calculate_q(p_arr)
  print('p-values', p_arr)
  print('q-values', q_arr)
