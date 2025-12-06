#!/bin/bash

# Zochi Setup Script
# This script sets up the environment for running Zochi components

set -e  # Exit on error

echo "=========================================="
echo "Zochi Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Check which component to install
echo ""
echo "Which component would you like to set up?"
echo "1) CS-ReFT (Parameter-efficient fine-tuning)"
echo "2) Tempest (Jailbreak testing)"
echo "3) Both"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Installing CS-ReFT dependencies..."
        pip install -r csreft/requirements.txt
        echo "CS-ReFT setup complete!"
        ;;
    2)
        echo "Installing Tempest dependencies..."
        pip install -r tempest/requirements.txt
        echo "Tempest setup complete!"
        ;;
    3)
        echo "Installing CS-ReFT dependencies..."
        pip install -r csreft/requirements.txt
        echo "Installing Tempest dependencies..."
        pip install -r tempest/requirements.txt
        echo "Both components setup complete!"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "Please copy .env.example to .env and fill in your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your favorite editor"
else
    echo "✓ .env file found"
fi

# Create necessary directories
echo ""
echo "Creating output directories..."
mkdir -p outputs
mkdir -p checkpoints
mkdir -p logs

echo ""
echo "=========================================="
echo "Setup Complete! ✓"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Set up your .env file with API keys (if not done already)"
echo "3. Run one of the components:"
echo ""
echo "   For CS-ReFT:"
echo "   cd csreft"
echo "   python csrf_train_instruct.py --output_dir ../outputs/csrf_model --run_eval"
echo ""
echo "   For Tempest:"
echo "   cd tempest"
echo "   python tempest_pipeline.py --target_model gpt-4-turbo --pipeline_model gpt-4-turbo --results_json ../outputs/results.json --resume"
echo ""
