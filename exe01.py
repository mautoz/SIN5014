from typing import Tuple
from PIL import Image
from numpy import array
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np


def get_image_matrix(img_path: str) -> array:
    image_matrix = Image.open(img_path)
    return array(image_matrix)


def get_image_shape(img_matrix: array):
    return img_matrix.shape


def get_frequencies_arrays(img_path: str) -> Tuple[array, array, array]:
    red = [0] * 256
    green = [0] * 256
    blue = [0] * 256

    img = get_image_matrix(img_path)
    width, height, _ = get_image_shape(img)

    for w in range(width):
        for h in range(height):
            red[img[w][h][0]] += 1
            green[img[w][h][1]] += 1
            blue[img[w][h][2]] += 1

    return red, green, blue


def change_brightness(img_path: str, level: int) -> array:
    img = get_image_matrix(img_path)
    width, height, _ = get_image_shape(img)

    for w in range(width):
        for h in range(height):
            r_new_level = img[w][h][0] + level
            g_new_level = img[w][h][1] + level
            b_new_level = img[w][h][2] + level

            if r_new_level < 0:
                img[w][h][0] = 0
            elif r_new_level > 255:
                img[w][h][0] = 255
            else:
                img[w][h][0] = r_new_level

            if g_new_level < 0:
                img[w][h][1] = 0
            elif g_new_level > 255:
                img[w][h][1] = 255
            else:
                img[w][h][1] = g_new_level

            if b_new_level < 0:
                img[w][h][2] = 0
            elif b_new_level > 255:
                img[w][h][2] = 255
            else:
                img[w][h][2] = b_new_level

    return img


def get_neighborhood_average(img_matrix: array, w: int, h: int, color: int) -> float:
    neighborhood = [
        img_matrix[w - 1][h - 1][color],
        img_matrix[w][h - 1][color],
        img_matrix[w + 1][h - 1][color],
        img_matrix[w + 1][h][color],
        img_matrix[w + 1][h + 1][color],
        img_matrix[w][h + 1][color],
        img_matrix[w - 1][h + 1][color],
        img_matrix[w - 1][h][color],
    ]

    return np.mean(neighborhood)


def calculate_image_average(img_path: str) -> array:
    img = get_image_matrix(img_path)
    img_aux = img
    width, height, _ = get_image_shape(img)

    for w in range(1, width - 1):
        for h in range(1, height - 1):
            img[w][h][0] = get_neighborhood_average(img_aux, w, h, 0)
            img[w][h][1] = get_neighborhood_average(img_aux, w, h, 1)
            img[w][h][2] = get_neighborhood_average(img_aux, w, h, 2)

    return img


def show_histogram(
    frequencies_array, color, name: str, output=None, save=False
) -> None:
    X = [i for i in range(256)]
    Y = frequencies_array

    plt.bar(X, Y, color=color, width=1)

    plt.title(f"Histogram for {color}")
    plt.xlabel(f"Level of {color}")
    plt.ylabel(f"Pixels frequency")

    if save:
        name = name.split(".")
        plt.savefig(f"{output}/{name[0]}_{color}_histogram.png")
    plt.show()
    plt.close()


def save_image(array: str, output: str, name: str):
    img = Image.fromarray(array, "RGB")
    img.save(f"{output}/{name}.png")
    img.show()
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Criando histogramas para imagens RGB")
    parser.add_argument("--img", type=str, help="Caminho da imagem que será analisada")
    parser.add_argument(
        "--output", type=str, help="Pasta em que as imagens serão salvas"
    )
    args = parser.parse_args()

    # r, g, b = get_frequencies_arrays(args.img)

    # # Calculate
    # show_histogram(r, "red", os.path.basename(args.img), output=args.output, save=True)
    # show_histogram(
    #     g, "green", os.path.basename(args.img), output=args.output, save=True
    # )
    # show_histogram(b, "blue", os.path.basename(args.img), output=args.output, save=True)

    # new_image = change_brightness(args.img, 10)
    # save_image(
    #     new_image,
    #     args.output,
    #     f"{str(os.path.basename(args.img)).split('.')[0]}_brightness",
    # )

    new_image_average = calculate_image_average(args.img)
    save_image(
        new_image_average,
        args.output,
        f"{str(os.path.basename(args.img)).split('.')[0]}_average",
    )
