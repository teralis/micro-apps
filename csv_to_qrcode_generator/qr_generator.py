#!/usr/bin/env python3
"""
QR Code Generator Script
Reads a CSV file with filename and URL columns and generates SVG QR codes
with high error correction for each entry.
"""

import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import qrcode
import qrcode.image.svg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
# import svglib.svglib as svg2rlg  # Not needed - generating QR directly


def generate_qr_codes(csv_file, output_dir="qr_codes"):
    """
    Generate QR codes from CSV file containing filenames and URLs.
    
    Args:
        csv_file (str): Path to CSV file with 'filename' and 'url' columns
        output_dir (str): Directory to save generated QR codes
    
    Returns:
        list: List of tuples (filename, url, short_url) for generated QR codes
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    generated_codes = []
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Check if required columns exist
            if 'filename' not in reader.fieldnames or 'url' not in reader.fieldnames:
                print("Error: CSV file must contain 'filename' and 'url' columns")
                return False
            
            # Check if short_url column exists (optional)
            has_short_url = 'short_url' in reader.fieldnames
            
            for row in reader:
                filename = row['filename'].strip()
                url = row['url'].strip()
                short_url = row.get('short_url', '').strip() if has_short_url else ''
                
                if not filename or not url:
                    print(f"Skipping empty row: filename='{filename}', url='{url}'")
                    continue
                
                # Create QR code with high error correction
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
                    box_size=13,
                    border=1,
                )
                
                qr.add_data(url)
                qr.make(fit=True)
                
                # Create SVG image
                factory = qrcode.image.svg.SvgPathImage
                img = qr.make_image(image_factory=factory)
                
                # Save as SVG file
                output_path = Path(output_dir) / f"{filename}.svg"
                with open(output_path, 'wb') as svg_file:
                    img.save(svg_file)
                
                print(f"Generated QR code: {output_path}")
                generated_codes.append((filename, url, short_url))
        
        return generated_codes
        
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
        return []
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return []


def generate_index_pdf(generated_codes, output_dir, csv_filename):
    """
    Generate an index PDF with all QR codes for verification.
    
    Args:
        generated_codes (list): List of tuples (filename, url, short_url)
        output_dir (str): Directory containing SVG files
        csv_filename (str): Original CSV filename for reference
    """
    if not generated_codes:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf_filename = Path(output_dir) / f"QR_Index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # A4 dimensions in points (72 points per inch)
    width, height = A4
    margin = 50
    qr_size = 100  # Size of QR code in PDF (points)
    cols = 4  # QR codes per row
    rows = 5  # QR codes per page (reduced to accommodate spacing)
    codes_per_page = cols * rows
    
    c = canvas.Canvas(str(pdf_filename), pagesize=A4)
    
    # Calculate spacing
    available_width = width - 2 * margin
    available_height = height - 2 * margin - 50  # Reserve space for title (reduced)
    col_spacing = available_width / cols
    row_spacing = available_height / rows  # Even spacing
    
    for page_num, start_idx in enumerate(range(0, len(generated_codes), codes_per_page)):
        if page_num > 0:
            c.showPage()
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, height - margin, f"QR Code Index - Batch {csv_filename}")
        c.setFont("Helvetica", 10)
        c.drawString(margin, height - margin - 20, f"Generated: {timestamp}")
        c.drawString(margin, height - margin - 35, f"Page {page_num + 1} of {(len(generated_codes) - 1) // codes_per_page + 1}")
        
        # Draw QR codes
        for i, code_data in enumerate(generated_codes[start_idx:start_idx + codes_per_page]):
            filename = code_data[0]
            url = code_data[1]
            short_url = code_data[2] if len(code_data) > 2 else ''
            row = i // cols
            col = i % cols
            
            x = margin + col * col_spacing
            y = height - margin - 70 - row * row_spacing  # Start QR codes ~10mm from header
            
            # Generate QR code directly for PDF (more reliable than SVG conversion)
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=1,  # Will scale manually
                    border=1,
                )
                qr.add_data(url)
                qr.make(fit=True)
                
                # Get QR code matrix
                matrix = qr.modules
                if matrix:
                    # Calculate scaling to fit qr_size
                    matrix_size = len(matrix)
                    box_size = qr_size / matrix_size
                    
                    # Draw QR code as black squares
                    c.setFillColorRGB(0, 0, 0)  # Black
                    for row_idx, row in enumerate(matrix):
                        for col_idx, is_black in enumerate(row):
                            if is_black:
                                box_x = x + col_idx * box_size
                                box_y = y - qr_size + row_idx * box_size
                                c.rect(box_x, box_y, box_size, box_size, fill=1, stroke=0)
                else:
                    # Fallback: draw placeholder
                    c.rect(x, y - qr_size, qr_size, qr_size, fill=0, stroke=1)
                    c.setFont("Helvetica", 8)
                    c.drawString(x + 5, y - qr_size/2, "QR Error")
            except Exception as e:
                # Fallback: draw placeholder
                c.rect(x, y - qr_size, qr_size, qr_size, fill=0, stroke=1)
                c.setFont("Helvetica", 8)
                c.drawString(x + 5, y - qr_size/2, f"Error: {str(e)[:20]}")
            
            # Add filename and URL below QR code
            c.setFont("Helvetica", 8)
            c.drawString(x, y - qr_size - 15, f"File: {filename}")
            
            # Add short URL as clickable link if available
            if short_url:
                c.setFillColorRGB(0, 0, 1)  # Blue color for links
                c.linkURL(short_url, (x, y - qr_size - 25, x + 120, y - qr_size - 15))
                c.drawString(x, y - qr_size - 25, f"Link: {short_url}")
                c.setFillColorRGB(0, 0, 0)  # Reset to black
            else:
                # Fallback to showing original URL if no short URL
                display_url = url if len(url) <= 30 else url[:27] + "..."
                c.drawString(x, y - qr_size - 25, f"URL: {display_url}")
    
    c.save()
    print(f"Index PDF generated: {pdf_filename}")


def main():
    """Main function to handle command line arguments and run the generator."""
    # Default values
    default_csv = "input.csv"
    default_output_dir = datetime.now().strftime("%y%m%d_%H%M%S") + "_qr_codes"
    
    # Parse arguments
    csv_file = sys.argv[1] if len(sys.argv) > 1 else default_csv
    output_dir = sys.argv[2] if len(sys.argv) > 2 else default_output_dir
    
    # Show usage if no args and default file doesn't exist
    if len(sys.argv) == 1 and not os.path.exists(default_csv):
        print("Usage: python qr_generator.py [csv_file] [output_directory]")
        print("CSV file should have 'filename', 'url', and optionally 'short_url' columns")
        print(f"Defaults: csv_file='{default_csv}', output_dir='{default_output_dir}'")
        sys.exit(1)
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist")
        sys.exit(1)
    
    generated_codes = generate_qr_codes(csv_file, output_dir)
    
    if generated_codes:
        print(f"QR code generation completed. Files saved to '{output_dir}' directory.")
        
        # Generate index PDF
        csv_basename = Path(csv_file).stem
        generate_index_pdf(generated_codes, output_dir, csv_basename)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()