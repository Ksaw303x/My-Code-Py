import random
from core.channels import Channels

NUM_ENTITIES = 500


def _generate_random_entity():
    return {
        # Posizione
        "latitude": random.uniform(-90.0, 90.0),
        "longitude": random.uniform(-180.0, 180.0),
        "altitude": random.randint(0, 10000),
        "yaw": random.uniform(0, 360),  # Yaw angle in degrees
        "pitch": random.uniform(-90, 90),  # Pitch angle
        "roll": random.uniform(-180, 180),  # Roll angle
        "heading": random.uniform(0, 360),  # Heading in degrees
        # Velocità e dinamica di volo
        "airspeed": random.randint(100, 900),  # Airspeed in knots
        "vertical_speed": random.uniform(-5000, 5000),  # Vertical speed in ft/min
        "mach": round(random.uniform(0.5, 2.0), 2),  # Mach speed
        # Strumentazione
        "altimeter": random.randint(0, 50000),  # Altimeter reading in feet
        "fuel_level": random.uniform(0, 100),  # Fuel level in percentage
        "oil_temperature": random.uniform(50, 250),  # Oil temperature in degrees
        "engine_thrust": random.uniform(0, 100),  # Engine thrust in percentage
        "gear_down": random.choice([True, False]),  #

        # Gear status
        "flaps_position": random.uniform(0, 40),  # Flaps position in degrees
        "spoilers_position": random.uniform(0, 100),  # Spoilers position in percentage
        # Sensori
        "gps_accuracy": random.uniform(0.1, 5.0),  # GPS accuracy in meters
        "radar": random.choice([True, False]),  # Radar status
        "barometer": random.uniform(900, 1050),  # Barometric pressure in hPa
        "temperature": random.uniform(-50, 50),  # Temperature in Celsius
        "humidity": random.uniform(0, 100),  # Humidity in percentage
        # Comunicazioni
        "callsign": f"CS{random.randint(1000, 9999)}",  # Callsign
        "radio_freq": random.uniform(108.0, 136.0),  # Radio frequency in MHz
        "transponder_code": f"{random.randint(1000, 7777)}",  # Transponder squawk code
        "sidc": f"S{random.randint(1000, 9999)}",  # SIDC code (System Identification Code)
        "iff": random.choice([True, False]),  # IFF status (Identification Friend or Foe)
        # Modello dell'aereo
        "aircraft_model": random.choice(["Boeing737", "AirbusA320", "Cessna172", "F16", "Boeing747"]),
        "aircraft_type": random.choice(["Passenger", "Cargo", "Military", "Private"]),
        # Sistema
        "autopilot_engaged": random.choice([True, False]),  # Autopilot status
        "autopilot_altitude": random.randint(0, 40000),  # Autopilot target altitude
        "autopilot_heading": random.uniform(0, 360),  # Autopilot heading target
        # Stato
        "engine_on": random.choice([True, False]),  # Engine status
        "engine_rpm": random.randint(1000, 5000),  # Engine RPM
        "battery_level": random.uniform(0, 100),  # Battery level in percentage
        # Stato dell'operazione
        "lights_on": random.choice([True, False]),  # Lights status
        "emergency_status": random.choice([True, False]),  # Emergency status
        "navigation_lights_on": random.choice([True, False]),  # Navigation lights status
        "collision_warning": random.choice([True, False])  # Collision warning system
    }


def _generate_entities(num_entities):
    entities = []
    for _ in range(num_entities):
        entities.append(_generate_random_entity())
    return entities


async def send_entity_data(producer, data=None):
    if not data:
        data = {"entities": ENTITIES}
    await producer.send_and_wait(Channels.ENTITY.value, data)


ENTITIES = _generate_entities(NUM_ENTITIES)
