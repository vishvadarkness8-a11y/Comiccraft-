import os
import base64

from google import genai


def generate_image(prompt: str):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing"
        )

    client = genai.Client(
        api_key=api_key
    )

    print("Requesting image from Gemini Pro Image...")

    interaction = client.interactions.create(
        model="gemini-3-pro-image",
        input=prompt,
        response_format={
            "type": "image",
            "mime_type": "image/png",
            "aspect_ratio": "1:1",
            "image_size": "1K"
        }
    )

    if not interaction.output_image:
        raise RuntimeError(
            "Gemini did not return an image"
        )

    image_data = interaction.output_image.data

    print("Gemini image received.")

    return base64.b64decode(image_data)
