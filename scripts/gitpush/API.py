import requests as rq
import os 


def to_ai(prompt): # The messages that will go to Cloud or local AI

	API_KEY = os.getenv("OPENROUTER_API_KEY")
	if not API_KEY:
		print("ERROR: OPENROUTER_API_KEY Not Found In Enviroment!!")
		print("hint: export OPENROUTER_API_KEY=<Your-API-key-here>")
		print(" echo 'export OPENROUTER_API_KEY=<Your-API-key-here>' >> ~/.bashrc or ~/.zshrc  to make it permanant!! ")


	url = "https://openrouter.ai/api/v1/chat/completions"

	headers={
		"Authorization": f"Bearer {API_KEY}",
		"Content-Type": "application/json",
	}

	data = {
		"model":"openai/gpt-oss-120b:free",
		"messages":[
			{
				"role":"system",
				"content":"You are a git commit assistant. Reply in English only. Return ONE short conventional commit message only."
			},
			{
				"role":"user",
				"content":prompt,
			},
		]
	}

	res = rq.post(
		url=url,
		headers=headers,
		json=data,
		timeout=60
	)
	
	res.raise_for_status()
	res = res.json()
	reply = res['choices'][0]['message']['content']
	return reply 