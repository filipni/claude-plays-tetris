SYSTEM_PROMPT = """
You are playing Tetris. You can see the game screen and control the game by pressing buttons.
Your goal is to create horisontal lines and score as many points as possible.
Make decisions based on what you see on the screen.
Before each action, explain your reasoning briefly, then press your chosen buttons."""

SUMMARY_PROMPT = """
I need you to create a summary of our conversation history up to this point.
This summary will replace the full conversation history to manage the context window.
The summary should briefly state your main strategy and current goal with the falling block."""

BUTTONS_PROPERTY_DESCRIPTION = """
List of buttons to press in sequence.

Valid buttons:
'left': Moves block to the left
'right': Moves block to the right
'down': Makes the block fall down faster (never press this button more than once in the same sequence)
'a': Rotates block 90 degrees clockwise
'b': Rotates block 90 degrees counter-clockwise"""

AVAILABLE_TOOLS = [
    {
        "name": "press_buttons",
        "description": "Press a sequence of buttons on the Game Boy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "buttons": {
                    "type": "array",
                    "maxItems": 3,
                    "items": {
                        "type": "string",
                        "enum": ["a", "b", "down", "left", "right"],
                    },
                    "description": BUTTONS_PROPERTY_DESCRIPTION
                }
            },
            "required": ["buttons"],
            "additionalProperties": False
        }
    }
]
