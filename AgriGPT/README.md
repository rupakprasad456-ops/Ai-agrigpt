# AgriGPT - AI Agent for Farmers

An intelligent AI assistant designed to help farmers with crop recommendations, weather updates, and government scheme information.

## Features

- 🌱 **Crop Recommendation** - Get personalized crop suggestions based on soil, climate, and region
- 🌤️ **Weather Updates** - Real-time weather forecasts to plan farming activities
- 📋 **Govt Schemes Info** - Information about government agricultural schemes and subsidies

## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI
- **AI**: OpenAI GPT-4 API
- **Weather Data**: OpenWeatherMap API

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AgriGPT
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
     - `OPENWEATHERMAP_API_KEY` - Get from https://openweathermap.org/api

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
AgriGPT/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## API Keys Required

### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it to your `.env` file

### OpenWeatherMap API Key
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key
4. Copy it to your `.env` file

## Usage Guidelines

- Provide accurate location information for better crop recommendations
- Check weather regularly for optimal farming decisions
- Stay updated with latest government schemes

## License

MIT License