"""
timetable_ai.py — AI-powered timetable extraction using Groq Llama 3.2 Vision.

Accepts an image file path, sends it to Groq Llama 3.2 Vision, and returns
structured timetable data as a list of entries.
"""

import base64
import json
import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")


async def extract_timetable(image_path: str) -> list[dict]:
    """
    Extract timetable entries from an image using Groq Llama 3.2 Vision.
    
    Args:
        image_path: Absolute path to the timetable image file.
    
    Returns:
        List of dicts with keys: day_of_week, subject, start_time, end_time, room
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        raise ValueError("GROQ_API_KEY not set in environment")
    
    client = Groq(api_key=GROQ_API_KEY)
    
    # Read the image file and encode to base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    base64_image = base64.b64encode(image_data).decode("utf-8")
    
    # Determine MIME type from extension
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.webp': 'image/webp',
        '.gif': 'image/gif', '.bmp': 'image/bmp',
    }
    mime_type = mime_map.get(ext, 'image/jpeg')
    image_url = f"data:{mime_type};base64,{base64_image}"
    
    prompt = """Extract the weekly timetable from this image.
Return ONLY a JSON array (no markdown, no code fences) with objects containing:
- "day_of_week": one of "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
- "subject": the subject/class name
- "start_time": in "HH:MM" 24-hour format
- "end_time": in "HH:MM" 24-hour format  
- "room": the room/hall number if visible, otherwise null

Only include actual class/lecture slots. Skip breaks, lunch, and empty slots.
If time is not clearly visible, estimate based on typical class durations (1 hour)."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            temperature=0.1
        )
        text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq Vision API error: {e}")
        return []
    
    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]  # Remove first line
        if text.endswith("```"):
            text = text[:-3].strip()
        elif "```" in text:
            text = text[:text.rfind("```")].strip()
            
    if text.startswith("json"):
        text = text[4:].strip()
    
    try:
        entries = json.loads(text)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {text}")
        return []
    
    # Validate and normalize entries
    valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
    validated = []
    if isinstance(entries, list):
        for entry in entries:
            day = entry.get("day_of_week", "").lower().strip()
            if day not in valid_days:
                continue
            validated.append({
                "day_of_week": day,
                "subject": str(entry.get("subject", "Unknown")).strip(),
                "start_time": str(entry.get("start_time", "09:00")).strip(),
                "end_time": str(entry.get("end_time", "10:00")).strip(),
                "room": entry.get("room"),
            })
    
    return validated
