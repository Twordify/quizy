#!/bin/bash

# Deploy to Streamlit Community Cloud
# This script helps you prepare your app for deployment

echo "🚀 Preparing Streamlit Quiz App for deployment..."

# Check if all required files exist
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

if [ ! -f "questions.json" ]; then
    echo "❌ questions.json not found!"
    exit 1
fi

echo "✅ All required files found!"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Streamlit Quiz App"
    echo "✅ Git repository initialized!"
else
    echo "✅ Git repository already exists!"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Add the remote: git remote add origin https://github.com/your-username/your-repo-name.git"
echo "3. Push your code: git push -u origin main"
echo "4. Go to https://share.streamlit.io"
echo "5. Connect your GitHub repository"
echo "6. Deploy your app!"
echo ""
echo "📖 For detailed instructions, see README.md"
