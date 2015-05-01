#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

op_set = ['TransE', 'ScalE']
sim_set = ['L1', 'L2', 'dot']
#epochs_set, nbatches_set, ndim_set = [100], [10], [100]
epochs_set, nbatches_set, ndim_set = [500], [10], [100]
l2_regularizer_set = [0.0001]
lr_set = [00.000001, 00.000010, 00.000100, 00.001000, 00.010000, 00.100000, 01.000000, 10.000000]
epsilon_set = [0.000001]

cmd_adagrad = './learn_parameters.py --op=%s --sim=%s --strategy=%s --totepochs=%d --test_all=%d --lr=%f --ndim=%d --l2_param=%f --name=fb15k_adagrad_%s_%s_%d  --train=%s --valid=%s --test=%s --nbatches=%d --use_db > logs/fb15k.adagrad.%s_%s_%d.log 2>&1'

c, method = 0, 'ADAGRAD'


for op in op_set:
    for sim in sim_set:
        for epochs in epochs_set:
            for nbatches in nbatches_set:
                for ndim in ndim_set:
                    for lr in lr_set:
                        for l2_regularizer in l2_regularizer_set:
                            print(cmd_adagrad % (op, sim, method, epochs, epochs, lr, ndim, l2_regularizer, op, sim, c, train_path, valid_path, test_path, nbatches, op, sim, c))
                            c += 1
