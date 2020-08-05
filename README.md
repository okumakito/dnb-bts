# dnb-bts
This repository provides source codes used in the following work.

* K. Koizumi, M. Oku, S. Hayashi, A. Inujima, N. Shibahara, L. Chen, Y. Igarashi, K. Tobe, S. Saito, M. Kadowaki, and K. Aihara: Suppression of dynamical network biomarker signals at the pre-disease state (Mibyou) before metabolic syndrome in mice by a traditional Japanese medicine (Kampo formula) bofutsushosan, eCAM, 2020:9129134 (2020). https://doi.org/10.1155/2020/9129134

## Requirements

The source codes are written in Python 3. In addition, NumPy, SciPy, pandas, Matplotlib, seaborn, and NetworkX packages are required. All of them are included in Anaconda. Graphviz and graphviz, a python wrapper for Graphviz, are also required.

A gene expression data set GSE112653 is analyzed. Because the data size is large, the data set will not be included in this repository. Therefore, in order to run the source codes locally, please download the data set from [Gene Expression omnibus (GEO)](https://www.ncbi.nlm.nih.gov/geo/) database and put them into the *data* directory.
