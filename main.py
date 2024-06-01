import pyperclip


def initiate_modifiers(modifier_key_1, modifier_key_2):
    modifiers = f"""
    {{
    "description": "Pressing 'f' + multiple keys outputs them as Capitals, 'g' alone on release if it was not used as a modifier",
    "manipulators": [
    {{
        "from": {{
            "key_code": "{modifier_key_1}",
            "modifiers": {{
                "optional": ["caps_lock"]
            }}
        }},
        "parameters": {{
            "basic.to_if_alone_timeout_milliseconds": 500,
            "basic.to_if_held_down_threshold_milliseconds": 100
        }},
        "to": [
            {{
                "set_variable": {{
                    "name": "modifier_1_active",
                    "value": 1
                }}
            }}
        ],
        "to_after_key_up": [
            {{
                "set_variable": {{
                    "name": "modifier_1_active",
                    "value": 0
                }}
            }}
        ],
        "to_if_alone": [
            {{
                "key_code": "{modifier_key_1}",
                "lazy": false
            }}
        ],
        "type": "basic"
    }},
    {{
        "from": {{
            "key_code": "{modifier_key_2}",
            "modifiers": {{
                "optional": ["caps_lock"]
            }}
        }},
        "parameters": {{
            "basic.to_if_alone_timeout_milliseconds": 500,
            "basic.to_if_held_down_threshold_milliseconds": 100
        }},
        "to": [
            {{
                "set_variable": {{
                    "name": "modifier_2_active",
                    "value": 1
                }}
            }}
        ],
        "to_after_key_up": [
            {{
                "set_variable": {{
                    "name": "modifier_2_active",
                    "value": 0
                }}
            }}
        ],
        "to_if_alone": [
            {{
                "key_code": "{modifier_key_2}",
                "lazy": false
            }}
        ],
        "type": "basic"
    }}
,
    """
    return(modifiers)


def add_single_to_be_modified_key(key):
    json = f"""
    {{
            "conditions": [
                {{
                    "name": "modifier_1_active",
                    "type": "variable_if",
                    "value": 1
                }},
                {{
                    "name": "modifier_2_active",
                    "type": "variable_if",
                    "value": 1
                }}
            ],
            "from": {{
                "key_code": "{key}",
                "modifiers": {{
                    "optional": ["any"]
                }}
            }},
            "to": [
                {{
                    "key_code": "{key}",
                    "modifiers": ["left_shift"]
                }}
            ],
            "type": "basic"
        }},"""
    return(json)

def remove_komma_add_end(input):
    if input[-1] == ",":
        input = input[:-1]
    output = input + """
    ]
    }"""
    return output

def add_all_to_be_modified_keys(modifiers_json, to_be_modified_keys):
    for i, key in enumerate(to_be_modified_keys):
        modifiers_json = modifiers_json + add_single_to_be_modified_key(key)
    return(modifiers_json)

def add_one_key_pressed(modifier_key_1, modifier_key_2, key_pressed):
    json = f"""
    {{
            "conditions": [
                {{
                    "name": "modifier_1_active",
                    "type": "variable_if",
                    "value": 1
                }}
            ],
            "from": {{
                "key_code": "{key_pressed}",
                "modifiers": {{
                    "optional": ["any"]
                }}
            }},
            "to": [
                {{
                    "key_code": "{modifier_key_1}"
                }},
                {{
                    "key_code": "{key_pressed}"
                }}
            ],
            "type": "basic"
        }},
        {{
            "conditions": [
                {{
                    "name": "modifier_2_active",
                    "type": "variable_if",
                    "value": 1
                }}
            ],
            "from": {{
                "key_code": "{key_pressed}",
                "modifiers": {{
                    "optional": ["any"]
                }}
            }},
            "to": [
                {{
                    "key_code": "{modifier_key_2}"
                }},
                {{
                    "key_code": "{key_pressed}"
                }}
            ],
            "type": "basic"
        }},"""
    return(json)

def add_single_press_security(current_json, modifier_key_1, modifier_key_2, to_be_modified_keys):
    for i, key_pressed in enumerate(to_be_modified_keys):
        current_json = current_json + add_one_key_pressed(modifier_key_1, modifier_key_2, key_pressed)
    return(current_json)

#We create a list of all keys we wish to modify, and the modifying keys
capitals = list("qwertasdzxcvbyuiophjklnm")
numbers = list("1234567890")
controls_and_symbols = [
    "return_or_enter",
    "escape",
    "delete_or_backspace",
    "delete_forward",
    "tab",
    # "spacebar",
    "hyphen",
    "equal_sign",
    "open_bracket",
    "close_bracket",
    "backslash",
    "non_us_pound",
    "semicolon",
    "quote",
    "grave_accent_and_tilde",
    "comma",
    "period",
    "slash",
    "non_us_backslash",
]
to_be_modified_keys = capitals + numbers + controls_and_symbols
modifier_key_1, modifier_key_2 = "d", "f"


#Then we initiate the modifiers
modifiers_json = initiate_modifiers(modifier_key_1, modifier_key_2)




#Next we add the modifiers to the keys on which we want the modifiers to act
modifiers_and_keys_to_be_modified_json = add_all_to_be_modified_keys(modifiers_json, to_be_modified_keys)

modifiers_and_keys_to_be_modified_and_single_press_security_json = add_single_press_security(modifiers_and_keys_to_be_modified_json, modifier_key_1, modifier_key_2, to_be_modified_keys)


final_json = remove_komma_add_end(modifiers_and_keys_to_be_modified_and_single_press_security_json)
pyperclip.copy(final_json)
print(final_json)
print("final json was copie to the clipboard")