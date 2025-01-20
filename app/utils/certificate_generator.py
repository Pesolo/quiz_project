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
    draw.text((400, 100), "Certificate of Achievement", font=font, fill='black')
    draw.text((400, 200), f"Awarded to: {user.username}", font=font, fill='black')
    draw.text((400, 300), f"Level {certificate.level}", font=font, fill='black')
    draw.text((400, 400), f"Category: {certificate.category}", font=font, fill='black')
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Certificate ID: {certificate.id}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr