offset migrator ( migrate all CF offsets from one cluster to another )

Important:
- Before running the script, make sure the target consumer group is either in "empty" state or "inactive" state. If it is in the "stable" state, the script will not be able to write to (without error message)
- Double check the consumer group offset before and after the migration

Commands for the validation are:
- check the offset for the consumer group
  kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group <consumerGroupName> --command-config consumer.properties

- check the consumer group's state
  kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group <consumerGroupName> --command-config consumer.properties  --state
