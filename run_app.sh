#!/bin/bash

# Script to run the Business Growth Potential Streamlit app

echo "🚀 Starting the Business Growth Potential app..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating a new one..."
    python -m venv venv
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if necessary files exist
echo "🔍 Checking necessary files..."

if [ ! -f "dados/data.csv" ]; then
    echo "❌ File dados/data.csv not found!"
    exit 1
fi

if [ ! -f "modelos/Random_Forest_model.joblib" ]; then
    echo "❌ Model Random_Forest_model.joblib not found!"
    exit 1
fi

echo "✅ All necessary files found!"

# Check if we can load data locally (to avoid GitHub rate limiting during testing)
if [ -f "dados/data.csv" ] && [ -f "modelos/Random_Forest_model.joblib" ]; then
    echo "📁 Using local files - no GitHub download needed!"
else
    echo "🌐 Will download files from GitHub (ensure internet connection)"
    echo "💡 Tip: Place data.csv and Random_Forest_model.joblib in their respective folders to avoid GitHub rate limits"
fi

# Run the app
echo "🌟 Running the Streamlit app..."
# Don't specify port - let Streamlit Cloud manage it
streamlit run app.py
