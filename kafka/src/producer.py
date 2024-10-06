import asyncio
import gzip
import json
from aiokafka import AIOKafkaProducer
from producer.entity import send_entity_data
from producer.interaction import send_interaction_data


async def create_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        max_request_size=2000000,
        value_serializer=lambda data: gzip.compress(json.dumps(data).encode('utf-8'))
        # value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    return producer


async def produce_messages():
    producer = await create_producer()

    try:
        while True:
            await send_entity_data(producer)
            await send_interaction_data(producer)
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(produce_messages())
