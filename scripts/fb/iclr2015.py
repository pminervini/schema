#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

train_path = 'data/fb/FB-train.pkl'
valid_path = 'data/fb/FB-valid.pkl'
test_path = 'data/fb/FB-test.pkl'

op_set = ['TransE', 'ScalE']

epochs_set, nbatches_set, ndim_set = [100], [10], [100]

l2_regularizer_set = [0.0001]

lr_set = [00.100000]
epsilon_set = [0.000001]

cmd_adagrad = './learn_parameters.py --op=%s --strategy=%s --totepochs=%d --test_all=1 --lr=%f --ndim=%d --l2_param=%f --name=fb_%d  --train=%s --valid=%s --test=%s --nbatches=%d > logs/fb.%d.log 2>&1'

c, method = 0, 'ADAGRAD'

for op in op_set:
    for epochs in epochs_set:
        for nbatches in nbatches_set:
            for ndim in ndim_set:
                for lr in lr_set:
                    for l2_regularizer in l2_regularizer_set:
                        print(cmd_adagrad % (op, method, epochs, lr, ndim, l2_regularizer, c, train_path, valid_path, test_path, nbatches, c))
                        c += 1
