from core.channels import Channels


async def send_interaction_data(producer, data=None):
    if not data:
        data = {"action": "center_on_map", "target": {"latitude": 45.0, "longitude": 9.0}}
    await producer.send_and_wait(Channels.INTERACTION.value, data)
