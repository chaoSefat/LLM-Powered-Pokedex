# Pokémon Image Identification

A Python application that uses computer vision and machine learning to identify Pokémon from webcam images and retrieve detailed information about them.

## Requirements

- Python 3.7+
- Webcam or camera device
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pokemon-identification.git
cd pokemon-identification
```

2. Install required packages:
```bash
pip install opencv-python requests openai python-dotenv
```

3. Set up your OpenAI API key:

Create a `.env` file in the project directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Point your camera at a Pokémon (can be a toy, card, image on screen, etc.) and run the application:
```bash
python pokemon_identification.py
```

2. The application will:
   - Identify the Pokémon using AI
   - Fetch detailed information from the PokéAPI
   - Display the results in your terminal


## Future Improvements

- Add live camera feed so that users can take pictures with ease.
- Add a graphical user interface (GUI).
- Include more detailed information and statistics.


## Acknowledgments

- OpenAI for the Vision API
- PokéAPI for the comprehensive Pokémon database
- The Pokémon Company for creating these wonderful creatures
