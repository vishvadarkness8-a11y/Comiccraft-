def build_layout(
    story,
    image_paths
):
    panels = []

    for panel, image_path in zip(
        story.panels,
        image_paths
    ):
        panels.append({
            "panel": panel.panel,
            "description": panel.description,
            "narration": panel.narration,
            "dialogue": panel.dialogue,
            "image": image_path,
            "filepath": image_path
        })

    return panels
