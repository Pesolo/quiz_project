from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
import os
from datetime import datetime
from typing import Optional, Union

class CertificateGenerationError(Exception):
    """Custom exception for certificate generation errors"""
    pass

def generate_certificate_image(user, certificate) -> io.BytesIO:
    """
    Generate a certificate image with error handling and validation.
    
    Args:
        user: User object with username attribute
        certificate: Certificate object with id, level, and date_earned attributes
    
    Returns:
        io.BytesIO: Binary stream containing the generated certificate image
    
    Raises:
        CertificateGenerationError: If certificate generation fails
    """
    try:
        # Input validation
        if not hasattr(user, 'username') or not user.username:
            raise ValueError("Invalid user object: missing username")
        if not all(hasattr(certificate, attr) for attr in ['id', 'level', 'date_earned']):
            raise ValueError("Invalid certificate object: missing required attributes")

        # Create a blank image with a slight off-white background for better appearance
        img = Image.new('RGB', (800, 600), '#FAFAFA')
        draw = ImageDraw.Draw(img)
        
        # Font handling with fallback options
        font_paths = [
            'app/static/font/Lato-Bold.ttf'
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, 36)
                    break
                except Exception:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
            print("Warning: Using default font as Lato-Bold.ttf could not be loaded")

        # Format date safely
        try:
            date_str = certificate.date_earned.strftime('%Y-%m-%d')
        except AttributeError:
            date_str = datetime.now().strftime('%Y-%m-%d')
            print("Warning: Using current date as certificate date was invalid")

        # Define text content with proper escaping
        texts = [
            "Certificate of Achievement In Resource Conservation",
            f"Awarded to: {str(user.username)[:50]}",  # Limit username length
            f"Level: {str(certificate.level)[:20]}",  # Limit level length
            f"Date: {date_str}"
        ]

        # Draw text with improved positioning
        image_width, image_height = img.size
        start_y = 100
        line_spacing = 60  # Increased for better readability

        for i, text in enumerate(texts):
            # Get text size using getbbox (more accurate than textbbox)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (image_width - text_width) / 2
            y = start_y + i * line_spacing
            
            # Add subtle shadow effect for main title
            if i == 0:
                draw.text((x+2, y+2), text, font=font, fill='#CCCCCC')
            draw.text((x, y), text, font=font, fill='#000000')

        # Generate QR code with error handling
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=5
            )
            qr.add_data(f"Certificate ID: {certificate.id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Position QR code with proper padding
            qr_x = image_width - qr_img.width - 40
            qr_y = image_height - qr_img.height - 40
            img.paste(qr_img, (qr_x, qr_y))
        except Exception as e:
            print(f"Warning: Failed to generate QR code: {e}")
            # Continue without QR code rather than failing completely

        # Save image to bytes with error handling
        try:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG', optimize=True)
            img_byte_arr.seek(0)
            return img_byte_arr
        except Exception as e:
            raise CertificateGenerationError(f"Failed to save certificate image: {e}")

    except Exception as e:
        raise CertificateGenerationError(f"Certificate generation failed: {e}")