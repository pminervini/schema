#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# Classes of methods
base_vers = ['TransE', 'ScalE']
scaltrans_vers = ['ScalTransE']
xi_vers = ['XiTransE', 'XiScalE']
semixi_vers = ['XiScalTransSE', 'XiTransScalSE']
xiscaltrans_vers = ['XiScalTransE']

simple_method_set = base_vers + xi_vers + scaltrans_vers + semixi_vers + xiscaltrans_vers

sim_set = ['L1', 'L2', 'dot']

#margin_set = [1, 2, 10]
margin_set = [1]

ndim_set = [20, 50, 100, 200]
nhid_set = [20, 50, 100, 200]

epochs = 100
nbatches = 10
lr = 0.1
seed = 123

train_path = 'data/music_type/music-train.pkl'
valid_path = 'data/music_type/music-valid.pkl'
test_path = 'data/music_type/music-test.pkl'

# ADAGRAD
# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
c, method = 0, 'ADAGRAD'

# def adagrad(param, rate, epsilon, gradient, updates, param_squared_gradients):
cmd_adagrad = ('./learn_parameters.py --seed=%d --strategy=%s --totepochs=%d --test_all=%d --lr=%f --name=music_dr_sl/music_%s_%d '
                ' --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling --filtered '
                ' --domain_range=data/music_type/music_domains_ranges.pkl --dr_standard_learning '
                ' --op=%s --sim=%s --ndim=%d --nhid=%d --margin=%d' # varying params
                ' > logs/music_schema/music_schema.%s_%s_%d_%d_%d_%d.log 2>&1')


for op in simple_method_set:
    for sim in sim_set:
        for ndim in ndim_set:
            nhid = ndim
            for margin in margin_set:
                print(cmd_adagrad % (seed, method, epochs, epochs, lr, op, c, train_path, valid_path, test_path, nbatches, op, sim, ndim, nhid, margin, op, sim, ndim, nhid, margin, c))
                c += 1
