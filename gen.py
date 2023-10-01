import os
import random
from concurrent.futures import ThreadPoolExecutor
from time import time_ns

from PIL import Image, ImageDraw, ImageFont


def generate_image_with_text(text, font_path, result_path):
    # Create a blank image
    background_color = "white"  # Background color

    # Define font size and color
    font_size = 20
    font_color = "black"

    # Load the specified font
    font = ImageFont.truetype(font_path, font_size)

    # print("Generating image with text:", text, font.getbbox(text))
    # Calculate text position
    x, y, text_width, text_height = font.getbbox(text)
    image = Image.new("RGB", (text_width + 40, text_height + 40), background_color)
    draw = ImageDraw.Draw(image)

    # Add the text to the image
    draw.text((x + 20, y + 20), text, font=font, fill=font_color)

    # Save the image to the result path
    image.save(result_path)
    # print("Image saved to", result_path)


def append_text_to_file(text, file_path):
    with open(file_path, "a") as f:
        f.write(text + "\n")
    # print("Text appended to", file_path)


vocab = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~ '


def load_all_sentences(input_path):
    with open(input_path, "r") as f:
        sentences = f.readlines()
        sentences = [sentence.strip() for sentence in sentences]
        # remove all characters not in vocab
        sentences = ["".join([c for c in sentence if c in vocab]) for sentence in sentences]
        return sentences


vietnamese_sentences = load_all_sentences("./data/sentences.txt")
# print first 10 sentences
print(vietnamese_sentences[:10])


def generate_random_vietnamese_sentence():
    # Choose a random Vietnamese sentence
    random_sentence = random.choice(vietnamese_sentences)
    return random_sentence


def generate_time_and_random_string(prefix):
    # Get current time in nanoseconds
    current_time_nano = str(time_ns())

    # Generate a random number (between 0 and 999999)
    random_number = str(random.randint(0, 999999))

    # Concatenate the current time in nanoseconds and the random number
    result_string = prefix + current_time_nano + random_number
    return result_string


annotation_path = "./data/train_custom_annotation.txt"
annotation_test_path = "./data/test_custom_annotation.txt"


def generate_train_data(font_path, annotation_path, train_name, font_name):
    random_vietnamese_sentence = generate_random_vietnamese_sentence()

    text = random_vietnamese_sentence
    # file name = current system time nanoseconds + random number
    file_name = f'{generate_time_and_random_string(font_name)}'

    result_short_path = f"{train_name}/{file_name}.jpg"
    result_path = f"./data/{train_name}/{file_name}.jpg"

    # check mkdir parent of result_path
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    generate_image_with_text(text, font_path, result_path)
    append_text_to_file(result_short_path + "	" + text, annotation_path)


if __name__ == '__main__':
    # remove annotation_path
    if os.path.exists(annotation_path):
        os.remove(annotation_path)
    # remove annotation_test_path
    if os.path.exists(annotation_test_path):
        os.remove(annotation_test_path)
    # remove all files in train_custom
    for file in os.listdir('./data/train_custom'):
        os.remove(f'./data/train_custom/{file}')
    # remove all files in test_custom
    for file in os.listdir('./data/test_custom'):
        os.remove(f'./data/test_custom/{file}')

    num_workers = 100
    # create threadpool with num_workers
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # loop 10_000 times
        listdir = os.listdir('./fonts')
        for i in range(4000):
            # loop all fonts
            for font in listdir:
                executor.submit(generate_train_data, f'./fonts/{font}', annotation_path, 'train_custom', '')

        for i in range(1000):
            # loop all fonts
            for font in listdir:
                executor.submit(generate_train_data, f'./fonts/{font}', annotation_test_path, 'test_custom', '')
