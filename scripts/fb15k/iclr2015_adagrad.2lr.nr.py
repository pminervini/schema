#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

train_path = 'data/fb15k/FB15k-train.pkl'
valid_path = 'data/fb15k/FB15k-valid.pkl'
test_path = 'data/fb15k/FB15k-test.pkl'

op_set = ['TransE','ScalE']
sim_set = ['L1','L2']
epochs_set, nbatches_set, ndim_set = [1000], [1000], [50]
lremb_set = [0.1]
lrparam_set = [10.0,1.0,0.1,0.01,0.01]
epsilon_set = [0.000001]

cmd = './learn_parameters.py --op=%s --sim=%s --strategy=%s --totepochs=%d --test_all=500 --lremb=%f --lrparam=%f --ndim=%d --nhid=%d --name=fb15k_adagrad.2lr.nr_%d  --train=%s --valid=%s --test=%s --nbatches=%d --no_rescaling > logs/fb15k.adagrad.2lr.nr_%d.log 2>&1'

c, method = 0, 'ADAGRAD'

for op in op_set:
    for sim in sim_set:
        for epochs in epochs_set:
            for nbatches in nbatches_set:
                for ndim in ndim_set:
                    for lremb in lremb_set:
                        for lrparam in lrparam_set:
                            print(cmd % (op, sim, method, epochs, lremb, lrparam, ndim, ndim, c, train_path, valid_path, test_path, nbatches, c))
                            c += 1
