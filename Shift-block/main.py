import pyperclip


def init():
    json = f"""
    {{
    "description": "Pressing Shift + [any key] neglects shift or everything alltogether.",
            "manipulators": [
    """
    return json

def block_shift_modification(letter):
    json = f"""
    {{
    "type": "basic",
    "from": {{
        "key_code": "{letter}",
        "modifiers": {{
            "mandatory": ["left_shift"]
        }}
    }},
    "to": [
        {{
            "key_code": "{letter}"
        }}
    ]
    }},"""
    return json


def block_multiple_shift_modifications(karabinerScript, to_be_modified_keys):
    for i, letter in enumerate(to_be_modified_keys):
        karabinerScript = karabinerScript + block_shift_modification(letter)
    return(karabinerScript)

def end_script(input):
    if input[-1] == ",":
        input = input[:-1]
    output = input + """
    ]
    }"""
    return output

capitals = list("qwertasdzxcvbyuiophjklnm")
numbers = list("1234567890")
controls_and_symbols = [
    "return_or_enter",
    "escape",
    "delete_or_backspace",
    "delete_forward",
    # "tab", We exclude this, as we want to still shift-tab the ordinary way
    "spacebar",
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

arrows = ["up_arrow",
          "down_arrow",
          "left_arrow",
          "right_arrow",
          "page_up",
          "page_down",
          "home",
          "end"]
to_be_modified_keys = capitals + numbers + controls_and_symbols + arrows


karabinerScript = init()

karabinerScript = block_multiple_shift_modifications(karabinerScript, to_be_modified_keys)

karabinerScript = end_script(karabinerScript)

pyperclip.copy(karabinerScript)
