#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# Classes of methods
base_vers = ['TransE', 'ScalE', 'NTransE', 'NScalE', 'BiTransE', 'BiScalE', 'BiNTransE', 'BiNScalE']
#lc_vers = ['CeTransE', 'CrTransE', 'CerTransE']
scaltrans_vers = ['ScalTransE', 'NScalTransE', 'BiScalTransE', 'BiNScalTransE']
aff_vers = ['AffinE', 'NAffinE']

affc_vers = ['BiAffinE', 'BiNAffinE']

simple_method_set = base_vers + scaltrans_vers
complex_method_set = affc_vers

sim_set = ['L1', 'L2', 'dot']

ndim_set = [20, 50, 100]
nhid_set = [20, 50, 100]

ndim_small_set = [20, 50]
nhid_small_set = [20, 50]

epochs = 100
nbatches = 10
lr = 0.1
seed = 123
margin = 1

train_path = 'data/fb15k-401/FB15k-401-train.pkl'
valid_path = 'data/fb15k-401/FB15k-401-valid.pkl'
test_path = 'data/fb15k-401/FB15k-401-test.pkl'

# ADAGRAD
# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
c, method = 0, 'ADAGRAD'

# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
cmd_adagrad = ('./learn_parameters.py --seed=%d --strategy=%s --totepochs=%d --test_all=%d --lr=%f --name=fb15k-401/no_reg/fb15k-401_%s_%d '
                ' --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling '
                ' --op=%s --sim=%s --ndim=%d --nhid=%d --margin=%d ' # varying params
                ' > logs/fb15k-401_models/no_reg/fb15k-401.%s.%s.%d.%d.%d.log 2>&1')


for op in simple_method_set:
    for sim in sim_set:
        for ndim in ndim_set:
            nhid = ndim
            print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, op, sim, ndim, nhid, c))
            c += 1

for op in aff_vers:
    for sim in sim_set:
        for ndim in ndim_small_set:
            nhid = ndim
            print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, op, sim, ndim, nhid, c))
            c += 1

for op in complex_method_set:
    for sim in sim_set:
        for ndim in ndim_small_set:
            for nhid in nhid_small_set:
                print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, op, sim, ndim, nhid, c))
                c += 1
