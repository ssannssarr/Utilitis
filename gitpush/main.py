from rich.console import Console
import requests as rq
import subprocess as sp
import json
import os 

API_KEY = os.getenv("OPENROUTER_API_KEY") # Use whichever API you wanna USE.
c = Console()

def run(cmd):
	return sp.run(
		cmd,
		text=True,
		capture_output=True,
		encoding="utf-8",
		errors="replace"
	)


def to_ai(prompt): # The messages that will go to Cloude or local AI
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
				"content":"You are a git commit assistant. Reply in English only. Return ONE short conventinal commit message only."
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
		json=data
	)
	res = res.json()
	reply = res['choices'][0]['message']['content']
	return reply 

def main():
	run(['git','add','.'])

	stat = run(['git','diff','--cached','--stat']).stdout or ""
	diff  = (run(['git','diff','--cached']).stdout or "")[:4000]

	if not diff.strip():
		print("[yellow]No Changes To commit.[/]")
		return 

	prompt =  f"""
	Generate ONE conventional commit message.

	Changed files:
	{stat}

	Diff:
	{diff}
	"""

	with c.status("Thinking...",spinner="dots",spinner_style="#AB82FF"):
		msg = to_ai(prompt)

	print(f'\nAI:{msg}')

	confirm = input('\nUse this? [y/n]')
	if confirm.lower() == 'n' or confirm.lower() == 'no':
		msg = input("Enter commit message: ")

	with c.status("",spinner="dots",spinner_style="#AB82FF"):	
		commit = run(['git','commit','-m',msg])
		print(commit.stdout)
		print(commit.stderr)

	if commit.returncode == 0:
		with c.status("",spinner="dots",spinner_style="#AB82FF"):
			push = run(['git','push'])
			print(push.stdout)
			print(push.stderr)
			print("[green]DONE!![/]")
	else:
		print("[red]Commit Failed!![/]")

if __name__ == '__main__':
	main()