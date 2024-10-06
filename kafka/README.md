# Kafka architecture

Event streamer propagator, published and read in async

## Topics

Topics must be created in advance using the admin client

```python
from confluent_kafka.admin import AdminClient, NewTopic

# Configura Kafka Admin Client
admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

# Definisci il nuovo topic
new_topic = [NewTopic(topic="my_new_topic", num_partitions=3, replication_factor=1)]

# Crea il topic
fs = admin_client.create_topics(new_topic)

for topic, f in fs.items():
    try:
        f.result()
        print(f"Topic {topic} creato con successo")
    except Exception as e:
        print(f"Errore durante la creazione del topic {topic}: {e}")
```
Another way to manage the kafka installation is by the web admin panel

| Topic name | Scope                         | Proxy |
|------------|-------------------------------|-------|
| `internal` | Internal Interactions Channel | no    |
| `entity`   | Entity channel                | yes   |
| `weather`  | Weather channel               | yes   |
