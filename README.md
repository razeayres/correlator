# Correlator - machine learning module to create models
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.154379.svg)](https://doi.org/10.31223/osf.io/kj2vc)
###### *Rodrigo de Queiroga Miranda, and Josiclêda Domiciano Galvíncio*
###### Contact: rodrigo.qmiranda@gmail.com

### About
Correlator fits multiple modelss based on the combinations of input series; custom indices; transformation functions (logarithm, square root, reciprocal, and etc), and basic mathematical operations (+, -, *, and /). The models are calculated by using an exhaustive training iteration process  that selected the best results based on the highest coefficient of determination (r2) with the lowest Root Mean Square Error (RMSE). A threshold can be determined to avoid large files as output. The scripts were developed for the interpreter Python 2.7.15.

### Package usage
```r
python <input> <n_pars> <threshold> <n_procs>
```

Where ```r <input>``` is the input csv (comma delimited) file, ```r <n_pars>``` is the number of parameters used to develop the models, ```r <threshold>``` is the lowest r2 value that produces an output, ```r <n_procs>``` is the number of processors used to perform parallel optimizations.
