#!/bin/bash
echo "🔧 Installing dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install selenium beautifulsoup4 openai pandas pyyaml python-dotenv
echo "✅ Done. Run with: python main.py"

