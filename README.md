# 🧠 Streamlit Quiz App

A comprehensive quiz application built with Streamlit for learning and testing knowledge.

## Features

- 📊 Interactive multiple-choice questions
- 📈 Personal statistics tracking
- 🔄 Randomized questions and answer options
- 📝 Progress tracking and detailed results
- 🚩 Question feedback system
- 💾 Persistent user statistics

## Quick Start

### Option 1: Use the Deployed App (Recommended for non-technical users)

Click this link to use the app directly: [Quiz App on Streamlit Cloud](https://your-app-url.streamlit.app)

### Option 2: Run Locally

1. Clone this repository:
```bash
git clone https://github.com/your-username/streamlit-quiz-app.git
cd streamlit-quiz-app
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your forked repository
6. Set main file path to `app.py`
7. Click "Deploy"

Your app will be available at a public URL that you can share with anyone!

### Alternative Deployment Options

- **Heroku**: Use the included `Procfile` for Heroku deployment
- **Railway**: Connect your GitHub repo to Railway for automatic deployment
- **Render**: Deploy directly from GitHub with zero configuration

## File Structure

```
streamlit-quiz-package/
├── app.py                 # Main application file
├── questions.json         # Quiz questions database
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment file
├── .streamlit/           # Streamlit configuration
│   └── config.toml
└── README.md             # This file
```

## Configuration

The app can be configured by modifying the `questions.json` file. Each question should follow this format:

```json
{
  "question": "Your question text here?",
  "options": [
    "Option A",
    "Option B", 
    "Option C",
    "Option D"
  ],
  "correct_answer": ["Option A", "Option C"]
}
```

## Features Details

### Statistics Tracking
- Individual question performance
- Overall quiz completion rate
- Success rate per question
- Historical answer tracking

### User-Friendly Features
- Progress indicators
- Immediate feedback
- Detailed result summaries
- Question problem reporting

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/your-username/streamlit-quiz-app/issues) page
2. Create a new issue if your problem isn't already reported

## License

This project is open source and available under the [MIT License](LICENSE).
