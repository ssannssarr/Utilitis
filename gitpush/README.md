# GITPUSH 

As the name it automate the git push flow.

## Why this ?

When do work on some project and commit repeatedly the commit messages became meaningless (T_T) and that time nothing comes to my mind so I made this workflow.

## How to use?

Clone the repo:
```bash
git clone https://github.com/ssannssarr/Utilitis
cd 
```



## What it has?

It has three part:

1. run()
```python
def run(cmd):
	return sp.run(
		cmd,
		text=True,
		capture_output=True,
		encoding="utf-8",
		errors="replace"
	)
```
NOTE: `sp` is aliased form of Module `subprocess`.

This is shortform of `subprocess.run()` with all `capture_output`,etc into all in one. So it becames easy later 

2. to_ai()
```python
def to_ai(prompt,API_KEY): 
	url = "https://openrouter.ai/api/v1/chat/completions"

	headers={
		"Authorization": f"Bearer {API_KEY}",
		"Content-Type": "application/json",
	}

	data = {
		"model":"openrouter/free",
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
	res = res.json()
	reply = res['choices'][0]['message']['content']
	return reply 
```
NOTE: `rq` is aliased form of Module `requests`


The API calling part using requests library from Openrouter(You change that as your provider) 