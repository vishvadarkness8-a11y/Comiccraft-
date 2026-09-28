import os

from fastapi import APIRouter, Form

from gemini_flash import generate_story
from image_generator import generate_image
from layout_builder import build_layout
from exporters import save_pdf


router = APIRouter()


@router.post("/generate")
def create_comic(
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    from google import genai

    story_api_key = os.getenv("GEMINI_API_KEY")

    if not story_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(
        api_key=story_api_key
    )

    # One Gemini request
    story = generate_story(
        prompt=prompt,
        character=character,
        setting=setting,
        tone=tone,
        style=style,
        client=client
    )

    image_paths = []

    for panel in story.panels:

        if style.strip().lower() in [
            "realistic",
            "realistic style",
            "photorealistic"
        ]:
            style_instruction = """
Photorealistic cinematic photography,
natural realistic lighting,
realistic textures and materials,
natural human proportions,
detailed real-world environment,
highly realistic visual appearance.
"""
        else:
            style_instruction = style

        image_prompt = f"""
Create a single comic panel image.

VISUAL STYLE
============
{style_instruction}

CHARACTER CONSISTENCY
=====================

Fixed character profile:

{story.character_profile}

Keep this character visually consistent.

Do not randomly change:
- face
- hair
- hairstyle
- clothing
- clothing colors
- body proportions
- age
- accessories
- distinctive features

SETTING
=======

{setting}

CURRENT SCENE
=============

{panel.description}

STORY CONTEXT
=============

This is panel {panel.panel} of a
5-panel continuous comic story.

The scene must logically fit the story.

IMAGE REQUIREMENTS
==================

Create only the visual scene.

Do not add:
- speech bubbles
- captions
- narration text
- written dialogue
- watermarks
- random text

The image should visually represent
the current scene.
"""

        print(f"Generating image for panel {panel.panel}...")

        image = generate_image(image_prompt)

        filename = f"panel_{panel.panel}.png"

        filepath = os.path.join(
            "static",
            "generated",
            filename
        )

        with open(filepath, "wb") as file:
            file.write(image)

        image_paths.append(filepath)

    panels = build_layout(
        story,
        image_paths
    )

    pdf_path = os.path.join(
        "static",
        "generated",
        "comic.pdf"
    )

    save_pdf(
        panels,
        pdf_path
    )

    for panel in panels:
        panel["image"] = (
            "/static/generated/"
            f"panel_{panel['panel']}.png"
        )

    return {
        "comic": {
            "panels": panels
        },
        "panels": panels,
        "pdf": "/static/generated/comic.pdf"
    }
