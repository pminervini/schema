# schema

Prerequisites:

    # apt-get install build-essential git gfortran python-dev python-setuptools python-pip python-numpy python-scipy python-sklearn python-pandas cython libblas-dev libopenblas-dev libatlas-base-dev liblapack-dev parallel
    # pip install --upgrade git+git://github.com/Theano/Theano.git
    # pip install --upgrade scikit-learn pymongo patsy seaborn termcolor

The following commands use GNU Parallel for executing multiple experiments (default: 8) at the same time.

# Evaluating the Schema-Aware Energy Functions:

Freebase (FB15k):

    $ ./scripts/fb15k_schema/fb15k_schema.py | parallel -j 8

WordNet:

    $ ./scripts/music_schema/music_schema.py | parallel -j 8

Validation and test results will be stored in directories logs/fb15k_schema/ and logs/music_schema/.

# Comparing the Learning Algorithms:

Freebase (FB15k):

    $ ./scripts/fb15k_optimization/fb15k_optimal.py | parallel -j 8

WordNet:

    $ ./scripts/wn_optimization/wn_optimal.py | parallel -j 8
