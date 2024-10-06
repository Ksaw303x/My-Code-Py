import asyncio
import gzip
import time
import json

from aiokafka import AIOKafkaConsumer
from core.channels import Channels


async def create_consumer():
    consumer = AIOKafkaConsumer(
        Channels.ENTITY.value,
        Channels.INTERACTION.value,
        bootstrap_servers='localhost:9092',
        group_id='entity_interaction_group',
        value_deserializer=lambda data: json.loads(gzip.decompress(data).decode('utf-8'))
        # value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    return consumer


async def consume_messages(consumer):
    last_message_time = None
    try:
        async for msg in consumer:
            current_time = time.time()

            if last_message_time is not None:
                time_diff = current_time - last_message_time
                print(f"Tempo {time_diff * 1000}")
            else:
                print("Primo messaggio ricevuto.")

            last_message_time = current_time

            if msg.topic == Channels.ENTITY.value:
                print(f"Received entity data len: {len(msg.value)}")
            elif msg.topic == Channels.INTERACTION.value:
                print(f"Received interaction data len: {len(msg.value)}")
    finally:
        await consumer.stop()


async def main():
    consumer = await create_consumer()
    await consume_messages(consumer)

# Avvia il consumer
if __name__ == '__main__':
    asyncio.run(main())
