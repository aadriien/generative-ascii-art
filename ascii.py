import requests
from PIL import Image

from ascii_magic import AsciiArt
from ansi2html import Ansi2HTMLConverter

from flask import Flask, request, render_template

app = Flask(__name__)

AI_URL_BASE = "https://image.pollinations.ai/prompt"



def generate_image(prompt):
    response = requests.get(f"{AI_URL_BASE}/{prompt}")

    if response.status_code != 200:
        raise ValueError("Error: could not reach URL")

    with open('image.jpg', 'wb') as file:
        file.write(response.content)

    return response.url


def generate_ascii_from_image(image_filepath='image.jpg'):
    my_art = AsciiArt.from_image(image_filepath)
    ascii_art = my_art.to_terminal(columns=70)

    converter = Ansi2HTMLConverter()
    ascii_art_html = converter.convert(ascii_art)
    
    return ascii_art_html


def convert_image_to_ascii(image_filepath='image.jpg'):
    # Download image from URL
    image = Image.open(image_filepath)

    # Resize for ASCII conversion
    width, height = image.size
    aspect_ratio = height / width
    new_width = 70 
    new_height = int(aspect_ratio * new_width * 0.55) 
    image = image.resize((new_width, new_height))

    # Convert image to grayscale
    image = image.convert("L")

    # ASCII chars to map grayscale values
    chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

    pixels = image.getdata()
    ascii_str = "".join([chars[pixel // 25] for pixel in pixels])

    # Format ASCII string into rows
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[i:i + new_width] for i in range(0, ascii_str_len, new_width)])

    return ascii_img


@app.route("/", methods=["GET", "POST"])
def index():
    image_url = ""
    ascii_art_custom = ""
    ascii_art_magic = ""

    if request.method == "POST":
        prompt = request.form["prompt"]
        image_url = generate_image(prompt)

        # Generate ASCII art using both methods
        ascii_art_magic = generate_ascii_from_image()
        ascii_art_custom = convert_image_to_ascii()

    return render_template("index.html", image_url=image_url, ascii_art_magic=ascii_art_magic, ascii_art_custom=ascii_art_custom)



# def main():
#     prompt = "A fish riding a bike with sunglasses"
    
#     # Step 1: Generate image from prompt
#     image_url = generate_image(prompt)
#     print(f"Generated image URL: {image_url}")
#     print("\n\n\n")

#     generate_ascii_from_image()
#     print("\n\n\n")
    
#     # Step 2: Convert generated image to ASCII
#     ascii_art = convert_image_to_ascii()
#     print("Generated ASCII Art:\n")
#     print(ascii_art)


if __name__ == "__main__":
    # main()
    app.run(debug=True)


