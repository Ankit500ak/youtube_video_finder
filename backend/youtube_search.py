import os
import requests
from datetime import datetime, timedelta
import re

def search_youtube_videos(query):
    try:
        # Validate input
        if not query:
            return [{'error': 'Search query cannot be empty'}]
            
        # Get API key
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            return [{'error': 'YOUTUBE_API_KEY not found in environment variables'}]
            
        # Make API request
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 20,
            'key': api_key
        }
        
        try:
            resp = requests.get(url, params=params)
            
            # Check response status
            if resp.status_code != 200:
                error_text = f"YouTube API request failed with status code {resp.status_code}: {resp.text}"
                return [{'error': error_text}]
                
            raw_json = resp.json()
            
            # Check for API errors
            if 'error' in raw_json:
                error_text = raw_json['error'].get('message', 'Unknown error from YouTube Data API')
                return [{'error': f"YouTube API Error: {error_text}"}]
                
            # Get video IDs from search results
            items = raw_json.get('items', [])
            if not items:
                return []
                
            video_ids = [item['id']['videoId'] for item in items]
            
            if not video_ids:
                return []
                
            # Make a separate request to get video details
            details_url = 'https://www.googleapis.com/youtube/v3/videos'
            details_params = {
                'part': 'snippet,contentDetails,statistics',
                'id': ','.join(video_ids),
                'key': api_key
            }
            
            try:
                details_resp = requests.get(details_url, params=details_params)
                if details_resp.status_code != 200:
                    error_text = f"YouTube API details request failed with status code {details_resp.status_code}: {details_resp.text}"
                    return [{'error': error_text}]
                    
                details_json = details_resp.json()
                if 'error' in details_json:
                    error_text = details_json['error'].get('message', 'Unknown error from YouTube Data API')
                    return [{'error': f"YouTube API Error: {error_text}"}]
                
                # Initialize videos list
                videos = []
                now = datetime.utcnow()
                
                # Process video details
                for item in details_json.get('items', []):
                    try:
                        # Get basic video info
                        video_id = item['id']
                        snippet = item['snippet']
                        content_details = item.get('contentDetails', {})
                        
                        title = snippet.get('title', '')
                        url = f'https://www.youtube.com/watch?v={video_id}'
                        description = snippet.get('description', '')
                        thumbnail = snippet.get('thumbnails', {}).get('default', {}).get('url', '')
                        channel = snippet.get('channelTitle', '')
                        publishedAt = snippet.get('publishedAt', None)
                        
                        # Get duration from content details
                        duration = None
                        iso_dur = content_details.get('duration')
                        if iso_dur:
                            m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', iso_dur)
                            if m:
                                mins = int(m.group(1)) if m.group(1) else 0
                                secs = int(m.group(2)) if m.group(2) else 0
                                duration = mins * 60 + secs
                        
                        # Create video data
                        video_data = {
                            'title': title,
                            'url': url,
                            'snippet': description,
                            'thumbnail': thumbnail,
                            'channelTitle': channel,
                            'duration': duration,
                            'publishedAt': publishedAt
                        }
                        
                        # Add video with priority score
                        priority = 0
                        
                        # Duration preference (4-25 minutes preferred)
                        if duration is not None:
                            if 240 <= duration <= 1500:  # 4-25 minutes
                                priority += 3  # Highest priority
                            elif 120 <= duration <= 240:  # 2-4 minutes
                                priority += 2  # Medium priority
                            elif 1500 <= duration <= 1800:  # 25-30 minutes
                                priority += 1  # Low priority
                            
                        # Recent videos get bonus
                        if publishedAt:
                            try:
                                pubdate = datetime.fromisoformat(publishedAt.replace('Z','+00:00'))
                                age_days = (now - pubdate).days
                                if age_days <= 7:  # Very recent
                                    priority += 2
                                elif age_days <= 30:  # Recent
                                    priority += 1
                                
                                # Always add recent videos
                                video_data['priority'] = priority
                                videos.append(video_data)
                                
                            except Exception:
                                # If we can't parse date but have other data, still add
                                if priority > 0:
                                    video_data['priority'] = priority
                                    videos.append(video_data)
                        else:
                            # If no publish date but good duration, still add
                            if priority > 1:
                                video_data['priority'] = priority
                                videos.append(video_data)
                    except KeyError:
                        continue
                        
                # Sort videos by priority (highest first)
                videos.sort(key=lambda x: x.get('priority', 0), reverse=True)
                
                # If no videos found with good priority, try to find any videos
                if not videos:
                    # Try to get any videos from the search results
                    for item in details_json.get('items', []):
                        try:
                            video_id = item['id']
                            title = item['snippet'].get('title', '')
                            url = f'https://www.youtube.com/watch?v={video_id}'
                            
                            # Add basic video data
                            videos.append({
                                'title': title,
                                'url': url,
                                'priority': 0  # Lowest priority
                            })
                        except Exception:
                            continue
                    
                    # Sort by title length as a fallback
                    videos.sort(key=lambda x: len(x.get('title', '')), reverse=True)
                
                return videos[:20]
                
            except requests.exceptions.RequestException as e:
                error_text = f"Error making details request: {str(e)}"
                return [{'error': error_text}]
            except ValueError as e:
                error_text = f"Error parsing JSON response: {str(e)}"
                return [{'error': error_text}]
            
        except Exception as e:
            error_text = str(e)
            error_text = ''.join(c for c in error_text if ord(c) < 128)
            return [{'error': f'Error making YouTube API request: {error_text}'}]
            
    except Exception as e:
        error_text = str(e)
        error_text = ''.join(c for c in error_text if ord(c) < 128)
        return [{'error': f'Error in search_youtube_videos: {error_text}'}]
