# WhatsApp Photo Extractor

Extract photos from WhatsApp chat exports and create Word documents with organized captions.

## Distribution Options for Other Computers

### Option 1: Simple User-Friendly Distribution
**Best for non-technical users**

**What to share:**
1. `WhatsApp_Photo_Extractor.bat` (double-click to run)
2. `whatsapp_photo_extractor.py` (the main script)
3. `README.md` (these instructions)

**User Requirements:**
- Windows computer
- Python 3.6+ installed (download from python.org)
- Run: `pip install python-docx`

**How users run it:**
1. Put their WhatsApp zip file in the same folder
2. Double-click `WhatsApp_Photo_Extractor.bat`
3. Follow the interactive prompts

### Option 2: Standalone Executable
**Best for users who don't want to install Python**

**What to share:**
1. `WhatsApp_Photo_Extractor.exe` (from the `dist` folder)
2. This README file

**User Requirements:**
- Windows computer only
- No Python installation needed

**How users run it:**
- Double-click the .exe file or
- Open Command Prompt and run with parameters

### Option 3: Python Script with Requirements
**Best for technical users**

**What to share:**
1. `whatsapp_photo_extractor.py`
2. `requirements.txt` (create this file with: python-docx)

**User Requirements:**
- Python 3.6+ installed
- Run: `pip install -r requirements.txt`

## Usage Examples

### Interactive Mode (Easiest)
```cmd
python whatsapp_photo_extractor.py --interactive
```
OR double-click `WhatsApp_Photo_Extractor.bat`

### Command Line Examples
```cmd
# Default - all photos
python whatsapp_photo_extractor.py

# Last month only
python whatsapp_photo_extractor.py --last-month

# Custom date range
python whatsapp_photo_extractor.py --start-date "01/08/2025" --end-date "31/08/2025"

# Extract photos only (no Word document)
python whatsapp_photo_extractor.py --last-month --extract-only

# Custom output files
python whatsapp_photo_extractor.py --last-month -o "August_Photos.docx" -e "august_pics"
```

## What the Script Does

1. **Extracts photos** from WhatsApp zip exports
2. **Renames files** with format: `YYMMDD_Initials_DescriptiveText.jpg`
   - Example: `250815_MP_beach sunset.jpg`
3. **Creates Word document** with:
   - Photos sized to quarter-page
   - Captions showing sender, date, time, and message text
   - Title includes date range if filtered
4. **Handles date filtering** for specific time periods

## File Naming Convention

Photos are renamed with:
- **YYMMDD**: Date (e.g., 250815 for Aug 15, 2025)
- **Initials**: Sender's initials (e.g., MP for Martin Philipp)
- **Description**: First 15 characters of descriptive words from message

## Troubleshooting

**"WhatsApp Chat.zip not found"**
- Rename your zip file to "WhatsApp Chat.zip" or specify the correct name

**"No chat text file found"**
- Ensure your zip contains the .txt chat file from WhatsApp export

**"python is not recognized"**
- Install Python from python.org and add it to PATH

**Executable doesn't work**
- Try the Python script version instead
- Make sure the .exe is not blocked by antivirus

## Technical Notes

- Supports WhatsApp date formats: DD/MM/YY and DD/MM/YYYY
- Filters out common words to extract meaningful descriptions
- Handles duplicate filenames with _1, _2, etc.
- Creates temporary folders for processing
- Supports both individual photos and batch processing