from rich.console import Console
from rich import print
import requests as rq
import subprocess as sp
import json
import os 

API_KEY = os.getenv("OPENROUTER_API_KEY") # Use whichever API you wanna USE.
if API_KEY == None:
	print('[red]OPENROUTER_API_KEY Not Found IN ENVIOROMENT!![/]')
	print('[yellow]hint:export OPENROUTER_API_KEY="sk-or-vk-...<your-API-key>"')
	exit()

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
	#if res.
	reply = res['choices'][0]['message']['content']
	return reply 

def main():

	branch = run(["git",'branch','--show-current']).stdout or ''
	print(f'Will you push to branch: [green] {branch} [/]')
	branch_check = input(">> ").strip()
	if branch_check.lower() == 'n' or branch_check.lower() == 'no':
		exit()

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
		try:
			msg = to_ai(prompt)
		except rq.exceptions.ConnectionError as e:
			print(f"[red]{type(e).__name__}[/]:{e}")
			print('[yellow]hint:Chenk Your Network Connection')
			exit()
		except Exception as e:
			print(f"[red]{type(e).__name__}[/]:{e}")
			exit()

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
	try:
		main()
	except KeyboardInterrupt:
		None