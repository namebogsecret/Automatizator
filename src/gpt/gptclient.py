from requests import post
class GPTClient:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    def complete_text(self, prompt, temperature=0.7, max_tokens=4000, timeout=240):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=timeout)
        
        return response.json()