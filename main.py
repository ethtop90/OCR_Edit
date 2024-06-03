from PIL import Image, ImageDraw, ImageFont
import pytesseract
import re

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract_executable'

def extract_text_with_boxes(image_path):
    # Open the image file
    image = Image.open(image_path)
    
    # Perform OCR on the image
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    return data

def replace_text(image_path, old_text, new_text, output_path):
    # Extract text and bounding boxes
    data = extract_text_with_boxes(image_path)
    
    # Open the image for editing
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # You can specify your font here
    
    # Iterate over each text instance
    for i in range(len(data['text'])):
        if re.search(old_text, data['text'][i], re.IGNORECASE):
            x, y, w, h = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            
            # Cover the old text with a white rectangle
            draw.rectangle((x, y, x + w, y + h), fill='white')
            
            # Draw the new text
            draw.text((x, y), new_text, fill='black', font=font)
    
    # Save the edited image
    image.save(output_path)

# Example usage
image_path = 'path_to_your_image.png'
output_path = 'path_to_output_image.png'
replace_text(image_path, 'Sotergram', 'CAREogram', output_path)
