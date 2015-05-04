#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import logging

import gzip

def main(argv):
    entities_path = 'music_entities.txt'

    #type_path = 'triples/instance_types_en.nt.gz'
    type_path = 'triples/types.nt.gz'

    with open(entities_path) as f:
        entity_iris = set([entity.strip() for entity in f.readlines()])

    entity_iris = set(entity_iris)

    count = 0
    with gzip.open(type_path) as f:
        for line in f:

            count += 1
            if (count % 100000 == 0):
                print('%d' % (count), end='\r', file=sys.stderr)

            triple = line.split()
            if len(triple) > 3:
                subject, predicate, object = triple[0], triple[1], triple[2]
                if subject in entity_iris:
                    print(line.rstrip())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
