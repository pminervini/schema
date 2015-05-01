#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# Classes of methods
base_vers = ['TransE']
simple_method_set = base_vers

sim_set = ['L1', 'L2']

ndim_set = [20, 50]
nhid_set = [20, 50]

epochs = 100
nbatches = 10
lr = 0.1
seed = 123
margin_set = [1, 2, 10]

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

# ADAGRAD
# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
c, method = 0, 'ADAGRAD'

# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
cmd_adagrad = ('./learn_parameters.py --seed=%d --strategy=%s --totepochs=%d --test_all=%d --lr=%f --name=fb15k_qualitative/fb15k_%s_%d '
                ' --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling '
                ' --op=%s --sim=%s --ndim=%d --nhid=%d --margin=%d ' # varying params
                ' > logs/fb15k_qualitative/fb15k.%s.%s.%d.%d.%d.log 2>&1')


for op in simple_method_set:
    for sim in sim_set:
        for margin in margin_set:
            for ndim in ndim_set:
                nhid = ndim
                print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, op, sim, ndim, margin, c))
                c += 1
