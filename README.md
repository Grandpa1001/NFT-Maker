# Create your own NFT collection: Python

Script to create image + json collection from folder traits.

![avatar_sample](./avatar_sample.png)

### Requirements

* Python 3.6 or higher
* [PIL](https://pillow.readthedocs.io/en/stable/) (Install by running `pip install pillow`)

## Before start

Prepare a folder where the applied layers will be located. The program requires them to have specific prefixes to be able to sort them.
Example: 0_trait1, 1_trait2
Remember that your folders should contain a prefix such as '0_'

The folder name is also important, as it will be entered into the trait attribute. From the example '0_trait1' to json, the attribute will be written in the form : {"trait_type": "trait1", "value": "xyz"},



### Usage

```bash
python generate_avatar.py
```



### output
The result of the script is a created collection folder containing an image + json with the same name.
