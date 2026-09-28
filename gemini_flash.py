from pydantic import BaseModel
from google import genai


class Panel(BaseModel):
    panel: int
    description: str
    narration: str
    dialogue: str


class ComicStory(BaseModel):
    character_profile: str
    panels: list[Panel]


def generate_story(
    prompt: str,
    character: str,
    setting: str,
    tone: str,
    style: str,
    client: genai.Client
):
    story_prompt = f"""
Create a coherent 5-panel comic from the following inputs.

STORY:
{prompt}

CHARACTER:
{character}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{style}

CHARACTER PROFILE:
Create a short fixed visual profile for the main character.
Include age, hair, face, clothing, colors, body features,
distinctive features, and accessories.
Keep the same appearance in all panels.

STORY:
Create exactly 5 connected panels.

1. Introduce the situation.
2. Develop it.
3. Show the main event or conflict.
4. Move toward the resolution.
5. Conclude the story.

Maintain continuity of the character, location, objects,
actions, events, time, and cause-and-effect.

For every panel provide:
- panel number
- concise visual description
- concise narration
- concise dialogue

The description must explain what should be visible in the
image, including character action, position, environment,
important objects, and expression.

Do not put speech bubbles, captions, written text,
watermarks, or random text in the image description.

Return exactly 5 panels.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=story_prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ComicStory.model_json_schema()
        }
    )

    return ComicStory.model_validate_json(
        interaction.output_text
    )
