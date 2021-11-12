def plain(text: str) -> dict:
    return {
        "type": "Plain",
        "text": text
    }


def image(image_id: str = None, url: str = '', path: str = None, base64: str = None):
    return {
        "type": "Image",
        "imageId": image_id,
        "url": url,
        "path": path,
        "base64": base64
    }
