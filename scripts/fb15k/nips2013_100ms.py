#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

op_set = ['TransE']
sim_set = ['L1', 'L2']
epochs_set, nbatches_set, ndim_set = [1000], [100], [20, 50]
margin_set = [1.0, 2.0, 10.0]
lr_set = [0.001, 0.01, 0.1]

cmd_adagrad = './learn_parameters.py --op=%s --sim=%s --strategy=%s --totepochs=%d --test_all=100 --lr=%f --ndim=%d --nhid=%d --margin=%f --name=fb15k_nips13_%d --train=%s --valid=%s --test=%s --nbatches=%d > logs/fb15k.nips13.%d.log 2>&1'

c, method = 0, 'SGD'

for op in op_set:
    for sim in sim_set:
        for epochs in epochs_set:
            for nbatches in nbatches_set:
                for ndim in ndim_set:
                    for lr in lr_set:
                        for margin in margin_set:
                            print(cmd_adagrad % (op, sim, method, epochs, lr, ndim, ndim, margin, c, train_path, valid_path, test_path, nbatches, c))
                            c += 1
