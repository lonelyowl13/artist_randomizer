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
                "weight_noise": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.05}),
                "seed": ("INT", {"default": 0, "min": -9999999999999, "max": 9999999999999}),
                "lumina_style": ("BOOLEAN", {"default": False})
            },
            "optional": {
                "artist_list": ("ARTIST_LIST", )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)

    FUNCTION = "compose_prompt"
    CATEGORY = "Prompt/Random"

    def compose_prompt(self, prompt, num_artists, min_post_count, weight_noise, seed, lumina_style, artist_list=None):
        
        if not artist_list:
            json_path = os.path.join(os.path.dirname(__file__), "artists.json")
            with open(json_path, "r", encoding="utf-8") as f:
                artist_list = json.load(f)
        
        eligible = [a["name"] for a in artist_list if a["post_count"] >= min_post_count]

        random.seed(seed)

        if not eligible:
            return (prompt + "  # [No eligible artists found]",)

        selected = random.sample(eligible, min(num_artists, len(eligible)))

        final_tags = []
        for artist in selected:

            artist_escaped = artist.replace(")", "\\)").replace("(", "\\(")
            if lumina_style:
                artist_escaped = "@" + artist_escaped

            if weight_noise > 0.0 and random.random() < 0.5:
                weight = round(random.uniform(1.0 - weight_noise, 1.0 + weight_noise), 2)
                final_tags.append(f"({artist_escaped}:{weight})")
            else:
                final_tags.append(artist_escaped)

        final_prompt = prompt.strip()

        if "__random_artists__" in final_prompt:
            final_prompt = final_prompt.replace("__random_artists__", ", ".join(final_tags))

        else:
            # just add it to the end of a prompt then
            final_prompt += ", ".join(final_tags)

        composed = final_prompt
        return (composed.strip(),)


def validate_artist_list(artists):
    if not isinstance(artists, list):
        raise ValueError(f"Expected a list, got {type(artists).__name__}")
    
    if len(artists) == 0:
        raise ValueError("Artist list cannot be empty")
    
    for i, entry in enumerate(artists):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry at index {i} is not a dictionary")
        
        if "name" not in entry:
            raise ValueError(f"Entry at index {i} is missing required field 'name'")
        
        if not isinstance(entry["name"], str):
            raise ValueError(f"Entry at index {i}: 'name' must be a string, got {type(entry['name']).__name__}")
        
        if "post_count" not in entry:
            raise ValueError(f"Entry at index {i} is missing required field 'post_count'")
        
        if not isinstance(entry["post_count"], (int)):
            raise ValueError(f"Entry at index {i}: 'post_count' must be aN INTEGER, got {type(entry['post_count']).__name__}")
        
        if entry["post_count"] <= 0:
            raise ValueError(f"Entry at index {i}: 'post_count' cannot be negative")


class LoadArtists:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "File path, e.g. /home/username/artists.json"})
            }
        }


    RETURN_TYPES = ("ARTIST_LIST",)
    RETURN_NAMES = ("artist_list",)

    FUNCTION = "load_json"
    CATEGORY = "Loaders"

    def load_json(self, file_path: str):
        import json
        import os
        
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError("There is no file named '%s'" % file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            validate_artist_list(data)
        return (data,)


class TextInput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Prompt...", "multiline": True})
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
    "TextInput": TextInput,
    "LoadArtists": LoadArtists,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddRandomArtists": "Add Random Artists",
    "TextInput": "Text Input",
    "LoadArtists": "Load Artists",
}
