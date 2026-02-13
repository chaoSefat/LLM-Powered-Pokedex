# 🔴 AI Pokédex - Streamlit Edition

A production-ready web application that identifies Pokémon from images using OpenAI Vision and displays detailed stats from PokéAPI.

## ✨ Features

- **Browser Camera Integration**: Capture images directly from your device camera (works on desktop & mobile)
- **AI Vision Identification**: Uses GPT-4o Vision to identify Pokémon from images
- **Rich Pokémon Data**: Displays sprites, types, abilities, height, weight, and full base stats
- **Smart Caching**: PokéAPI responses cached for 1 hour to improve performance
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile browsers
- **Error Handling**: Graceful error messages for network failures and API issues
- **Environment Variables**: Secure API key management via environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))

### Installation

1. **Navigate to the repository**

   ```bash
   cd LLM-Powered-Pokedex
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

The app will open at `http://localhost:8501`

## 📱 Usage

1. Click **"Take a Picture"** to access your device camera
2. Capture an image of a Pokémon (card, artwork, or photo)
3. Click **"Capture & Analyze"** to identify it
4. View detailed Pokémon information:
   - Official artwork/sprite
   - Type badges
   - Height & weight metrics
   - Abilities
   - Full base stats with visual progress bars

## 🏗️ Architecture

### Core Functions

- **`encode_image(image_bytes)`** - Converts image bytes to base64 string
- **`predict_pokemon(base64_image)`** - Calls OpenAI Vision API to identify Pokémon
- **`clean_name(raw_prediction)`** - Formats Pokémon name for API queries
- **`fetch_pokemon_data(pokemon_name)`** - Fetches comprehensive data from PokéAPI (cached)
- **`render_pokemon_info(data)`** - Renders detailed UI with stats and visuals

### State Management

Uses Streamlit's `st.session_state` to:

- Store current Pokémon data
- Prevent redundant API calls
- Maintain captured image reference

### Caching Strategy

- **PokéAPI responses**: Cached for 1 hour using `@st.cache_data`
- **Session state**: Preserves results during user interaction

## 🔐 Security

- **No hardcoded API keys**: Uses `os.getenv("OPENAI_API_KEY")`
- **Environment variable only**: Set via system environment or `.streamlit/secrets.toml`
- **Safe for deployment**: Ready for Streamlit Community Cloud

## 📦 Deployment to Streamlit Community Cloud

1. **Push to GitHub** (public repo)

   ```bash
   git add .
   git commit -m "Add AI Pokédex Streamlit app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repo, branch, and `app.py`
   - Add environment variable in "Advanced settings":
     - Key: `OPENAI_API_KEY`
     - Value: Your OpenAI API key
   - Deploy!

## 🛠️ Tech Stack

- **Streamlit** - Web framework for rapid prototyping
- **OpenAI** - GPT-4o Vision for Pokémon identification
- **PokéAPI** - Pokémon data source
- **Requests** - HTTP client for API calls
- **Pillow** - Image processing

## 📊 Performance Optimizations

- Efficient base64 encoding
- Cached PokéAPI responses (1-hour TTL)
- Session state to avoid reprocessing
- Streamlit spinner feedback during API calls
- Responsive image loading with official artwork

## 🎨 UI/UX Highlights

- Centered, polished layout
- Emoji-based visual feedback
- Type-based color badges
- Stat visualization with progress bars
- Mobile-optimized camera input
- Clear error messages
- "Start Over" button for new searches

## 🐛 Error Handling

The app gracefully handles:

- Missing OPENAI_API_KEY environment variable
- Network timeouts (5-second timeout on API calls)
- Pokémon not found in PokéAPI (404)
- API rate limits and failures
- Invalid image captures

## 📝 Requirements

See `requirements.txt` for pinned versions:

- streamlit==1.28.1
- openai==1.3.8
- requests==2.31.0
- Pillow==10.1.0

## 🤝 Contributing

Feel free to extend this project:

- Add team comparison features
- Include move information from PokéAPI
- Add sound effects
- Implement evolutionary chain display
- Add multi-language support

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, OpenAI, and PokéAPI**

## Acknowledgments

- OpenAI for the Vision API
- PokéAPI for the comprehensive Pokémon database
- The Pokémon Company for creating these wonderful creatures
