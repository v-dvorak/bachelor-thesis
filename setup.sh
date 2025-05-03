# !/bin/bash

cd "$(dirname "$0")"

if [ $# -ne 1 ]; then
  echo "Usage: $0 /path/to/python"
  exit 1
fi

PYTHON=$1

echo "🐍 Creating virtual environment..."
"$PYTHON" -m venv .venv

if [ $? -ne 0 ]; then
  echo "❌ Failed to create virtual environment"
  exit 1
fi
echo "✅ Virtual environment created at ./.venv"

echo "🐍 Updating pip..."
.venv/bin/pip3 install --upgrade pip

echo "📦 Installing StaLiX..."
cd stalix || exit 1
../.venv/bin/pip install -e .[viz]
cd ..

echo "📦 Installing od-tools..."
cd od-tools || exit 1
../.venv/bin/pip install -e .
cd ..

echo "📦 Installing TonIC dependencies..."
cd tonic || exit 1
../.venv/bin/pip install -r requirements.txt
cd ..

echo "🐍 Verifying installation..."
.venv/bin/python -c "import odtools, stalix; print('✅ Libraries od-tools and StaLiX are importable.')"
if [ $? -ne 0 ]; then
  echo "❌ Import test failed. Please check installation."
  exit 1
fi

echo "🎉 Done!"
