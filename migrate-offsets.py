#!/usr/bin/env python

import os

from confluent_kafka import ConsumerGroupTopicPartitions
from confluent_kafka.admin import AdminClient

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(dir_path, 'configuration.ini')
    connection_configs = {}
    with open(conf_path, 'r') as f:
        for line in f:
            (key, val) = line.split('=')
            connection_configs[key] = val

    kafka_admin = AdminClient(connection_configs)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(dir_path, 'consumer-group-migration-map')
    consumer_group_map = {}
    with open(conf_path, 'r') as f:
        for line in f:
            (existing_group, new_group) = line.split(':')
            consumer_group_map[existing_group] = new_group

    for existing_group, new_group in consumer_group_map.items():
        offsets = kafka_admin.list_consumer_group_offsets([ConsumerGroupTopicPartitions(group_id=existing_group)])

        consumer_offsets = offsets.get(existing_group).result()
        print(consumer_offsets.topic_partitions)

        setattr(consumer_offsets, 'group_id', new_group)

        consumer_offsets_new = kafka_admin.alter_consumer_group_offsets([consumer_offsets])

        consumer_offsets_altered = consumer_offsets_new.get(new_group).result()

        print(consumer_offsets_altered.topic_partitions)
