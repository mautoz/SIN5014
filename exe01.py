from typing import Tuple
from PIL import Image
from numpy import array
import matplotlib.pyplot as plt
import argparse
import os


def get_image_matrix(img_path: str) -> array:
    """
    Open an image and convert to matrix.

    Parameters
    ----------
        img_path : str
            The path from the image source

    Returns
    -------
        An matrix of the image
    """
    image_matrix = Image.open(img_path)
    return array(image_matrix)


def get_image_shape(img_matrix: array):
    """
    An image matrix as parameter and return width, height and colors os the image
    """
    return img_matrix.shape


def get_frequencies_arrays(img_matrix: array) -> Tuple[array, array, array]:
    """
    Read the matrix and

    Parameters
    ----------
        img_matrix : array
            An array that represents the image.

    Returns
    -------
        A tuple with the frequencies of the colors RGB
    """
    red = [0] * 256
    green = [0] * 256
    blue = [0] * 256

    width, height, _ = get_image_shape(img_matrix)

    for w in range(width):
        for h in range(height):
            red[img_matrix[w][h][0]] += 1
            green[img_matrix[w][h][1]] += 1
            blue[img_matrix[w][h][2]] += 1

    return red, green, blue


def change_brightness(img_matrix: array, level: int) -> array:
    """
    Read an image matrix and apply the level of `brightness` you want to change.

    Parameters
    ----------
        img_matrix : array
            An array that represents the image.
        level: int
            A number that we use to change the brigthness. Use something between -255 and 255.

    Returns
    -------
        A tuple with the frequencies of the colors RGB
    """
    width, height, _ = get_image_shape(img_matrix)

    for w in range(width):
        for h in range(height):
            r_new_level = img_matrix[w][h][0] + level
            g_new_level = img_matrix[w][h][1] + level
            b_new_level = img_matrix[w][h][2] + level

            if r_new_level < 0:
                img_matrix[w][h][0] = 0
            elif r_new_level > 255:
                img_matrix[w][h][0] = 255
            else:
                img_matrix[w][h][0] = r_new_level

            if g_new_level < 0:
                img_matrix[w][h][1] = 0
            elif g_new_level > 255:
                img_matrix[w][h][1] = 255
            else:
                img_matrix[w][h][1] = g_new_level

            if b_new_level < 0:
                img_matrix[w][h][2] = 0
            elif b_new_level > 255:
                img_matrix[w][h][2] = 255
            else:
                img_matrix[w][h][2] = b_new_level

    return img_matrix


def get_neighborhood_average(img_matrix: array, w: int, h: int, color: int) -> float:
    """
    Read an image matrix and apply the level of `brightness` you want to change.

    Parameters
    ----------
        img_matrix: array
            An array that represents the image.
        w: int
            Width of the image
        h: int
            Height of the image
        color: int
            R is 0, G is 1 and B is 2

    Returns
    -------
        An array with the RGB
    """
    return [
        img_matrix[w - 1][h - 1][color],
        img_matrix[w][h - 1][color],
        img_matrix[w + 1][h - 1][color],
        img_matrix[w + 1][h][color],
        img_matrix[w + 1][h + 1][color],
        img_matrix[w][h + 1][color],
        img_matrix[w - 1][h + 1][color],
        img_matrix[w - 1][h][color],
    ]


def calculate_image_average(img_matrix: array) -> array:
    """
    Read an image matrix and

    Parameters
    ----------
        img_matrix: array
            Image matrix.

    Returns
    -------
        An array of image after calculate the average.
    """
    img_aux = img_matrix
    width, height, _ = get_image_shape(img_matrix)

    for w in range(1, width - 1):
        for h in range(1, height - 1):
            img_matrix[w][h][0] = calculate_average(
                get_neighborhood_average(img_aux, w, h, 0)
            )
            img_matrix[w][h][1] = calculate_average(
                get_neighborhood_average(img_aux, w, h, 1)
            )
            img_matrix[w][h][2] = calculate_average(
                get_neighborhood_average(img_aux, w, h, 2)
            )

    return img_matrix


def calculate_image_median(img_matrix: array) -> array:
    """
    Read an array of frequencies, show the histogram and save the image.

    Parameters
    ----------
        img_matrix: array
            Image matrix.

    Returns
    -------
        An array of image after calculate the median.
    """
    img_aux = img_matrix
    width, height, _ = get_image_shape(img_matrix)

    for w in range(1, width - 1):
        for h in range(1, height - 1):
            img_matrix[w][h][0] = calculate_median(
                get_neighborhood_average(img_aux, w, h, 0)
            )
            img_matrix[w][h][1] = calculate_median(
                get_neighborhood_average(img_aux, w, h, 1)
            )
            img_matrix[w][h][2] = calculate_median(
                get_neighborhood_average(img_aux, w, h, 2)
            )

    return img_matrix


# Just a function to calculate average and avoid np.average
def calculate_average(neighborhood_array: array) -> int:
    return sum(neighborhood_array) / len(neighborhood_array)


# Just a function to calculate median and avoid np.median
def calculate_median(neighborhood_array: array) -> int:
    index_neighborhood_array = int(len(neighborhood_array) / 2)
    ordered_neighborhood_array = bubble_sort(neighborhood_array)

    return ordered_neighborhood_array[index_neighborhood_array]


# Just a function to order an array and avoid sort()
def bubble_sort(vetor) -> array:

    for i in range(0, len(vetor) - 1, 1):
        for j in range(i + 1, len(vetor), 1):
            if vetor[i] > vetor[j]:
                temp = vetor[i]
                vetor[i] = vetor[j]
                vetor[j] = temp

    return vetor


def show_histogram(
    frequencies_array,
    color,
    filename_original: str,
    output_path: str = None,
    save: bool = False,
) -> None:
    """
    Read an array of frequencies, show the histogram and save the image.

    Parameters
    ----------
        frequencies_array: array
            Array with the frequencies of color.
        color: str
            Color R, G or B.
        filename_original: str
            Original name of the file.
        output_path: str
            Output directory where the histogram will be save.
        save: bool
            Default is false. Save an image case True.

    Returns
    -------
        Show a picture on screen and save an image.
    """

    X = [i for i in range(256)]
    Y = frequencies_array

    plt.bar(X, Y, color=color, width=1)

    plt.title(f"Histogram for {color}")
    plt.xlabel(f"Level of {color}")
    plt.ylabel(f"Pixels frequency")

    if save:
        filename_original = filename_original.split(".")
        plt.savefig(f"{output_path}/{filename_original[0]}_{color}_histogram.png")
    plt.show()
    plt.close()


# Simple function to save the image.
def save_image(array: str, output: str, name: str) -> None:
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

    # Histogram for the original picture
    img_matrix = get_image_matrix(args.img)
    r, g, b = get_frequencies_arrays(img_matrix)

    show_histogram(
        r, "red", os.path.basename(args.img), output_path=args.output, save=True
    )
    show_histogram(
        g, "green", os.path.basename(args.img), output_path=args.output, save=True
    )
    show_histogram(
        b, "blue", os.path.basename(args.img), output_path=args.output, save=True
    )

    # Histogram for the picture after brightness
    new_image = change_brightness(img_matrix, 10)

    save_image(
        new_image,
        args.output,
        f"{str(os.path.basename(args.img)).split('.')[0]}_brightness",
    )
    img_brightness_name = (
        f"{str(os.path.basename(args.img)).split('.')[0]}_brightness.png"
    )
    img_matrix = get_image_matrix(os.path.join(args.output, img_brightness_name))
    r, g, b = get_frequencies_arrays(img_matrix)

    show_histogram(
        r,
        "red",
        img_brightness_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        g,
        "green",
        img_brightness_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        b,
        "blue",
        img_brightness_name,
        output_path=args.output,
        save=True,
    )

    # Histogram for the picture after average
    new_image_average = calculate_image_average(img_matrix)
    save_image(
        new_image_average,
        args.output,
        f"{str(os.path.basename(args.img)).split('.')[0]}_average",
    )
    img_average_name = f"{str(os.path.basename(args.img)).split('.')[0]}_average.png"
    print(img_average_name)
    img_matrix = get_image_matrix(os.path.join(args.output, img_average_name))
    r, g, b = get_frequencies_arrays(img_matrix)

    show_histogram(
        r,
        "red",
        img_average_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        g,
        "green",
        img_average_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        b,
        "blue",
        img_average_name,
        output_path=args.output,
        save=True,
    )

    # Histogram for the picture after median
    new_image_median = calculate_image_median(img_matrix)
    save_image(
        new_image_median,
        args.output,
        f"{str(os.path.basename(args.img)).split('.')[0]}_median",
    )
    img_median_name = f"{str(os.path.basename(args.img)).split('.')[0]}_median.png"
    print(img_median_name)
    img_matrix = get_image_matrix(os.path.join(args.output, img_median_name))
    r, g, b = get_frequencies_arrays(img_matrix)

    show_histogram(
        r,
        "red",
        img_median_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        g,
        "green",
        img_median_name,
        output_path=args.output,
        save=True,
    )
    show_histogram(
        b,
        "blue",
        img_median_name,
        output_path=args.output,
        save=True,
    )
