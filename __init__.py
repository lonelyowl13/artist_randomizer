import json
import os
import random
import time

class RandomArtists:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": ""}),
                "num_artists": ("INT", {"default": 2, "min": 1, "max": 10}),
                "min_post_count": ("INT", {"default": 0, "min": 0}),
                "weight_noise": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0}),
                "seed": ("INT", {"default": 0, "min": -9999999999999, "max": 9999999999999})
            },
            "optional": {}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)

    FUNCTION = "compose_prompt"
    CATEGORY = "Prompt/Random"

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "artists.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.artists = json.load(f)

    def compose_prompt(self, prompt, num_artists, min_post_count, weight_noise, seed):
        eligible = [a["name"] for a in self.artists if a["post_count"] >= min_post_count]

        random.seed(seed)

        if not eligible:
            return (prompt + "  # [No eligible artists found]",)

        selected = random.sample(eligible, min(num_artists, len(eligible)))

        final_tags = []
        for artist in selected:

            artist_escaped = artist.replace(")", "\\)").replace("(", "\\(")
            if weight_noise > 0.0 and random.random() < 0.5:
                weight = round(random.uniform(1.0 - weight_noise, 1.0 + weight_noise), 2)
                final_tags.append(f"({artist_escaped}:{weight})")
            else:
                final_tags.append(artist_escaped)

        final_prompt = prompt.strip()
        if final_prompt and not final_prompt.endswith(","):
            final_prompt += ","

        composed = f"{final_prompt} \n" + ", ".join(final_tags)
        return (composed.strip(),)


class TextInput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Prompt...", "multiline": True})
                # Or use "TEXT" instead of "STRING" if you want a multi-line input
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_output",)

    FUNCTION = "output_text"
    CATEGORY = "Prompt/Basic"

    def output_text(self, text):
        return (text,)

# Required exports
NODE_CLASS_MAPPINGS = {
    "AddRandomArtists": RandomArtists,
    "TextInput": TextInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddRandomArtists": "Add Random Artists",
    "TextInput": "Text Input"
}
