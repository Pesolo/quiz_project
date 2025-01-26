from PIL import Image, ImageDraw, ImageFont
import qrcode
import io

def generate_certificate_image(user, certificate):
    img = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(img)
    
    # Load font
    try:
        font = ImageFont.truetype('app/static/font/Lato-Bold.ttf', 36)
    except:
        font = ImageFont.load_default()
    
    # Draw certificate content
# Calculate center of the image
    image_width, image_height = img.size

    # Define text content
    texts = [
        "Certificate of Achievement In Resource Conservation",
        f"Awarded to: {user.username}",
        f"Level: {certificate.level}",
        f"Date: {certificate.date_earned.strftime('%Y-%m-%d')}"
    ]

    # Define starting y-coordinate and line spacing
    start_y = 100
    line_spacing = 50  # Space between lines

    # Draw each line of text, center-aligned
    for i, text in enumerate(texts):
        text_width, text_height = draw.textsize(text, font=font)
        x = (image_width - text_width) / 2  # Center horizontally
        y = start_y + i * line_spacing  # Space lines vertically
        draw.text((x, y), text, font=font, fill='black')

    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Certificate ID: {certificate.id}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_x = image_width - qr_img.width - 20  # 20px margin
    qr_y = image_height - qr_img.height - 20
    img.paste(qr_img, (qr_x, qr_y))


    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr