import asyncio
import urllib.parse
from typing import Optional, Tuple

import yt_dlp

from app.models import EducationTopic, MediaCategory, MediaPlatform

TOPIC_KEYWORDS = {
    'ai_ml': ['machine learning', 'deep learning', 'neural network', 'artificial intelligence', 'ai ', 'gpt', 'llm', 'transformer', 'nlp', 'computer vision', 'reinforcement learning', 'tensorflow', 'pytorch'],
    'computer_science': ['algorithm', 'data structure', 'programming', 'operating system', 'compiler', 'database', 'dsa', 'competitive programming', 'leetcode', 'coding', 'software engineering'],
    'information_science': ['information theory', 'data science', 'big data', 'analytics', 'visualization', 'information retrieval', 'data analysis'],
    'web_dev': ['react', 'javascript', 'frontend', 'backend', 'fullstack', 'full stack', 'css', 'html', 'node.js', 'nodejs', 'django', 'flask', 'api', 'rest api', 'web development', 'next.js', 'vue', 'angular'],
    'mathematics': ['calculus', 'linear algebra', 'statistics', 'probability', 'discrete math', 'number theory', 'mathematics', 'differential equation'],
    'science': ['physics', 'chemistry', 'biology', 'astronomy', 'quantum', 'thermodynamics', 'mechanics', 'organic chemistry'],
}

EDUCATION_SIGNALS = ['tutorial', 'course', 'lecture', 'lesson', 'learn', 'class', 'explained', 'how to', 'guide', 'introduction to', 'beginner', 'advanced', 'masterclass', 'bootcamp', 'university', 'college', 'professor', 'mit ', 'stanford']

KNOWN_EDUCATION_CHANNELS = ['3blue1brown', 'freecodecamp', 'mit opencourseware', 'khan academy', 'computerphile', 'numberphile', 'sentdex', 'corey schafer', 'traversy media', 'the coding train', 'cs dojo', 'tech with tim', 'fireship', 'web dev simplified', 'neetcode', 'abdul bari', 'jenny', 'gate smashers', 'apna college', 'love babbar', 'striver', 'take u forward', 'code with harry', 'telusko']


def detect_platform(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return MediaPlatform.youtube.value
        if 'netflix.com' in domain:
            return MediaPlatform.netflix.value
        if 'primevideo.com' in domain or 'amazon.com' in domain:
            return MediaPlatform.prime_video.value
        if 'disneyplus.com' in domain:
            return MediaPlatform.disney_plus.value
        if 'hotstar.com' in domain:
            return MediaPlatform.hotstar.value
        if 'instagram.com' in domain:
            return MediaPlatform.instagram.value
        return MediaPlatform.other.value
    except Exception:
        return MediaPlatform.other.value


def classify_content(title: str, description: str, tags: list[str], channel: str, yt_category: str, duration: int) -> Tuple[str, Optional[str], float]:
    title_lower = (title or "").lower()
    desc_lower = (description or "").lower()
    channel_lower = (channel or "").lower()
    tags_lower = [t.lower() for t in tags] if tags else []
    
    text_corpus = f"{title_lower} {desc_lower} {' '.join(tags_lower)}"
    
    confidence = 0.5
    category = None
    
    # YouTube category matching
    yt_cat_lower = (yt_category or "").lower()
    if yt_cat_lower in ['education', 'howto & style', 'science & technology']:
        category = MediaCategory.education.value
        confidence += 0.2
    elif yt_cat_lower in ['film & animation', 'shows']:
        category = MediaCategory.movie.value
        confidence += 0.2
    elif yt_cat_lower in ['music', 'gaming', 'entertainment', 'comedy', 'people & blogs', 'sports', 'pets & animals']:
        category = MediaCategory.entertainment.value
        confidence += 0.2
    elif yt_cat_lower == 'news & politics':
        category = MediaCategory.article.value
        confidence += 0.2
    
    # Channel check
    if channel_lower in KNOWN_EDUCATION_CHANNELS:
        category = MediaCategory.education.value
        confidence += 0.1
        
    # Edu signals check
    edu_signal_count = sum(1 for s in EDUCATION_SIGNALS if s in text_corpus)
    if edu_signal_count > 0:
        if not category:
            category = MediaCategory.education.value
        confidence += min(0.3, edu_signal_count * 0.1)
        
    if duration and duration > 2700: # 45 min
        if category == MediaCategory.education.value:
            confidence += 0.1
    elif duration and duration < 60:
        if not category:
            category = MediaCategory.entertainment.value

    # If still no category, check keywords for education topic
    edu_topic = None
    best_topic_score = 0
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_corpus)
        if score > best_topic_score:
            best_topic_score = score
            edu_topic = topic
            
    if best_topic_score > 0:
        if not category or category == MediaCategory.other.value:
            category = MediaCategory.education.value
        confidence += min(0.3, best_topic_score * 0.15)
        
    if not category:
        category = MediaCategory.other.value
        
    if category != MediaCategory.education.value:
        edu_topic = None

    confidence = min(1.0, confidence)
    return category, edu_topic, confidence


def extract_yt_info(url: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'no_download': True,
        'extract_flat': False,
        'skip_download': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


async def analyze_url(url: str) -> dict:
    platform = detect_platform(url)
    
    result = {
        "title": None,
        "channel": None,
        "description": None,
        "thumbnail": None,
        "duration": None,
        "platform": platform,
        "category": MediaCategory.other.value,
        "education_topic": None,
        "tags": [],
        "confidence": 0.5
    }

    if platform in [MediaPlatform.netflix.value, MediaPlatform.prime_video.value, MediaPlatform.disney_plus.value, MediaPlatform.hotstar.value]:
        result["category"] = MediaCategory.movie.value
        result["confidence"] = 0.9
        return result
        
    if platform == MediaPlatform.instagram.value:
        result["category"] = MediaCategory.entertainment.value
        result["confidence"] = 0.9
        return result
        
    if 'goodreads.com' in url.lower() or '/dp/' in url.lower():
        result["category"] = MediaCategory.book.value
        result["confidence"] = 0.9
        return result

    if platform == MediaPlatform.youtube.value:
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, extract_yt_info, url)
            
            result["title"] = info.get('title')
            result["channel"] = info.get('uploader')
            desc = info.get('description')
            result["description"] = desc[:500] if desc else None
            result["thumbnail"] = info.get('thumbnail')
            result["duration"] = info.get('duration')
            result["tags"] = info.get('tags', [])
            
            yt_category = info.get('categories', [None])[0]
            
            cat, topic, conf = classify_content(
                result["title"],
                desc,
                result["tags"],
                result["channel"],
                yt_category,
                result["duration"]
            )
            
            result["category"] = cat
            result["education_topic"] = topic
            result["confidence"] = conf
            
        except Exception as e:
            print(f"Error extracting yt info: {e}")
            
    return result
