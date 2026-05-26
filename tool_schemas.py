# Define the tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_car_price",
            "description": "looks inside the loaded list of cars, and return the price in egp that is located with the model provided, if not found it returns 'not available'",
            "parameters": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "the brand model of the car",
                    }
                },
                "required": ["model"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_available_colors",
            "description": "looks for the loaded inventory list, it gets the available colors  for a given model, if not found it returns not available",
            "parameters": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "the brand model of the car",
                    }
                },
                "required": ["model"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_cars",
            "description": "looks for the loaded inventory list, it returns all the car models found",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        },
    },
    # ---------- TEST DRIVES
    {
        "type": "function",
        "function": {
            "name": "check_test_drive_request",
            "description": "if the customer request a test drive, we need to check if he already requested it before or not, return true or false, if he already has, we can ask him to edit it",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "description": "the phone number of the customer requesting test drive",
                    },
                    "car_model": {
                        "type": "string",
                        "description": "the brand model of the car",
                    }
                },
                "required": ["phone", "car_model"],
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_test_drive_request",
            "description": "if the customer request a test drive, we will save it",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "description": "the phone number of the customer requesting test drive",
                    },
                    "car_model": {
                        "type": "string",
                        "description": "the brand model of the car",
                    },
                    "name": {
                        "type": "string",
                        "description": "the name of the customer requesting test drive",
                    }
                },
                "required": ["name", "phone", "car_model"],
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_test_drive_request",
            "description": "editing the test drive requested by a user, by adding a new model instead of the old car model",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "description": "the phone number of the customer requesting test drive",
                    },
                    "car_model": {
                        "type": "string",
                        "description": "the old brand model of the car",
                    },
                    "new_car_model": {
                        "type": "string",
                        "description": "the new car model that will be updated for the test drive",
                    }
                },
                "required": ["phone", "car_model", "new_car_model"],
            }
        },
    },

    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": "taking the query, it searches in the vector database created for POLICY for relevant chunks that have the information to the query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "the string that it will search the vector database for relevant vectors",
                    },

                },
                "required": ["query"]
            }
        },
    },

]
