import qrcode

def generate(url: str, id: str) -> str:
    img = qrcode.make(url)
    image_path = f"qrs/generated_{id}.png"
    img.save(image_path)
    
    return image_path