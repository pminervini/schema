#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# Classes of methods
base_vers = ['TransE', 'ScalE']
scaltrans_vers = ['ScalTransE']
xi_vers = ['XiTransE', 'XiScalE']
semixi_vers = ['XiScalTransSE', 'XiTransScalSE']
xiscaltrans_vers = ['XiScalTransE']

simple_method_set = base_vers + scaltrans_vers + xi_vers + semixi_vers + xiscaltrans_vers

sim_set = ['L1', 'L2', 'dot']

margin_set = [1, 2, 10]
ndim_set = [20, 50, 100, 200]
nhid_set = [20, 50, 100, 200]

l1reg_set = ['0.0', '1e-4', '1e-2', '1e0', '1e2', '1e4', '1e6']

epochs = 100
nbatches = 10
lr = 0.1
seed = 123

train_path = 'data/wn/WN-train.pkl'
valid_path = 'data/wn/WN-valid.pkl'
test_path = 'data/wn/WN-test.pkl'

# ADAGRAD
# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
c, method = 0, 'ADAGRAD'

# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
cmd_adagrad = ('./learn_parameters.py --seed=%d --strategy=%s --totepochs=%d --test_all=%d --lr=%f --name=wn_regularization/wn_%s_%d '
                ' --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling --filtered '
                ' --op=%s --sim=%s --ndim=%d --nhid=%d --margin=%d --l1_embed=%s --l1_param=%s' # varying params
                ' > logs/wn_models_regularization/wn_regularization.%s_%s_%d_%d_%d_%s_%s_%d.log 2>&1')


for op in simple_method_set:
    for sim in sim_set:
        for ndim in ndim_set:
            nhid = ndim
            for margin in margin_set:
                for l1_embed in l1reg_set:
                    for l1_param in l1reg_set:
                        print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, l1_embed, l1_param, op, sim, ndim, nhid, margin, l1_embed, l1_param, c))
                        c += 1
