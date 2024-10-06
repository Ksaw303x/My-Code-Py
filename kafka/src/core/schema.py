# JSON schema for entity data
entity_data_schema = {
    "type": "object",
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "altitude": {"type": "number"},
        "callsign": {"type": "string"},
        "model": {"type": "string"},
        "discode": {"type": "string"}
    },
    "required": ["latitude", "longitude", "callsign", "model", "discode"]
}

# JSON schema for interaction data
interaction_data_schema = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "target": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            }
        }
    },
    "required": ["action", "target"]
}