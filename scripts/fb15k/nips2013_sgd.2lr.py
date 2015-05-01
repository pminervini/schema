#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

op_set = ['TransE']
sim_set = ['L1']
epochs_set, nbatches_set, ndim_set = [1000], [1000], [50]
lr_set = [00.000001, 00.000010, 00.000100, 00.001000, 00.010000, 00.100000, 01.000000, 10.000000]
epsilon_set = [0.000001]

cmd = './learn_parameters.py --op=%s --sim=%s --strategy=%s --totepochs=%d --test_all=%d --lremb=%f --lrparam=%f --ndim=%d --nhid=%d --name=fb15k_sgd.2lr_%d  --train=%s --valid=%s --test=%s --nbatches=%d > logs/fb15k.sgd.2lr_%d.log 2>&1'

c, method = 0, 'SGD'

for op in op_set:
    for sim in sim_set:
        for epochs in epochs_set:
            for nbatches in nbatches_set:
                for ndim in ndim_set:
                    for lremb in lr_set:
                        for lrparam in lr_set:
                            print(cmd % (op, sim, method, epochs, epochs, lremb, lrparam, ndim, ndim, c, train_path, valid_path, test_path, nbatches, c))
                            c += 1
