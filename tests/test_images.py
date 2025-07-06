import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except:
        return False

def test_images(url):
    try:
        if not is_valid_url(url):
            return "Please enter a valid website URL"
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.find_all('img')
        total_images = len(images)
        
        if total_images == 0:
            return {
                "total_images": 0,
                "broken_images": 0,
                "images_without_alt": 0,
                "broken_image_urls": [],
                "image_score": 3.0,
                "image_grade": "A",
                "recommendations": ["No images found on this page."]
            }
        
        broken_images = []
        images_without_alt = []
        
        images_to_check = images[:5]
        
        for img in images_to_check:
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Skip empty src
            if not src:
                continue
            
            # Convert relative URLs to absolute
            if not src.startswith('http'):
                src = urljoin(url, src)
            
            # Skip data URLs
            if src.startswith('data:'):
                continue
            
            if not alt:
                images_without_alt.append(src)
            
            try:
                img_response = requests.head(src, timeout=2)
                if img_response.status_code >= 400:
                    broken_images.append(src)
            except Exception:
                broken_images.append(src)
        
        total_score = 0
        max_score = 3
        
        if len(broken_images) == 0:
            total_score += 1
        alt_score = (total_images - len(images_without_alt)) / total_images
        total_score += alt_score
        if total_images <= 20:
            total_score += 1
        
        image_grade = get_grade(total_score, max_score)
        
        return {
            "total_images": total_images,
            "broken_images": len(broken_images),
            "images_without_alt": len(images_without_alt),
            "broken_image_urls": broken_images[:3],
            "image_score": round(total_score, 2),
            "image_grade": image_grade,
            "recommendations": get_image_recommendations(broken_images, images_without_alt, total_images)
        }
        
    except requests.exceptions.ConnectionError:
        return {"error": "Website not found or not accessible"}
    except Exception as e:
        return {"error": f"Could not analyze images: {str(e)}"}

def get_grade(score, max_score):
    percentage = (score / max_score) * 100
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"

def get_image_recommendations(broken_images, images_without_alt, total_images):
    recommendations = []
    
    if broken_images:
        recommendations.append(f"Fix {len(broken_images)} broken images")
    if images_without_alt:
        recommendations.append(f"Add alt text to {len(images_without_alt)} images")
    if total_images > 20:
        recommendations.append("Consider reducing the number of images")
    
    return recommendations 