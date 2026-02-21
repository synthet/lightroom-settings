import httpx
import sys
import argparse
from pathlib import Path

def test_api(image_path: str, xmp_path: str = None, as_xmp: bool = False):
    img = Path(image_path)
    if not img.exists():
        print(f"Error: {img} not found.")
        sys.exit(1)
        
    url = "http://127.0.0.1:8000/analyze"
    
    files = {
        "image": (img.name, open(img, "rb"), "image/jpeg" if img.suffix.lower() in [".jpg", ".jpeg"] else "image/png")
    }
    
    if xmp_path and Path(xmp_path).exists():
        files["xmp"] = (Path(xmp_path).name, open(xmp_path, "rb"), "application/rdf+xml")
        
    headers = {}
    if as_xmp:
        headers["Accept"] = "application/rdf+xml"
        
    print(f"Sending request to {url}...")
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(url, files=files, headers=headers)
            
        resp.raise_for_status()
        
        if as_xmp:
            print("Received XMP response:")
            print(resp.text)
        else:
            print("Received JSON settings:")
            print(resp.json())
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Lightroom AI API")
    parser.add_argument("image", help="Path to test image")
    parser.add_argument("--xmp", help="Optional path to contextual XMP")
    parser.add_argument("--as-xmp", action="store_true", help="Request XMP output instead of JSON")
    
    args = parser.parse_args()
    test_api(args.image, args.xmp, args.as_xmp)
