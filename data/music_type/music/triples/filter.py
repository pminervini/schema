#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

import sys
import gzip

import logging

def main(argv):
    f = open(argv[0], 'rb')
    entities = set([entity.strip() for entity in f.readlines()])

    with gzip.open('music.nt.gz') as f:
        for line in f:
            triple = line.split()
            if len(triple) > 3:
                subject, predicate, object = triple[0], triple[1], triple[2]
                if subject in entities and object in entities:
                    sys.stdout.write(line)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
