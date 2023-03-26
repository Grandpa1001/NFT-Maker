import os
import random
import json
from typing import List
from PIL import Image
from layer import Layer



class AvatarGenerator:
    def __init__(self, images_path: str):
        self.layers: List[Layer] = self.load_image_layers(images_path)
        self.background_color = (120, 150, 180)
        self.rare_background_color = (255, 225, 150)
        self.rare_background_chance = 0.05
        self.output_path: str = "./output"
        os.makedirs(self.output_path, exist_ok=True)

    def load_image_layers(self, images_path: str):
        sub_paths = sorted(os.listdir(images_path))
        layers: List[Layer] = []
        for sub_path in sub_paths:
            layer_path = os.path.join(images_path, sub_path)
            layer = Layer(layer_path)
            layers.append(layer)

## <%> If you want to change the % of participation in the generation of a particular layer, enter the number of the specific layer and % below. e.g. layers[2].rarity = 0.80 layer 3 only occurs at 80% frequency.
        layers[2].rarity = 0.80
        layers[3].rarity = 0.35
        layers[4].rarity = 0.15
## </%>
        return layers

    def generate_image_sequence(self):
        image_path_sequence = []
        layer_names = []
        layer_traits = []
        for layer in self.layers:
            if layer.should_generate():
                image_path = layer.get_random_image_path()
                image_path_sequence.append(image_path)
                layer_traits.append(os.path.basename(os.path.dirname(str(image_path)))[2:])
                layer_names.append(os.path.splitext(os.path.basename(image_path))[0])

        return image_path_sequence, layer_names, layer_traits

    def render_avatar_image(self, image_path_sequence: List[str]):

        if random.random() < self.rare_background_chance:
            bg_color = self.rare_background_color
        else:
            bg_color = self.background_color

## Parameterization of the generated image. Enter what type of graphics color generated and the size of the.
        image = Image.new("RGBA", (3500, 3500), bg_color)
        
        for image_path in image_path_sequence:
            layer_image = Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image

    def save_image(self, image: Image.Image, i: int = 0, image_path_sequence: List[str] = [], layer_names: List[str] = [], layer_traits: List[str] = []):
        image_index = str(i).zfill(4)
        image_file_name = f"avatar_{image_index}.png"
        image_save_path = os.path.join(self.output_path, image_file_name)
        image.save(image_save_path)
        txt_file_name = f"avatar_{image_index}.json"
        txt_file_path = os.path.join(self.output_path, txt_file_name)
        data = {
            "image": image_save_path,
            "name": f"Collection #{i+1}",
            "description": "New collection.",
            "attributes": [
            ]
        } 

        for j in range(len(layer_names)):
            data["attributes"].append({"trait_type": os.path.basename(layer_traits[j]), "value": layer_names[j]})

        with open(txt_file_path, "w") as f:
            f.write(json.dumps(data))


    def generate_avatar(self, n: int = 1):
        print("AvatarGenerator: Generating Avatar!")
        for i in range(n):
            image_path_sequence, layer_names, layer_traits  = self.generate_image_sequence()
            image = self.render_avatar_image(image_path_sequence)
            self.save_image(image, i, image_path_sequence, layer_names, layer_traits)


