import os
import random
import json
from typing import List
from PIL import Image
from layer import Layer



class AvatarGenerator:



    def __init__(self, images_path: str):
        self.layers: List[Layer] = self.load_image_layers(images_path)
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

        layers[3].rarity = 0.05
        layers[4].rarity = 0.995
        layers[5].rarity = 0.10
        layers[6].rarity = 0.07
## </%>
        return layers


    def generate_image_sequence(self):
        with open("input/banlista.txt", "r") as file:
            banList = file.read().splitlines()
        image_path_sequence = []
        layer_names = []
        layer_check = []
        layer_traits = []
        for layer in self.layers:
            if layer.should_generate():
                image_path = layer.get_random_image_path()
                image_path_sequence.append(image_path)
                layer_traits.append(os.path.basename(os.path.dirname(str(image_path)))[2:])
                layer_names.append(os.path.splitext(os.path.basename(image_path))[0].split("_")[0])
                layer_check.append("#"+os.path.splitext(os.path.basename(image_path))[0].split("_")[0]+"#")
        textCheck= "-".join(layer_check)

        for banned_name in banList:
            #print("???????Sprawdzamy: "+banned_name+"=>>>"+textCheck)
            banned_name = banned_name.strip()  # usuwa białe znaki z początku i końca linii
            if "-" in banned_name:
                banListText1, banListText2 = banned_name.split("-") # podział na dwie części
                banListText1 = "#"+banListText1+"#"
                banListText2 = "#"+banListText2+"#"
                #print(banListText1)
                #print(banListText2)
                #print(textCheck)
                if banListText1 in textCheck and banListText2 in textCheck:
                    print(f"----------BANLIST("+banListText2+" || "+banListText1+") in ("+textCheck+") and skip ")
                    return None, None, None
         #   print("+++++ Wygenerowano("+textCheck+")")
        return image_path_sequence, layer_names, layer_traits

    
    def render_avatar_image(self, image_path_sequence: List[str]):

## Parameterization of the generated image. Enter what type of graphics color generated and the size of the.
        image = Image.new("RGBA", (1088, 1088))
        
        for image_path in image_path_sequence:
            layer_image = Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image

    def save_image(self, image: Image.Image, i: int = 0, image_path_sequence: List[str] = [], layer_names: List[str] = [], layer_traits: List[str] = []):

##################### DO EDYCJI PARAMETR LOSOWOSCI    #####################
        numberToRoll = 0;   # 0- turn of random number || 1+ - change value to can roll number range 0-(write number) 
##################### DO EDYCJI PARAMETR LOSOWOSCI    #####################

        if numberToRoll != 0:
            rollNumber = random.randint(0, numberToRoll)
        else:
            rollNumber = i;
            

        image_index = str(rollNumber)
        image_file_name = f"{image_index}.png"
        image_save_path = os.path.join(self.output_path, image_file_name)
        image.save(image_save_path)
        txt_file_name = f"{image_index}.json"
        txt_file_path = os.path.join(self.output_path, txt_file_name)
        data = {
            "image": image_save_path,
            "name": f"Collection #{rollNumber}",
            "description": "New collection.",
            "attributes": [
            ]
        } 

        for j in range(len(layer_names)):
            data["attributes"].append({"trait_type": os.path.basename(layer_traits[j]), "value": layer_names[j]})

        with open(txt_file_path, "w") as f:
            f.write(json.dumps(data))


    def generate_avatar(self, n: int = 1):
        print("AvatarGenerator: Generating Avatar! Liczba do wygenerowania" + str(n))
        with open("output/generated_avatars.txt", "a") as f:
            generated_count = 0
            while generated_count < n:
                image_path_sequence, layer_names, layer_traits = self.generate_image_sequence()
                if image_path_sequence is not None and layer_names is not None and layer_traits is not None:
                    generated_count += 1
                    image = self.render_avatar_image(image_path_sequence)
                    self.save_image(image, generated_count, image_path_sequence, layer_names, layer_traits)
                    f.write(f"{image_path_sequence}\n")
                    print("Wygenerowano "+ str(generated_count) +" do "+str(n))

                else:
                    print(f"Nie udało się wygenerować poprawnego obrazu, próbuje ponownie!")

