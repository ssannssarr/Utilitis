from rich.console import Console
from rich import print
import requests as rq
import subprocess as sp
import sys
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

	# BRANCH CHECK 
	branch = run(["git",'branch','--show-current']).stdout or ''
	print(f'[#ffd39b]Will you push to branch:[/] [green] {branch} [/]')
	branch_check = input(">> ").strip()
	if not branch_check.lower() in ('y','yes'):
		print('[yellow]User Aborted[/]')
		print('[yellow]hint: use git push -u origin <branch>')
		exit()

	#FILE CHECK
	files = run(['git','status','--short']).stdout or ''
	print('[#ffd39b]This Files will be added[/]')
	print(files)
	f_check = input("[y/n]>>").strip()
	
	if not f_check.lower() in ('yes','y'):
		print("[yellow]Add in your Own[yellow]")
		exit()


	run(['git','add','.'])

	stat = run(['git','diff','--cached','--stat']).stdout or ""
	diff  = run(['git','diff','--cached']).stdout or ""

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
			run(['git','reset','HEAD'])
			print(f"[red]\n{type(e).__name__}[/]:\n{e}")
			print('[yellow]hint:Chenk Your Network Connection[/]')
			exit()
		except Exception as e:
			print(f"[red]\n{type(e).__name__}[/]:\n{e}")
			exit()

	print(f'\nAI:{msg}')

	print('[yellow]\nUse this? [y/n][/]')
	confirm = input(">> ")
	if confirm.lower() == 'n' or confirm.lower() == 'no':
		msg = input("[#ffd39b]Enter commit message:[/] ")

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