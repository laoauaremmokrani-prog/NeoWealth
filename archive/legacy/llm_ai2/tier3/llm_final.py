import os
import requests
import re
import sys
from tier3.sp500_sectors import SECTORS

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "")
MODEL_NAME = os.environ.get("TOGETHER_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")

def query_together_ai(prompt: str, max_tokens=500, temperature=0.7):
    if not TOGETHER_API_KEY:
        return "neutral"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
        "stop": ["</s>"]
    }

    response = requests.post(
        "https://api.together.xyz/inference",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        try:
            data = response.json()
            # Try different response formats
            if "output" in data and "choices" in data["output"]:
                return data["output"]["choices"][0]["text"].strip()
            elif "choices" in data:
                return data["choices"][0]["text"].strip()
            elif "text" in data:
                return data["text"].strip()
            else:
                # Fallback: return first non-empty text found
                response_text = str(data)
                if len(response_text) > 100:  # If response is very long, it might be HTML
                    return "neutral"  # Default fallback
                return response_text
        except Exception as e:
            # If JSON parsing fails, return default
            return "neutral"
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def analyze_text(text: str, return_sectors=False):
    """
    Analyze geopolitical/sentiment text and return a sentiment score (-1 to 1).
    If return_sectors=True, also return a list of relevant sectors.
    Returns:
        sentiment_score: float (-1=negative, 0=neutral, 1=positive)
        [relevant_sectors: list of str] (if return_sectors)
    """
    prompt = (
        f"Input: {text}\n"
        "Task: Based on the above, predict the likely impact on the market (positive, negative, or neutral). "
        "You must respond in exactly this format:\n"
        "Prediction: <positive/negative/neutral>\n"
        "Explanation: <brief one-sentence explanation of why this sentiment>\n"
        "Do not include any other text or formatting."
    )
    try:
        response = query_together_ai(prompt)
    except Exception:
        response = "neutral"
    pred_match = re.search(r"Prediction:\s*(\w+)", response, re.I)
    prediction = pred_match.group(1).lower() if pred_match else "neutral"
    

    
    # Extract explanation (look for line starting with "Explanation:")
    explanation = ""
    if pred_match:
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.lower().startswith('explanation:'):
                explanation = line[12:].strip()
                break
        # If no explanation found, provide a default based on sentiment
        if not explanation:
            if prediction == "positive":
                explanation = "Market sentiment appears favorable based on the input text."
            elif prediction == "negative":
                explanation = "Market sentiment appears unfavorable based on the input text."
            else:
                explanation = "Market sentiment appears neutral based on the input text."
        
        # Ensure we always have an explanation
        if not explanation:
            explanation = "Analysis based on market sentiment indicators in the provided text."
    
    # Final fallback - if we still don't have an explanation, create one based on the text content
    if not explanation:
        # Create a simple explanation based on the input text
        text_lower = text.lower()
        if any(word in text_lower for word in ['earnings', 'profit', 'growth', 'positive', 'optimism', 'strong']):
            explanation = "Positive market indicators suggest favorable sentiment."
        elif any(word in text_lower for word in ['decline', 'loss', 'negative', 'pessimism', 'weak', 'tension']):
            explanation = "Negative market indicators suggest unfavorable sentiment."
        else:
            explanation = "Mixed market indicators suggest neutral sentiment."
    
    if prediction == "positive":
        sentiment_score = 1.0
    elif prediction == "negative":
        sentiment_score = -1.0
    else:
        sentiment_score = 0.0
    
    if not return_sectors:
        return sentiment_score, explanation
    # Sector extraction (keyword match)
    text_lower = text.lower()
    relevant_sectors = []
    for sector, keywords in SECTORS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            relevant_sectors.append(sector)
    if not relevant_sectors:
        relevant_sectors = ["Technology", "Financials", "Healthcare"]  # fallback
    return sentiment_score, explanation, relevant_sectors 