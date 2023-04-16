from avatar_generator import AvatarGenerator


def generate_avatar():
    generator = AvatarGenerator("./input/images")
    generator.generate_avatar(10)


if __name__ == "__main__":
    generate_avatar()
