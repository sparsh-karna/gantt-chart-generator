#!/bin/bash

# Gantt Generator Setup Script

echo "🚀 Setting up Gantt Chart Generator..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install requirements
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully!"
else
    echo "❌ Failed to install packages. Please check the error messages above."
    exit 1
fi

# Make the script executable
chmod +x gantt_generator.py

echo
echo "🎉 Setup complete!"
echo
echo "📋 Quick start commands:"
echo "  Generate sample data:    python3 gantt_generator.py --sample"
echo "  Create chart from CSV:   python3 gantt_generator.py example_project.csv"
echo "  Get help:               python3 gantt_generator.py --help"
echo
echo "📖 See README.md for detailed usage instructions."
