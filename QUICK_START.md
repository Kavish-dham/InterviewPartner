# Quick Start Guide - Terminal Commands

## Initial Setup (One-time)

```bash
# Navigate to project directory
cd "/Users/kavishdham/Desktop/Interview Partner"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Method 1: Quick Run Script
```bash
./run.sh
```

### Method 2: Manual Activation
```bash
# Activate venv
source venv/bin/activate

# Run application
python main.py
```

### Method 3: One-line Command
```bash
source venv/bin/activate && python main.py
```

## Deactivating Virtual Environment

When you're done, you can deactivate the virtual environment:
```bash
deactivate
```

## Verifying Installation

To verify all dependencies are installed correctly:
```bash
source venv/bin/activate
python -c "import PyPDF2; import pdfplumber; print('✓ All dependencies verified')"
```

## Troubleshooting

If you encounter issues:

1. **Virtual environment not found**: Recreate it
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Permission denied on run.sh**: Make it executable
   ```bash
   chmod +x run.sh
   ```

3. **Python version issues**: Ensure you're using Python 3.7+
   ```bash
   python3 --version
   ```

