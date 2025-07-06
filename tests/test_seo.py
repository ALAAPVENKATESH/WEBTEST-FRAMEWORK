import requests
import re
from bs4 import BeautifulSoup

def test_seo_elements(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Get meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords.get('content', '') if meta_keywords else ""
        
        # Check for Open Graph tags
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        # Check for Twitter Card tags
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        
        # Check for canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        # Check for robots meta
        robots = soup.find('meta', attrs={'name': 'robots'})
        
        # Check for viewport meta (mobile-friendly)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        # Calculate scores
        title_score = 1 if title_text and len(title_text) > 10 and len(title_text) < 60 else 0
        desc_score = 1 if description and len(description) > 50 and len(description) < 160 else 0
        og_score = 1 if og_title or og_desc else 0
        twitter_score = 1 if twitter_card or twitter_title else 0
        canonical_score = 1 if canonical else 0
        viewport_score = 1 if viewport else 0
        
        total_score = title_score + desc_score + og_score + twitter_score + canonical_score + viewport_score
        max_score = 6
        seo_grade = get_grade(total_score, max_score)
        
        return {
            "title": title_text,
            "description": description,
            "keywords": keywords,
            "has_og_tags": bool(og_title or og_desc or og_image),
            "has_twitter_cards": bool(twitter_card or twitter_title),
            "has_canonical": bool(canonical),
            "has_robots": bool(robots),
            "mobile_friendly": bool(viewport),
            "seo_score": total_score,
            "seo_grade": seo_grade,
            "recommendations": get_seo_recommendations(title_score, desc_score, og_score, twitter_score, canonical_score, viewport_score)
        }
        
    except requests.exceptions.ConnectionError:
        return {"error": "Website not found or not accessible"}
    except Exception as e:
        return {"error": "Could not analyze SEO elements"}

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

def get_seo_recommendations(title_score, desc_score, og_score, twitter_score, canonical_score, viewport_score):
    recommendations = []
    
    if not title_score:
        recommendations.append("Add a title tag (10-60 characters)")
    if not desc_score:
        recommendations.append("Add a meta description (50-160 characters)")
    if not og_score:
        recommendations.append("Add Open Graph tags for social media")
    if not twitter_score:
        recommendations.append("Add Twitter Card tags")
    if not canonical_score:
        recommendations.append("Add canonical URL")
    if not viewport_score:
        recommendations.append("Add viewport meta tag for mobile")
    
    return recommendations 