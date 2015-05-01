#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# Classes of methods
base_vers = ['TransE', 'ScalE', 'NTransE', 'NScalE', 'BiTransE', 'BiScalE', 'BiNTransE', 'BiNScalE']
#lc_vers = ['CeTransE', 'CrTransE', 'CerTransE']
scaltrans_vers = ['ScalTransE', 'NScalTransE', 'BiScalTransE', 'BiNScalTransE']
afftrans_vers = ['AffTransE', 'NAffTransE', 'BiAffTransE', 'BiNAffTransE']

simple_method_set = base_vers + scaltrans_vers
complex_method_set = afftrans_vers

sim_set = ['L1', 'L2', 'dot']

l1reg_set = [0.0, 1e-6, 1e-4, 1e-2, 1e0]

ndim_set = [20, 50, 100]
nhid_set = [20, 50, 100]

epochs = 100
nbatches = 10
lr = 0.1
seed = 123
margin = 1

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

# ADAGRAD
# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
c, method = 0, 'ADAGRAD'

# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
cmd_adagrad = ('./learn_parameters.py --seed=%d --strategy=%s --totepochs=%d --test_all=%d --lr=%f --name=fb15k/fb15k_%s_%d '
                ' --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling '
                ' --op=%s --sim=%s --ndim=%d --nhid=%d --margin=%d --l1_param=%f ' # varying params
                ' > logs/fb15k_models/fb15k.%s.%d.log 2>&1')


for op in simple_method_set:
    for sim in sim_set:
        for ndim in ndim_set:
            nhid = ndim
            for l1reg in l1reg_set:
                print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, l1reg, op, c))
                c += 1


for op in complex_method_set:
    for sim in sim_set:
        for ndim in ndim_set:
            for nhid in nhid_set:
                for l1reg in l1reg_set:
                    print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, l1reg, op, c))
                    c += 1
