# QR Code Generator

Generate SVG QR codes from CSV files with automatic PDF index generation.

## Features

- **High error correction** QR codes in SVG format (~40mm size)
- **Batch processing** from CSV files
- **PDF index** with all QR codes for verification (A4, 4×5 grid, multi-page)
- **Timestamped output** folders for easy organization
- **Windows GUI support** - double-click to run

## Quick Start

### Method 1: Double-Click (Easiest)

1. **Prepare your data**: Create/edit `input.csv` with this format:
   ```csv
   filename,url
   bou001,http://qrtub.com/_a9f2k
   bou002,http://qrtub.com/_z3x7m
   bou003,http://qrtub.com/_t4g8r
   ```

2. **Generate QR codes**: Double-click `Generate QR Codes.bat`

3. **Find your output**: Check the new timestamped folder (e.g., `250822_094431_qr_codes/`)

### Method 2: Command Line (Advanced)

```bash
# Install dependencies first
pip install -r requirements.txt

# Basic usage (uses input.csv)
python qr_generator.py

# Specify custom CSV file
python qr_generator.py my_data.csv

# Specify both CSV file and output folder
python qr_generator.py my_data.csv my_output_folder
```

## Command Line Options

| Command | Description | Output Folder |
|---------|-------------|---------------|
| `python qr_generator.py` | Uses `input.csv` | `250822_094431_qr_codes` (auto-timestamped) |
| `python qr_generator.py data.csv` | Uses `data.csv` | `250822_094431_qr_codes` (auto-timestamped) |
| `python qr_generator.py data.csv batch1` | Uses `data.csv` | `batch1` |

## CSV File Format

Your CSV file must have exactly two columns: `filename` and `url`

```csv
filename,url
product001,https://mysite.com/product/001
product002,https://mysite.com/product/002
label_a,http://qrtub.com/_abc123
label_b,http://qrtub.com/_def456
```

- **filename**: Used for the SVG filename (e.g., `product001.svg`)
- **url**: The URL that will be encoded in the QR code

## Output

Each run generates:

### Individual QR Codes
- **Format**: SVG vector files
- **Size**: ~40mm × 40mm (perfect for printing)
- **Error correction**: High (can handle damage/dirt)
- **Naming**: `{filename}.svg`

### Index PDF
- **Layout**: A4 pages with 4×5 grid (20 QR codes per page)
- **Contains**: Visual QR codes with filename and URL labels
- **Filename**: `QR_Index_YYMMDD_HHMMSS.pdf`
- **Purpose**: Verification and batch tracking

### Folder Structure
```
250822_094431_qr_codes/
├── bou001.svg
├── bou002.svg
├── bou003.svg
├── ...
└── QR_Index_250822_094431.pdf
```

## Installation

1. **Download** all files to a folder
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ready to use!**

## Technical Specifications

- **QR Code Version**: Auto-fit (typically Version 1-4)
- **Error Correction**: Level H (High - ~30% recovery)
- **Module Size**: 13 points per module
- **Border**: 1 module
- **Output Size**: ~40.3mm × 40.3mm
- **Format**: SVG (scalable vector graphics)

## Printing Recommendations

- **Print from SVG files** for best quality (not the PDF)
- **Scale down** rather than up for crisp edges
- **Test scan** a sample before printing large batches
- **PDF index** is for verification only

## Troubleshooting

### "input.csv not found"
Create an `input.csv` file in the same folder as the script.

### "CSV file must contain 'filename' and 'url' columns"
Check your CSV has the exact column headers: `filename,url`

### "Module not found" errors
Install dependencies: `pip install -r requirements.txt`

### QR codes don't scan
- Check URLs are valid and reachable
- Ensure sufficient print quality
- Test with different QR scanner apps

## Files Included

- `qr_generator.py` - Main Python script
- `Generate QR Codes.bat` - Windows double-click launcher
- `requirements.txt` - Python dependencies
- `input.csv` - Sample data file
- `README.md` - This documentation

## Example Workflow

1. **Prepare data**: Update `input.csv` with your URLs
2. **Generate**: Double-click `Generate QR Codes.bat`
3. **Verify**: Check the PDF index for accuracy
4. **Print**: Use individual SVG files for production
5. **Archive**: Keep timestamped folders for batch tracking

---

*Generated with QR Code Generator - Perfect for product labels, marketing materials, and inventory management.*