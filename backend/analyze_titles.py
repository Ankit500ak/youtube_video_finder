import re
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_titles(query, videos):
    """
    Analyze video titles and metadata to find the best video for the given query.
    
    Scoring criteria:
    1. Title relevance (keywords matching)
    2. Recent publication
    3. Duration (4-20 minutes preferred)
    4. Description relevance
    5. Thumbnail availability
    """
    
    if not videos:
        return None
    
    # Clean and normalize query
    query_words = set(word.lower() for word in re.findall(r'\w+', query) if len(word) > 2)
    
    # Calculate scores for each video
    scored_videos = []
    now = datetime.utcnow()
    
    for video in videos:
        score = 0
        
        # 1. Title relevance (40 points max)
        title = video.get('title', '').lower()
        title_words = set(word for word in re.findall(r'\w+', title) if len(word) > 2)
        title_match = len(query_words & title_words)
        score += min(title_match * 5, 40)  # Max 40 points for title match
        
        # 2. Recent publication (30 points max)
        publishedAt = video.get('publishedAt')
        if publishedAt:
            try:
                pub_date = datetime.fromisoformat(publishedAt.replace('Z', '+00:00'))
                age_days = (now - pub_date).days
                if age_days <= 7:  # Very recent
                    score += 30
                elif age_days <= 30:  # Recent
                    score += 20
                elif age_days <= 90:  # Somewhat recent
                    score += 10
            except Exception:
                pass
        # added a pointing system to get the score
        # 3. Duration (20 points max)
        duration = video.get('duration')
        if duration is not None:
            if 240 <= duration <= 1500:  # 4-25 minutes
                score += 20
            elif 120 <= duration <= 240:  # 2-4 minutes
                score += 15
            elif 1500 <= duration <= 1800:  # 25-30 minutes
                score += 10
            else:
                score += 5  # Small bonus for videos outside preferred range
                
        # Add priority score from search results
        priority = video.get('priority', 0)
        score += priority * 10  # Convert priority to points (0-30 points max)
        
        # 4. Description relevance (10 points max)
        description = video.get('snippet', '').lower()
        desc_words = set(word for word in re.findall(r'\w+', description) if len(word) > 2)
        desc_match = len(query_words & desc_words)
        score += min(desc_match * 2, 10)  # Max 10 points for description match
        
        # 5. Thumbnail availability (5 points)
        if video.get('thumbnail'):
            score += 5
        
        scored_videos.append({
            'video': video,
            'score': score
        })
    
    # Sort by score and return the highest scoring video
    # First sort by priority (from search results), then by score
    scored_videos.sort(key=lambda x: (x['video'].get('priority', 0), x['score']), reverse=True)
    
    if scored_videos:
        best_video = scored_videos[0]['video']
        best_video['score'] = scored_videos[0]['score']
        return best_video
    
    return None
