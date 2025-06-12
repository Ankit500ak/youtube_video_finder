import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import YouTube search and analysis functions
from youtube_search import search_youtube_videos
from analyze_titles import analyze_titles

app = Flask(__name__)
CORS(app)

# Configure Gemini API
try:
    from google.generativeai import get_model
    model = get_model('gemini-pro')
    logger.info("Successfully configured Gemini API")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    model = None

@app.route('/api/search', methods=['POST'])
def search():
    try:
        logger.info("Received search request")
        
        # Get request data
        try:
            data = request.get_json()
            if not data:
                logger.error("No JSON data in request")
                return jsonify({
                    'error': 'Invalid request - no JSON data',
                    'status': 'error'
                }), 400
                
            query = data.get('query')
            if not query:
                logger.error("No query in request")
                return jsonify({
                    'error': 'Query is required',
                    'status': 'error'
                }), 400
                
            logger.info(f"Searching YouTube with query: {query}")
            
            # Search YouTube
            try:
                videos = search_youtube_videos(query)
                if isinstance(videos, list) and videos and 'error' in videos[0]:
                    logger.error(f"YouTube search error: {videos[0]['error']}")
                    return jsonify({
                        'error': videos[0]['error'],
                        'status': 'error'
                    }), 400
                    
                if not videos:
                    logger.warning("No videos found")
                    return jsonify({
                        'error': 'No videos found for the given query',
                        'status': 'warning'
                    }), 200
                    
                logger.info(f"Found {len(videos)} videos")
                
                # Analyze videos
                try:
                    best_video = analyze_titles(query, videos)
                    return jsonify({
                        'best_video': best_video,
                        'videos': videos,
                        'status': 'success'
                    })
                except Exception as e:
                    logger.error(f"Error analyzing videos: {str(e)}")
                    return jsonify({
                        'error': f'Error analyzing videos: {str(e)}',
                        'status': 'error'
                    }), 500
                    
            except Exception as e:
                logger.error(f"Error in YouTube search: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'error': f'Error searching YouTube: {str(e)}',
                    'status': 'error'
                }), 500
                
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({
                'error': f'Invalid request: {str(e)}',
                'status': 'error'
            }), 400
            
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        logger.error("Error traceback:")
        import traceback
            
        print(f"Found {len(videos)} videos")
        best_video = analyze_titles(query, videos)
        return jsonify({
            'best_video': best_video,
            'videos': videos,
            'status': 'success'
        })
        
    except Exception as e:
        import traceback
        print(f"Server error: {str(e)}")
        print("Error traceback:")
        traceback.print_exc()
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
