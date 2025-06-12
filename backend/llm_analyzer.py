import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# sending the data we got in the form of json format to the gemini api
def analyze_titles(query, videos):
    if not videos:
        return None
    titles = [v['title'] for v in videos]
    prompt = f"""
You are an expert at picking the most relevant YouTube video for a user's search query. The query is: '{query}'.
Here are the titles:
"""   # smale prompt
    prompt += '\n'.join([f"{i+1}. {title}" for i, title in enumerate(titles)])
    prompt += "\nReply ONLY with the number of the best video."  # limiting agent
    try:
        response = model.generate_content(prompt)
        idx = int(''.join(filter(str.isdigit, response.text.strip()))) - 1
        return videos[idx] if 0 <= idx < len(videos) else videos[0]
    except Exception:
        return videos[0]
