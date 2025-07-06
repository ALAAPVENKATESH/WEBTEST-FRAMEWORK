import requests
import re

def test_security_elements(url):
    try:
        # Check if HTTPS is used
        is_https = url.startswith('https://')
        
        # Get response headers
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        
        # Check security headers
        security_headers = {
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', ''),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', ''),
            'X-Frame-Options': headers.get('X-Frame-Options', ''),
            'X-XSS-Protection': headers.get('X-XSS-Protection', ''),
            'Content-Security-Policy': headers.get('Content-Security-Policy', ''),
            'Referrer-Policy': headers.get('Referrer-Policy', ''),
        }
        
        # Calculate security score
        https_score = 1 if is_https else 0
        hsts_score = 1 if security_headers['Strict-Transport-Security'] else 0
        content_type_score = 1 if security_headers['X-Content-Type-Options'] else 0
        frame_options_score = 1 if security_headers['X-Frame-Options'] else 0
        xss_score = 1 if security_headers['X-XSS-Protection'] else 0
        csp_score = 1 if security_headers['Content-Security-Policy'] else 0
        
        total_score = https_score + hsts_score + content_type_score + frame_options_score + xss_score + csp_score
        max_score = 6
        security_grade = get_grade(total_score, max_score)
        
        return {
            "uses_https": is_https,
            "security_headers": security_headers,
            "security_score": total_score,
            "security_grade": security_grade,
            "recommendations": get_security_recommendations(https_score, hsts_score, content_type_score, frame_options_score, xss_score, csp_score)
        }
        
    except requests.exceptions.ConnectionError:
        return {"error": "Website not found or not accessible"}
    except Exception as e:
        return {"error": "Could not analyze security elements"}

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

def get_security_recommendations(https_score, hsts_score, content_type_score, frame_options_score, xss_score, csp_score):
    recommendations = []
    
    if not https_score:
        recommendations.append("Use HTTPS instead of HTTP")
    if not hsts_score:
        recommendations.append("Add HSTS header")
    if not content_type_score:
        recommendations.append("Add X-Content-Type-Options header")
    if not frame_options_score:
        recommendations.append("Add X-Frame-Options header")
    if not xss_score:
        recommendations.append("Add X-XSS-Protection header")
    if not csp_score:
        recommendations.append("Add Content-Security-Policy header")
    
    return recommendations 