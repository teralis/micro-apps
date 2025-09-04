#!/usr/bin/env python3
"""
WhatsApp Timeline Web Generator
Creates a beautiful timeline webpage from WhatsApp chat exports
Similar to corporate history timelines with yearly sections and curated content
"""

import zipfile
import re
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from jinja2 import Template
import argparse
from PIL import Image, ImageOps
import random

def parse_message_date(date_str):
    """Parse WhatsApp date string to datetime object."""
    try:
        # Handle format like "15/11/2019" or "dd/mm/yyyy"
        parts = date_str.split('/')
        if len(parts) == 3:
            day, month, year = parts
            if len(year) == 2:
                year = '20' + year if int(year) < 50 else '19' + year
            return datetime(int(year), int(month), int(day))
    except:
        pass
    return None

def parse_chat_messages(chat_content):
    """Parse WhatsApp chat content and extract messages with metadata."""
    if isinstance(chat_content, bytes):
        chat_content = chat_content.decode('utf-8', errors='replace')
    
    messages = []
    lines = chat_content.split('\n')
    
    # Pattern to match WhatsApp message format: [15/11/2019, 4:38:17 pm] SMC: message
    message_pattern = r'^\[(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}:\d{2}(?:\u202f)?(?:am|pm)?)\] ([^:]+): (.+)$'
    
    current_message = None
    
    for line in lines:
        line = line.strip('\r\n ')
        if not line:
            continue
        
        # Clean up Unicode characters
        line = line.replace('\u200e', '')  # Left-to-right mark
        
        match = re.match(message_pattern, line)
        if match:
            date_str, time_str, sender, content = match.groups()
            time_str = time_str.replace('\u202f', ' ')
            
            current_message = {
                'date': date_str,
                'time': time_str,
                'sender': sender.strip(),
                'content': content.strip(),
                'full_content': content.strip(),
                'datetime': parse_message_date(date_str)
            }
            messages.append(current_message)
        else:
            if current_message and line:
                current_message['full_content'] += '\n' + line
    
    return messages

def find_photo_messages(messages):
    """Find messages that contain photo attachments."""
    photo_messages = []
    
    for message in messages:
        # Look for different attachment patterns
        content = message['full_content']
        
        if ('<attached:' in content or 
            '.jpg>' in content or 
            '.jpeg>' in content or 
            '.png>' in content or
            'PHOTO-' in content):
            
            # Try to extract filename from various formats
            filename_patterns = [
                r'<attached: ([^>]+\.(?:jpg|jpeg|png))>',  # <attached: filename.jpg>
                r'(IMG-\d{8}-WA\d{4}\.jpg)',              # IMG-20191115-WA0003.jpg
                r'(\d{8}-PHOTO-[^>]+\.jpg)',              # 00000003-PHOTO-2019-11-15-17-36-42.jpg
                r'([^<>\s]+\.(?:jpg|jpeg|png))'           # Generic image file
            ]
            
            image_filename = None
            for pattern in filename_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    image_filename = match.group(1)
                    break
            
            if image_filename:
                message['image_filename'] = image_filename
                photo_messages.append(message)
    
    return photo_messages

def extract_themes_from_text(text):
    """Extract themes/keywords from message text."""
    # Remove file attachment references
    text = re.sub(r'IMG-\d{8}-WA\d{4}\.jpg \(file attached\)', '', text)
    text = text.lower().strip()
    
    if not text:
        return []
    
    # Common meaningful words that indicate themes
    theme_words = []
    words = re.findall(r'\b\w{4,}\b', text)  # Words 4+ characters
    
    # Filter out common stop words but keep meaningful ones
    stop_words = {
        'that', 'this', 'with', 'from', 'they', 'were', 'been', 'have', 
        'will', 'your', 'what', 'when', 'where', 'there', 'their'
    }
    
    for word in words[:10]:  # Limit to first 10 words
        if word not in stop_words and len(word) >= 4:
            theme_words.append(word.capitalize())
    
    return theme_words

def select_representative_photos(photo_messages, max_per_year=6):
    """Select representative photos for each year using various criteria."""
    if len(photo_messages) <= max_per_year:
        return photo_messages
    
    # Sort by date
    photo_messages.sort(key=lambda x: x['datetime'] or datetime.min)
    
    # Try to get diverse selection across the year
    selected = []
    total_photos = len(photo_messages)
    
    # Method 1: Even distribution across the year
    if total_photos > max_per_year:
        step = total_photos // max_per_year
        for i in range(0, total_photos, step):
            if len(selected) < max_per_year:
                selected.append(photo_messages[i])
    
    # Method 2: If we still need more variety, add random selections
    remaining = [msg for msg in photo_messages if msg not in selected]
    while len(selected) < max_per_year and remaining:
        selected.append(remaining.pop(random.randint(0, len(remaining) - 1)))
    
    return selected[:max_per_year]

def organize_by_year(photo_messages):
    """Organize photo messages by year with statistics and themes."""
    years_data = defaultdict(lambda: {
        'photos': [],
        'themes': Counter(),
        'total_messages': 0,
        'active_months': set(),
        'senders': set()
    })
    
    for message in photo_messages:
        if not message['datetime']:
            continue
            
        year = message['datetime'].year
        month = message['datetime'].month
        
        years_data[year]['photos'].append(message)
        years_data[year]['total_messages'] += 1
        years_data[year]['active_months'].add(month)
        years_data[year]['senders'].add(message['sender'])
        
        # Extract themes from message text
        themes = extract_themes_from_text(message['full_content'])
        for theme in themes:
            years_data[year]['themes'][theme] += 1
    
    # Process each year's data
    processed_years = []
    for year in sorted(years_data.keys()):
        data = years_data[year]
        
        # Select representative photos
        selected_photos = select_representative_photos(data['photos'])
        
        # Get top themes
        top_themes = [theme for theme, count in data['themes'].most_common(8)]
        
        # Generate year summary
        summary = generate_year_summary(year, data, selected_photos)
        
        processed_years.append({
            'year': year,
            'photos': selected_photos,
            'themes': top_themes,
            'total_photos': len(data['photos']),
            'total_messages': data['total_messages'],
            'active_months': len(data['active_months']),
            'summary': summary
        })
    
    return processed_years

def generate_year_summary(year, data, photos):
    """Generate a descriptive summary for the year."""
    total_photos = len(data['photos'])
    active_months = len(data['active_months'])
    senders = len(data['senders'])
    
    # Create contextual summary
    if total_photos > 50:
        activity_level = "Very active year"
    elif total_photos > 20:
        activity_level = "Active year"
    else:
        activity_level = "Quieter year"
    
    summary_parts = [
        f"{activity_level} with {total_photos} photos",
        f"across {active_months} months"
    ]
    
    if senders > 1:
        summary_parts.append(f"from {senders} contributors")
    
    return " • ".join(summary_parts)

def process_and_copy_images(photo_messages, zip_file_path, output_dir):
    """Extract and process images, copying them to the output directory."""
    images_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    processed_photos = []
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with tempfile.TemporaryDirectory() as temp_dir:
            for message in photo_messages:
                if 'image_filename' not in message:
                    continue
                
                original_filename = message['image_filename']
                
                try:
                    # Extract to temporary location
                    zip_ref.extract(original_filename, temp_dir)
                    temp_path = os.path.join(temp_dir, original_filename)
                    
                    # Generate new filename based on date and message
                    date_str = message['datetime'].strftime('%Y%m%d') if message['datetime'] else '00000000'
                    sender_initials = ''.join([word[0].upper() for word in message['sender'].split()[:2]])
                    new_filename = f"{date_str}_{sender_initials}_{original_filename}"
                    
                    # Copy to output images directory
                    output_path = os.path.join(images_dir, new_filename)
                    shutil.copy2(temp_path, output_path)
                    
                    # Process message for web display
                    caption = message['full_content']
                    caption = re.sub(r'IMG-\d{8}-WA\d{4}\.jpg \(file attached\)', '', caption).strip()
                    if not caption:
                        caption = "Photo shared"
                    
                    processed_photo = {
                        'path': f'images/{new_filename}',
                        'date': message['datetime'].strftime('%B %d, %Y') if message['datetime'] else 'Unknown date',
                        'sender': message['sender'],
                        'caption': caption[:200] + ('...' if len(caption) > 200 else '')  # Limit caption length
                    }
                    
                    message['processed_photo'] = processed_photo
                    processed_photos.append(processed_photo)
                    
                except Exception as e:
                    print(f"Error processing image {original_filename}: {str(e)}")
                    continue
    
    return processed_photos

def generate_timeline_webpage(timeline_data, output_dir, title="WhatsApp Timeline"):
    """Generate the timeline webpage using Jinja2 template."""
    
    # Read the template
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'timeline.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Prepare template data
    years = [year_data['year'] for year_data in timeline_data]
    
    # Add processed photo data to timeline data
    for year_data in timeline_data:
        year_data['photos'] = [msg['processed_photo'] for msg in year_data['photos'] if 'processed_photo' in msg]
    
    # Render the template
    html_content = template.render(
        title=title,
        subtitle=f"A visual journey through {len(years)} years of shared memories",
        years=years,
        timeline_data=timeline_data,
        generation_date=datetime.now().strftime('%B %d, %Y at %I:%M %p')
    )
    
    # Write to output file
    output_file = os.path.join(output_dir, 'timeline.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate WhatsApp timeline webpage')
    parser.add_argument('--input', '-i', default='../whatsapp_photos_to_word/data/input/WhatsApp Chat.zip',
                       help='Path to WhatsApp chat export zip file')
    parser.add_argument('--output', '-o', default='../data/output',
                       help='Output directory for timeline webpage and images')
    parser.add_argument('--title', '-t', default='Our WhatsApp Timeline',
                       help='Title for the timeline webpage')
    parser.add_argument('--max-photos', type=int, default=6,
                       help='Maximum photos per year (default: 6)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    print(f"Processing WhatsApp export: {args.input}")
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return 1
    
    try:
        # Read chat content from zip
        with zipfile.ZipFile(args.input, 'r') as zip_ref:
            txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
            if not txt_files:
                print("Error: No chat text file found in zip")
                return 1
            
            chat_file = txt_files[0]
            print(f"Reading chat from: {chat_file}")
            chat_content = zip_ref.read(chat_file)
        
        # Parse messages
        print("Parsing chat messages...")
        messages = parse_chat_messages(chat_content)
        print(f"Found {len(messages)} total messages")
        
        # Find photo messages
        photo_messages = find_photo_messages(messages)
        print(f"Found {len(photo_messages)} photo messages")
        
        if not photo_messages:
            print("No photo messages found in chat")
            return 0
        
        # Organize by year
        print("Organizing photos by year...")
        timeline_data = organize_by_year(photo_messages)
        print(f"Found photos from {len(timeline_data)} years")
        
        # Process and copy images
        print("Processing and copying images...")
        all_selected_photos = []
        for year_data in timeline_data:
            all_selected_photos.extend(year_data['photos'])
        
        processed_photos = process_and_copy_images(all_selected_photos, args.input, args.output)
        print(f"Processed {len(processed_photos)} images")
        
        # Generate webpage
        print("Generating timeline webpage...")
        output_file = generate_timeline_webpage(timeline_data, args.output, args.title)
        print(f"Timeline webpage created: {output_file}")
        
        # Print summary
        print(f"\n--- Timeline Summary ---")
        print(f"Years covered: {timeline_data[0]['year']} - {timeline_data[-1]['year']}")
        print(f"Total photos selected: {sum(len(year['photos']) for year in timeline_data)}")
        print(f"Output directory: {args.output}")
        print(f"Open in browser: file://{os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())