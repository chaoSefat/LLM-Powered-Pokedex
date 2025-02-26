import cv2
import requests
import base64
import os
import json
from openai import OpenAI

### The first thing we are gonna do is to make a function that captures image with your web cam.

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    ret,frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        exit()
    
    img_path = "image.jpg"
    cv2.imwrite(img_path, frame)
    cap.release()
    cv2.destroyAllWindows()
    return img_path

### Now we will encode the image to 64 bit string.

def encode_image(img_path):
    with open(img_path, "rb") as img_file:
        img_str = base64.b64encode(img_file.read()).decode("utf-8")
        return img_str
    
### Now a function that makes a call to OpenAI API and gets response.
def get_pokemon_name(img_path):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OpenAI API Key not provided."
    
    client = OpenAI(api_key=api_key)
    
    try:
        # Base64 encode the image
        with open(img_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that identifies Pokemon from images."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What Pokemon is this? Provide only the name."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=10
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error Identifying Pokemon: {str(e)}")
        return None
    
def get_pokemon_info(pokemon_name):
    if not pokemon_name:
        return "Error: Pokemon name not provided."
    
    clean_name = pokemon_name.strip().lower().replace(" ", "-")

    try:
        api_url = f"https://pokeapi.co/api/v2/pokemon/{clean_name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            pokemon_info ={
                "name": data["name"].capitalize(),
                "type": [t["type"]["name"].capitalize() for t in data["types"]],
                "abilities": [a["ability"]["name"].capitalize() for a in data["abilities"]],
                "height": data["height"],
                "weight": data["weight"],
            }
            return pokemon_info
        else:
            return "Error: Pokemon not found."
    except Exception as e:
        print(f"Error Fetching Pokemon Info: {str(e)}")
        return None 

def main():
    print("Capturing Image...")
    img_path = capture_image()

    print("Identifying Pokemon...")
    pokemon_name = get_pokemon_name(img_path)
    print(f"Pokemon Name: {pokemon_name}")

    print("Fetching Pokemon Info...")
    pokemon_info = get_pokemon_info(pokemon_name)
    print(pokemon_info)

if __name__ == "__main__":
    main()
