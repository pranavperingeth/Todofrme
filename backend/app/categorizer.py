import asyncio
import json
import os
import httpx
import re
import urllib.parse
from typing import Optional, Tuple

import yt_dlp
from groq import Groq

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


def heuristic_classify(title: str, description: str, tags: list[str], channel: str, yt_category: str, duration: int) -> Tuple[str, Optional[str], float]:
    """Fallback heuristic classification."""
    title_lower = (title or "").lower()
    desc_lower = (description or "").lower()
    channel_lower = (channel or "").lower()
    tags_lower = [t.lower() for t in tags] if tags else []
    
    text_corpus = f"{title_lower} {desc_lower} {' '.join(tags_lower)}"
    
    confidence = 0.5
    category = None
    
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
    
    if channel_lower in KNOWN_EDUCATION_CHANNELS:
        category = MediaCategory.education.value
        confidence += 0.1
        
    edu_signal_count = sum(1 for s in EDUCATION_SIGNALS if s in text_corpus)
    if edu_signal_count > 0:
        if not category:
            category = MediaCategory.education.value
        confidence += min(0.3, edu_signal_count * 0.1)
        
    if duration and duration > 2700:
        if category == MediaCategory.education.value:
            confidence += 0.1
    elif duration and duration < 60:
        if not category:
            category = MediaCategory.entertainment.value

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


async def ai_classify(url: str, title: str, description: str, tags: list[str], channel: str) -> Optional[Tuple[str, Optional[str], float]]:
    """Use Groq AI (Llama 3) to classify the media content."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your-groq-api-key-here":
        return None
        
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Analyze the following media item to categorize it.
    
    URL: {url}
    Title: {title or 'Unknown'}
    Channel/Uploader: {channel or 'Unknown'}
    Description: {description or 'None'}
    Tags: {', '.join(tags) if tags else 'None'}
    
    Instructions:
    1. Determine the category strictly from this list: "movie", "education", "entertainment", "book", "podcast", "article", "other".
    2. If the category is "education", determine the most fitting education_topic from this list: "ai_ml", "computer_science", "information_science", "web_dev", "mathematics", "science", "general". If not education, set to null.
    3. Provide a confidence score between 0.0 and 1.0.
    
    Output exactly as JSON with keys: "category", "education_topic", "confidence". Do not include markdown formatting or code blocks.
    """
    
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.1,
                response_format={"type": "json_object"}
            )
        )
        
        text = response.choices[0].message.content
        data = json.loads(text)
        
        category = data.get("category", MediaCategory.other.value)
        # Ensure category is valid
        if category not in [e.value for e in MediaCategory]:
            category = MediaCategory.other.value
            
        topic = data.get("education_topic")
        if topic not in [e.value for e in EducationTopic]:
            topic = None
            
        confidence = float(data.get("confidence", 0.8))
        
        return category, topic, confidence
    except Exception as e:
        print(f"AI Classification failed: {e}")
        return None


def extract_yt_info(url: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'no_download': True,
        'extract_flat': False,
        'skip_download': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


async def fetch_basic_metadata(url: str) -> dict:
    """Fallback to fetch basic HTML metadata if yt-dlp fails."""
    try:
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = await client.get(url, headers=headers)
            html = response.text
            
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else None
            
            if not title:
                og_title = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
                if og_title: title = og_title.group(1).strip()
                
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
            if not desc_match:
                desc_match = re.search(r'<meta[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE | re.DOTALL)
            
            desc = desc_match.group(1).strip() if desc_match else None
            if not desc:
                og_desc = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
                if og_desc: desc = og_desc.group(1).strip()
                
            return {"title": title, "description": desc}
    except Exception as e:
        print(f"Basic metadata fetch failed: {e}")
        return {"title": None, "description": None}


async def fetch_youtube_oembed(url: str) -> dict:
    """Fallback to YouTube oEmbed API if yt-dlp fails."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(oembed_url)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "title": data.get("title"),
                    "channel": data.get("author_name"),
                    "thumbnail": data.get("thumbnail_url")
                }
    except Exception as e:
        print(f"oEmbed fetch failed: {e}")
    return {}


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

    # Extract metadata using yt-dlp if it's youtube
    # Even for other platforms, we can try yt-dlp to get a generic title
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
    except Exception as e:
        print(f"Error extracting yt info: {e}")
        yt_category = None

    # Fallback if yt-dlp failed to get a title
    if not result["title"]:
        # Try YouTube oEmbed first for YouTube links
        if platform == MediaPlatform.youtube.value:
            oembed_data = await fetch_youtube_oembed(url)
            if oembed_data.get("title"):
                result["title"] = oembed_data["title"]
                result["channel"] = oembed_data.get("channel") or result["channel"]
                result["thumbnail"] = oembed_data.get("thumbnail") or result["thumbnail"]

        # If still no title, try generic HTML scraper
        if not result["title"]:
            basic_meta = await fetch_basic_metadata(url)
            if basic_meta["title"]:
                result["title"] = basic_meta["title"]
            if basic_meta["description"] and not result["description"]:
                result["description"] = basic_meta["description"][:500]

    # Platform overrides for obvious cases
    if platform in [MediaPlatform.netflix.value, MediaPlatform.prime_video.value, MediaPlatform.disney_plus.value, MediaPlatform.hotstar.value]:
        result["category"] = MediaCategory.movie.value
        result["confidence"] = 0.9
        # Still attempt AI classification to see if we can get better metadata/confidence
    elif platform == MediaPlatform.instagram.value:
        result["category"] = MediaCategory.entertainment.value
        result["confidence"] = 0.9
    elif 'goodreads.com' in url.lower() or '/dp/' in url.lower():
        result["category"] = MediaCategory.book.value
        result["confidence"] = 0.9
        
    # Attempt AI Classification first
    ai_result = await ai_classify(
        url=url, 
        title=result["title"], 
        description=result["description"], 
        tags=result["tags"], 
        channel=result["channel"]
    )
    
    if ai_result:
        cat, topic, conf = ai_result
        # Trust AI if confidence is high or we only had default category
        if conf >= 0.7 or result["category"] == MediaCategory.other.value:
            result["category"] = cat
            result["education_topic"] = topic
            result["confidence"] = conf
    else:
        # Fallback to heuristic classification if AI is disabled or fails
        if platform == MediaPlatform.youtube.value:
            cat, topic, conf = heuristic_classify(
                result["title"],
                result["description"],
                result["tags"],
                result["channel"],
                yt_category,
                result["duration"]
            )
            result["category"] = cat
            result["education_topic"] = topic
            result["confidence"] = conf

    return result
