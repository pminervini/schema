#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

import sys
import logging

import gzip
import rdflib

import pickle

def dbo(x):
    return '<http://dbpedia.org/ontology/' + x + '>'

def entity_types(entity_iris):
    type_path = 'triples/types_sub.nt.gz'
    entity_to_types = {}
    with gzip.open(type_path) as f:
        for line in f:
            triple = line.split()
            if len(triple) > 3:
                subject, predicate, object = triple[0], triple[1], triple[2]
                if subject in entity_iris:
                    if subject not in entity_to_types:
                        entity_to_types[subject] = set()
                    entity_to_types[subject].add(object)
    return entity_to_types

def enrich_types(entity_iri_to_types):
    for (entity, types) in entity_iri_to_types.items():
        if dbo('Band') in types or dbo('MusicalArtist') in types or dbo('MusicGroup') in types:
            types.add(dbo('Band'))
            types.add(dbo('MusicalArtist'))
        #if dbo('Company') in types:
        #    types.add(dbo('RecordLabel'))
        #if dbo('Person') in types:
        #    types.add(dbo('MusicalArtist'))
        #    types.add(dbo('Band'))
    return entity_iri_to_types

def get_domain_range(relations):
    relation_to_domains = {
        dbo('album'): set([]),
        dbo('associatedBand'): set([]),
        dbo('associatedMusicalArtist'): set([]),
        dbo('genre'): set([]),
        dbo('musicalArtist'): set([dbo('Single')]),
        dbo('musicalBand'): set([dbo('Single')]),
        dbo('recordLabel'): set([])
    }
    relation_to_ranges = {
        dbo('album'): set([dbo('Album')]),
        dbo('associatedBand'): set([dbo('Band')]),
        dbo('associatedMusicalArtist'): set([dbo('MusicalArtist')]),
        dbo('genre'): set([dbo('Genre')]),
        dbo('musicalArtist'): set([dbo('MusicalArtist')]),
        dbo('musicalBand'): set([dbo('Band')]),
        dbo('recordLabel'): set([dbo('RecordLabel')])
    }
    return (relation_to_domains, relation_to_ranges)

def main(argv):
    entities_path = 'music_entities.txt'
    relations_path = 'music_relations.txt'

    with open(entities_path) as f:
        entity_iris = set([entity.strip() for entity in f.readlines()])

    with open(relations_path) as f:
        relation_iris = set([relation.strip() for relation in f.readlines()])

    (relation_iri_to_domains, relation_iri_to_ranges) = get_domain_range(relation_iris)

    logging.info('Associating each Relation with two Entity Sets ..')

    relation_to_domain_entities = {}
    relation_to_range_entities = {}

    entity_iri_to_types = entity_types(entity_iris)

    for path in ['dataset/music_mte5_train.nt.gz', 'dataset/music_mte5_valid.nt.gz']:
        f = gzip.open(path, 'r')
        for line in f:
            triple = line.split()
            if len(triple) >= 3:
                subject, predicate, object = triple[0], triple[1], triple[2]
                domain_types, range_types = relation_iri_to_domains[predicate], relation_iri_to_ranges[predicate]
                if subject not in entity_iri_to_types:
                    entity_iri_to_types[subject] = set()
                for domain_type in domain_types:
                    entity_iri_to_types[subject].add(domain_type)
                if object not in entity_iri_to_types:
                    entity_iri_to_types[object] = set()
                for range_type in range_types:
                    entity_iri_to_types[object].add(range_type)

    entity_iri_to_types = enrich_types(entity_iri_to_types)

    type_to_entity_iris = {}
    for (entity, types) in entity_iri_to_types.items():
        for type in types:
            if type in type_to_entity_iris:
                type_to_entity_iris[type] += [entity]
            else:
                type_to_entity_iris[type] = [entity]


    for relation_iri in relation_iris:
        relation = relation_iri
        domain_types = relation_iri_to_domains[relation_iri]
        range_types = relation_iri_to_ranges[relation_iri]

        domain = []
        for domain_type in domain_types:
            if domain_type in type_to_entity_iris:
                domain += type_to_entity_iris[domain_type]
        if len(domain_types) < 1:
            domain += entity_iris

        range = []
        for range_type in range_types:
            if range_type in type_to_entity_iris:
                range += type_to_entity_iris[range_type]
        if len(range_types) < 1:
            range += entity_iris

        print('%d %s %d' % (len(set(domain)), relation, len(set(range))))

        relation_to_domain_entities[relation] = set(domain)
        relation_to_range_entities[relation] = set(range)


    #sys.exit(0)


    native_entity2idx = pickle.load(open('data/music_entity2idx.pkl', 'rb'))

    NE, NP = len(entity_iris), len(relation_iris)

    entity2idx, relation2idx = {}, {}
    idx2entity, idx2relation = {}, {}

    for relation in relation_iris:
        native_relation_idx = native_entity2idx[relation]
        relation_idx = native_relation_idx - NE

        relation2idx[relation] = relation_idx
        idx2relation[relation_idx] = relation

        logging.debug('Relation (%d): %s ' % (relation_idx, relation))

    for entity in entity_iris:
        if entity in native_entity2idx:
            native_entity_idx = native_entity2idx[entity]
            entity_idx = native_entity_idx

            entity2idx[entity] = entity_idx
            idx2entity[entity_idx] = entity

            logging.debug('Entity (%d): %s ' % (entity_idx, entity))

    relation2domain, relation2range = {}, {}

    for relation in relation_iris:
        relation_idx = relation2idx[relation]

        domain = relation_to_domain_entities[relation]
        range = relation_to_range_entities[relation]

        domain_idxs = [entity2idx[e] for e in domain]
        range_idxs = [entity2idx[e] for e in range]

        relation2domain[relation_idx] = domain_idxs
        relation2range[relation_idx] = range_idxs


    with gzip.open('triples/music_mte5.nt.gz', 'r') as f:
        for line in f:
            triple = line.split()
            if len(triple) >= 3:
                subject, predicate, object = triple[0], triple[1], triple[2]

                domain = relation_to_domain_entities[predicate]
                range = relation_to_range_entities[predicate]

                if subject not in domain or object not in range:
                    logging.info('Illegal triple: %s' % (triple))
                    if subject not in domain:
                        logging.info('Subject was not in domain (%d)' % (len(domain)))
                    if object not in range:
                        logging.info('Object was not in range (%d)' % (len(range)))

                if subject not in entity_iris or object not in entity_iris:
                    logging.warn('subject %s or object %s not in entities' % (subject, object))

                if predicate not in relation_iris:
                    logging.warn('relation %s not in relations' % (predicate))


    logging.info('Serializing domains and ranges ..')

    to_serialize = {
        'relation2domain': relation2domain,
        'relation2range': relation2range,

        'entity2idx': entity2idx,
        'relation2idx': relation2idx,

        'idx2entity': idx2entity,
        'idx2relation': idx2relation
    }

    f = open('music_domains_ranges.pkl', 'wb')
    pickle.dump(to_serialize, f)
    f.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
