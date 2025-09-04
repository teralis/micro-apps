#!/usr/bin/env python3
"""
Marketing Timeline Generator
Transforms WhatsApp timeline data into compelling marketing content
using AI-powered content generation and SMC Marine styling
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
import json

# Import the base timeline generator functions
from whatsapp_timeline_generator import (
    parse_message_date, parse_chat_messages, find_photo_messages, 
    organize_by_year, process_and_copy_images
)

class MarketingContentGenerator:
    """AI-powered content generator for creating marketing copy from timeline data"""
    
    def __init__(self):
        self.marine_terms = [
            "Marine Engineering", "Coastal Infrastructure", "Maritime Construction",
            "Port Development", "Marine Structures", "Waterfront Projects", 
            "Offshore Engineering", "Harbor Works", "Marine Installation",
            "Underwater Construction", "Marine Logistics", "Coastal Protection"
        ]
        
        self.achievement_types = [
            "Project Milestone", "Technical Innovation", "Safety Achievement",
            "Environmental Initiative", "Quality Excellence", "Team Excellence",
            "Client Satisfaction", "Operational Efficiency", "Sustainability Goal"
        ]
        
        self.impact_phrases = [
            "enhancing marine infrastructure capabilities",
            "delivering sustainable coastal solutions", 
            "advancing maritime engineering standards",
            "strengthening Australian marine industry",
            "improving waterfront accessibility",
            "supporting local maritime communities",
            "creating lasting environmental benefits",
            "establishing new industry benchmarks"
        ]

    def generate_project_title(self, original_message, sender, date):
        """Generate a professional project title from message content"""
        # Extract meaningful keywords from message
        message = re.sub(r'<attached:.*?>', '', original_message).strip()
        
        # Common project types based on typical construction/marine work
        project_types = [
            "Infrastructure Development", "Marine Installation", "Construction Milestone",
            "Engineering Achievement", "Project Delivery", "Technical Implementation",
            "Site Development", "Marine Works", "Construction Progress"
        ]
        
        # Pick a project type and create title
        project_type = random.choice(project_types)
        
        # Create location/context if sender initials suggest it
        if len(message) > 20:
            # Try to extract meaningful words
            words = re.findall(r'\b[A-Z][a-z]{3,}\b', message)
            if words and len(words[0]) > 3:
                context = words[0]
                return f"{context} {project_type}"
        
        return f"{date.strftime('%B %Y')} {project_type}"

    def generate_project_description(self, original_message, title):
        """Transform basic message into professional project description"""
        # Clean the original message
        message = re.sub(r'<attached:.*?>', '', original_message).strip()
        
        if not message or len(message) < 10:
            # Generate based on title
            descriptions = [
                f"Successful completion of {title.lower()} demonstrating our commitment to marine engineering excellence and sustainable construction practices.",
                f"Strategic implementation of {title.lower()} showcasing advanced technical capabilities and innovative approaches to maritime infrastructure development.",
                f"Professional delivery of {title.lower()} highlighting our expertise in complex marine construction projects and dedication to quality outcomes.",
                f"Expert execution of {title.lower()} reflecting our industry-leading capabilities in marine engineering and infrastructure development."
            ]
            return random.choice(descriptions)
        
        # Enhance the existing message
        enhanced_starts = [
            "Professional execution of", "Strategic implementation of", "Successful delivery of",
            "Expert completion of", "Innovative approach to", "Advanced technical work on"
        ]
        
        enhanced_ends = [
            "demonstrating our marine engineering excellence.",
            "showcasing advanced technical capabilities and sustainable practices.",
            "highlighting our commitment to quality and environmental stewardship.",
            "reflecting industry-leading expertise in maritime infrastructure.",
            "establishing new benchmarks for Australian marine construction."
        ]
        
        return f"{random.choice(enhanced_starts)} {message.lower()} {random.choice(enhanced_ends)}"

    def generate_impact_statement(self, project_description, year):
        """Generate impact statement for the project"""
        impacts = [
            f"Advanced marine infrastructure capabilities, contributing to Australia's coastal development goals and environmental sustainability targets for {year}.",
            f"Strengthened maritime engineering standards while supporting local economic growth and creating lasting value for coastal communities.",
            f"Enhanced operational efficiency and safety protocols, establishing new industry benchmarks for sustainable marine construction practices.",
            f"Delivered measurable environmental benefits through innovative engineering approaches and commitment to ecological preservation.",
            f"Contributed to regional marine infrastructure resilience while maintaining highest standards of quality and environmental stewardship."
        ]
        
        return random.choice(impacts)

    def generate_achievements(self, year_data, year):
        """Generate achievement badges for the year"""
        num_photos = len(year_data['photos']) if hasattr(year_data, 'photos') and year_data['photos'] else year_data.get('total_photos', 0)
        active_months = year_data.get('active_months', 0)
        if isinstance(active_months, set):
            active_months = len(active_months)
        elif isinstance(active_months, int):
            pass  # already correct
        else:
            active_months = 0
            
        num_achievements = min(6, max(3, num_photos // 2))
        
        base_achievements = [
            f"{num_photos} Projects Delivered",
            f"{active_months} Months Active",
            "Safety Excellence",
            "Quality Assurance",
            "Environmental Compliance",
            "Technical Innovation",
            "Client Satisfaction",
            "Team Excellence",
            "Operational Efficiency",
            "Sustainable Practices"
        ]
        
        # Add year-specific achievements
        if year >= 2020:
            base_achievements.extend(["COVID-Safe Operations", "Adaptive Solutions"])
        if year >= 2022:
            base_achievements.extend(["Digital Innovation", "Advanced Technology"])
        
        return random.sample(base_achievements, num_achievements)

    def generate_capabilities(self, themes, year):
        """Generate capability tags from themes and year context"""
        # Combine extracted themes with marine-specific capabilities
        capabilities = list(set(themes[:4] + random.sample(self.marine_terms, min(4, len(self.marine_terms)))))
        
        # Add year-specific capabilities
        if year >= 2020:
            capabilities.append("Remote Operations")
        if year >= 2021:
            capabilities.append("Sustainable Engineering")
        if year >= 2023:
            capabilities.append("Digital Integration")
            
        return capabilities[:8]  # Limit to 8 capabilities

    def generate_year_summary(self, year, year_data):
        """Generate marketing-focused year summary"""
        total_projects = len(year_data['photos']) if hasattr(year_data, 'photos') and year_data['photos'] else year_data.get('total_photos', 0)
        active_months = year_data.get('active_months', 0)
        if isinstance(active_months, set):
            active_months = len(active_months)
        elif isinstance(active_months, int):
            pass  # already correct
        else:
            active_months = 0
        
        if total_projects > 40:
            intensity = "exceptional productivity"
        elif total_projects > 20:
            intensity = "strong project momentum"
        else:
            intensity = "focused strategic initiatives"
        
        summaries = [
            f"A year of {intensity} delivering {total_projects} major projects across {active_months} months, reinforcing our position as Australia's premier marine engineering specialists.",
            f"Demonstrated marine engineering excellence through {total_projects} successful project completions, showcasing innovative solutions and sustainable practices across {active_months} active months.",
            f"Strategic growth and technical advancement with {total_projects} projects delivered over {active_months} months, establishing new benchmarks for Australian maritime infrastructure development.",
            f"Exceptional performance delivering {total_projects} complex marine engineering projects, demonstrating our commitment to quality, safety, and environmental stewardship throughout {active_months} months of operations."
        ]
        
        return random.choice(summaries)

def transform_timeline_to_marketing(timeline_data):
    """Transform basic timeline data into marketing content"""
    content_gen = MarketingContentGenerator()
    
    marketing_timeline = []
    
    for year_data in timeline_data:
        year = year_data['year']
        
        # Transform projects
        marketing_projects = []
        for i, photo in enumerate(year_data['photos']):
            if 'processed_photo' not in photo:
                continue
                
            project = {
                'image': photo['processed_photo']['path'],
                'date': photo['processed_photo']['date'],
                'leader': photo['processed_photo']['sender'],
                'title': content_gen.generate_project_title(
                    photo['full_content'], photo['sender'], photo['datetime']
                ),
                'description': content_gen.generate_project_description(
                    photo['full_content'], 
                    content_gen.generate_project_title(photo['full_content'], photo['sender'], photo['datetime'])
                ),
                'impact': content_gen.generate_impact_statement(
                    photo['full_content'], year
                )
            }
            marketing_projects.append(project)
        
        # Generate marketing content
        marketing_year = {
            'year': year,
            'marketing_summary': content_gen.generate_year_summary(year, year_data),
            'achievements': content_gen.generate_achievements(year_data, year),
            'projects': marketing_projects,
            'capabilities': content_gen.generate_capabilities(year_data['themes'], year),
            'total_projects': len(marketing_projects),
            'total_milestones': len(marketing_projects) * 2,  # Assume 2 milestones per project
            'team_growth': f"{len(year_data.get('senders', set()))}+" if len(year_data.get('senders', set())) > 1 else "Stable"
        }
        
        marketing_timeline.append(marketing_year)
    
    return marketing_timeline

def generate_marketing_timeline(timeline_data, output_dir, company_name="SMC Marine", title="Project Timeline"):
    """Generate the marketing timeline webpage"""
    
    # Read the marketing template
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'marketing_timeline.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Transform data to marketing content
    marketing_data = transform_timeline_to_marketing(timeline_data)
    
    # Prepare template data
    years = [year_data['year'] for year_data in marketing_data]
    years_experience = max(years) - min(years) if years else 5
    
    # Render the template
    html_content = template.render(
        company_name=company_name,
        title=title,
        tagline="Marine Engineering Excellence Since 2019",
        cta_text="Results That Matter • 100% Australian • Sustainable Solutions",
        years=years,
        timeline_data=marketing_data,
        years_experience=years_experience,
        generation_date=datetime.now().strftime('%B %d, %Y')
    )
    
    # Write to output file
    output_file = os.path.join(output_dir, 'marketing_timeline.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate marketing timeline webpage')
    parser.add_argument('--input', '-i', default='../data/input/WhatsApp Chat.zip',
                       help='Path to WhatsApp chat export zip file')
    parser.add_argument('--output', '-o', default='../data/output',
                       help='Output directory for timeline webpage and images')
    parser.add_argument('--company', '-c', default='SMC Marine',
                       help='Company name for branding')
    parser.add_argument('--title', '-t', default='Engineering Excellence Timeline',
                       help='Title for the timeline webpage')
    parser.add_argument('--max-photos', type=int, default=6,
                       help='Maximum photos per year (default: 6)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    print(f"Processing WhatsApp export for marketing timeline: {args.input}")
    
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
        
        # Generate marketing webpage
        print("Generating marketing timeline webpage...")
        output_file = generate_marketing_timeline(timeline_data, args.output, args.company, args.title)
        print(f"Marketing timeline created: {output_file}")
        
        # Print summary
        print(f"\n--- Marketing Timeline Summary ---")
        print(f"Company: {args.company}")
        print(f"Years covered: {timeline_data[0]['year']} - {timeline_data[-1]['year']}")
        print(f"Projects featured: {sum(len(year['photos']) for year in timeline_data)}")
        print(f"Output directory: {args.output}")
        print(f"Open in browser: file://{os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())