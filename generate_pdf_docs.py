import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

def parse_markdown_to_pdf(input_file, output_file, logo_path=None):
    # Initialize Document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    story = []

    # Customize Styles
    styles.add(ParagraphStyle(
        name='Justify',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        spaceAfter=12
    ))
    
    # Bullet Style
    bullet_style = ParagraphStyle(
        name='Bullet',
        parent=styles['Normal'],
        leftIndent=20,
        spaceAfter=6
    )

    # Add Logo if it exists
    if logo_path and os.path.exists(logo_path):
        try:
            # Adjust width and height to preserve aspect ratio
            # Set a fixed width (e.g., 2.5 inches = 180 points)
            target_width = 180
            img = Image(logo_path)
            
            # Calculate aspect ratio
            aspect_ratio = img.imageHeight / float(img.imageWidth)
            target_height = target_width * aspect_ratio
            
            # Update image dimensions
            img.drawWidth = target_width
            img.drawHeight = target_height
            
            img.hAlign = 'LEFT' 
            story.append(img)
            story.append(Spacer(1, 12))
        except Exception as e:
            print(f"Warning: Could not add logo: {e}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    # Regex for bold: **text** -> <b>text</b>
    def format_text(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#c7254e">\1</font>', text) # Inline code
        return text

    for line in lines:
        line = line.strip()
        
        # Skip empty lines, but maybe we want some spacing?
        # The Spacer logic below handles spacing after paragraphs.
        if not line:
            continue

        # Page Break
        if line == '---':
            story.append(PageBreak())
            continue

        # Headings
        if line.startswith('# '):
            text = format_text(line[2:])
            story.append(Paragraph(text, styles['Heading1']))
            story.append(Spacer(1, 14))
        elif line.startswith('## '):
            text = format_text(line[3:])
            story.append(Paragraph(text, styles['Heading2']))
            story.append(Spacer(1, 12))
        elif line.startswith('### '):
            text = format_text(line[4:])
            story.append(Paragraph(text, styles['Heading3']))
            story.append(Spacer(1, 10))
        elif line.startswith('#### '):
            text = format_text(line[5:])
            story.append(Paragraph(text, styles['Heading4']))
            story.append(Spacer(1, 8))
            
        # Lists (Basic support for * and -)
        elif line.startswith('* ') or line.startswith('- '):
            text = format_text(line[2:])
            story.append(Paragraph(f'<bullet>&bullet;</bullet> {text}', bullet_style))
            
        # Numbered Lists (Basic support for 1. 2.)
        elif re.match(r'^\d+\.\s', line):
            text = format_text(re.sub(r'^\d+\.\s', '', line))
            number = line.split('.')[0] + '.'
            # Using a simplified approach for numbered lists in paragraphs
            story.append(Paragraph(f'<b>{number}</b> {text}', bullet_style))

        # Links - Naive handling: [Text](#link) -> Text
        # Reportlab supports <a href="..."> but internal linking is complex. 
        # We will just strip formatting or keep text.
        # Let's keep the text and ignore the link part for print/pdf specifically or format nicely.
        # Actually reportlab supports <link> but user wants a readable doc. 
        # Markdown link: [text](url)
        # Transformation: text (url)
        elif re.search(r'\[(.*?)\]\((.*?)\)', line):
            # Replace [Text](URL) with Text (URL)
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<u>\1</u>', line) # Just underline the text
            text = format_text(line)
            story.append(Paragraph(text, styles['Justify']))

        # Normal Text
        else:
            text = format_text(line)
            story.append(Paragraph(text, styles['Justify']))

    try:
        doc.build(story)
        print(f"Successfully generated {output_file}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    parse_markdown_to_pdf('PROJECT_DOCUMENTATION.md', 'PROJECT_DOCUMENTATION_FINAL.pdf', logo_path='logo_hd.png')
