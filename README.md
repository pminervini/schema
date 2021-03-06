# Link Prediction with Schema-Aware Energy-Based Models for Knowledge Graphs

Prerequisites:

    # apt-get install build-essential git gfortran python-dev python-setuptools python-pip python-numpy python-scipy python-sklearn python-pandas cython libblas-dev libopenblas-dev libatlas-base-dev liblapack-dev parallel
    # pip install --upgrade git+git://github.com/Theano/Theano.git
    # pip install --upgrade scikit-learn pymongo patsy seaborn termcolor

The following commands use GNU Parallel for executing multiple experiments (default: 8) at the same time.

## Evaluating the Schema-Aware Energy Functions:

Freebase (FB15k):

    $ ./scripts/fb15k_schema/fb15k_schema.py | parallel -j 8

WordNet:

    $ ./scripts/music_schema/music_schema.py | parallel -j 8

Validation and test results will be stored in directories logs/fb15k_schema/ and logs/music_schema/.

## Triple Classification experiments:

Freebase (FB13):

    $ ./scripts/fb13_classification/fb13_classification.py | parallel -j 8

WordNet (WN11):

    $ ./scripts/wn11_classification/wn11_classification.py | parallel -j 8

Validation and test results will be stored in directories logs/fb13_classification/ and logs/wn11_classification/.

## Link Prediction experiments:

Freebase (FB15k):

    $ ./scripts/fb15k_lp/fb15k_lp.py | parallel -j 8

WordNet (WN18):

    $ ./scripts/wn18_lp/wn18_lp.py | parallel -j 8

Validation and test results will be stored in directories logs/fb15k_lp/ and logs/wn18_lp/.

## Comparing the Optimization Criteria:
### (by comparing the behaviour of the loss functional with each of them)

Freebase (FB15k):

    $ ./scripts/fb15k_optimization/fb15k_optimal.py | parallel -j 8

WordNet:

    $ ./scripts/wn_optimization/wn_optimal.py | parallel -j 8

Visualizing the minimization of the loss functional using different adaptive learning rate selection criteria:

    $ BEST_K=1 ./show_losses.py models/wn18_optimal/*.pkl -show
    $ BEST_K=1 LOSS_THR=10000 ./show_losses.py models/fb15k_optimal/*.pkl -show

![Visualization](http://slides.neuralnoise.com/schema/schema.png)
