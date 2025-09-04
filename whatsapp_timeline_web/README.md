# WhatsApp Timeline Web Generator

A Python application that transforms WhatsApp chat exports into beautiful timeline webpages, similar to corporate history pages like Hutchinson Builders' timeline.

## Features

- **📅 Year-based Organization**: Automatically organizes photos and messages by year
- **🖼️ Smart Photo Selection**: Intelligently selects representative images for each year
- **🎨 Beautiful Web Design**: Modern, responsive timeline with smooth animations
- **📊 Statistics & Themes**: Extracts themes and shows activity statistics
- **🔍 Interactive Elements**: Year navigation, photo lightbox, hover effects

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

2. **Prepare Data**:
   - Export your WhatsApp chat with media
   - Place the zip file in `data/input/`

3. **Generate Timeline**:
   ```bash
   python whatsapp_timeline_generator.py --title "My Timeline" --max-photos 5
   ```

4. **View Result**:
   - Open `data/output/timeline.html` in your browser

## Usage Options

```bash
# Basic usage
python whatsapp_timeline_generator.py

# Custom options
python whatsapp_timeline_generator.py \
  --input "path/to/chat.zip" \
  --output "path/to/output" \
  --title "Project Timeline" \
  --max-photos 6
```

## Output Structure

```
data/output/
├── timeline.html          # Main timeline webpage
└── images/                # Processed and renamed photos
    ├── 20191115_SMC_filename.jpg
    └── ...
```

## Timeline Features

- **Year Sections**: Each year gets its own section with header and statistics
- **Photo Cards**: Hover effects and click-to-expand lightbox viewing  
- **Theme Detection**: Automatically extracts keywords from message content
- **Statistics**: Shows total photos, messages, active months per year
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Navigation**: Year-based navigation with smooth scrolling

## How It Works

1. **Parse WhatsApp Export**: Extracts messages and identifies photo attachments
2. **Organize by Year**: Groups content chronologically 
3. **Select Representative Photos**: Chooses diverse, well-distributed images
4. **Extract Themes**: Analyzes message text for keywords and topics
5. **Generate Statistics**: Calculates activity metrics for each year
6. **Create Webpage**: Renders beautiful HTML using Jinja2 templates
7. **Process Images**: Copies and renames photos with descriptive filenames

## Dependencies

- **Jinja2**: Template rendering
- **Pillow**: Image processing
- **Python 3.7+**: Core functionality

## Directory Structure

```
whatsapp_timeline_web/
├── src/
│   ├── whatsapp_timeline_generator.py  # Main script
│   └── requirements.txt                # Dependencies
├── templates/
│   └── timeline.html                   # Jinja2 template
├── data/
│   ├── input/                          # WhatsApp zip files (gitignored)
│   └── output/                         # Generated files (gitignored)
└── README.md
```

## Example Output

The generated timeline includes:
- **Interactive year navigation** at the top
- **Beautiful photo cards** with hover effects  
- **Theme tags** showing key topics for each year
- **Activity statistics** (photos, messages, active months)
- **Lightbox viewing** for full-size images
- **Mobile-responsive** design that works everywhere

Perfect for creating professional-looking timelines from your WhatsApp project communications!