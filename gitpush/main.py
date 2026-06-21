from rich.console import Console
import subprocess as sp
import requests as rq
import os 


c = Console()


def run(cmd):
	return sp.run(
		cmd,
		text=True,
		capture_output=True,
		encoding="utf-8",
		errors="replace"
	)


def to_ai(prompt,API_KEY): # The messages that will go to Cloud or local AI
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

def main():
	API_KEY = os.getenv("OPENROUTER_API_KEY") # Use whichever API you wanna USE.
	if not API_KEY:
		c.print('[red]OPENROUTER_API_KEY Not Found IN ENVIROMENT!![/]')
		c.print('[yellow]hint:export OPENROUTER_API_KEY="sk-or-v1-...<your-API-key>"')
		exit()

	if run(['git','rev-parse','--is-inside-work-tree']).returncode != 0:
		c.print('[red]Not Inside Git Repo[/]')
		exit()

	# BRANCH CHECK 
	branch = run(["git",'branch','--show-current']).stdout.strip() or ''
	c.print(f'[#ffd39b]Will you push to branch:[/] [green] {branch} [/]')
	branch_check = input("(y/n)>> ").strip()
	if not branch_check.lower() in ('y','yes'):
		c.print('[yellow]User Aborted[/]')
		c.print('[yellow]hint: use git push -u origin <branch>')
		exit()

	#FILE CHECK
	files = run(['git','status','--short']).stdout or ''
	c.print('[#ffd39b]This Files will be added[/]')
	c.print(files)
	f_check = input("[y/n]>>").strip()
	if not f_check.lower() in ('yes','y'):
		c.print("[yellow]Add in your Own[/]")
		exit()

	# ADD THE FILES
	run(['git','add','.'])

	# THE INFO THAT WILL BE SENT TO CLOUD AI TO FRAME THE MESSAGE 
	stat = run(['git','diff','--cached','--stat']).stdout or ""
	raw_diff  = (run(['git','diff','--cached']).stdout or "")
	if len(raw_diff) >= 4000:
		c.print('[yellow]Diff truncted at 4000 chars [/]')
	diff = raw_diff[:4000]

	# FALLBACK IF NOTHINGS TO COMMIT 
	if not diff.strip():
		c.print("[yellow]No Changes To commit.[/]")
		return 

	# THE PROMPT 
	prompt =  f"""
	Generate ONE conventional commit message.

	Changed files:
	{stat}

	Diff:
	{diff}
	"""


	# THE CLOUD AI PROCESS 
	with c.status("Thinking...",spinner="dots",spinner_style="#AB82FF"):
		try:
			msg = to_ai(prompt,API_KEY)
		except rq.exceptions.ConnectionError as e:
			run(['git','reset'])
			c.print(f"[red]\n{type(e).__name__}[/]:\n{e}")
			c.print('[yellow]hint:Chenk Your Network Connection[/]')
			exit()
		except Exception as e:
			c.print(f"[red]\n{type(e).__name__}[/]:\n{e}")
			run(['git','reset'])
			exit()


	# MESSAGE CONFIRM MATION BEFORE FINAL COMMIT
	c.print(f'\nAI:{msg}')
	c.print('[yellow]\nUse this? [y/n][/]')
	confirm = input(">> ").strip()
	if not confirm.lower() in ('y','yes'):
		msg = ''
		while not msg:
			c.print("[#ffd39b]Enter commit message:[/] ")
			msg = input(">> ").strip()


	# FINAL COMMIT 
	with c.status("",spinner="dots",spinner_style="#AB82FF"):	
		commit = run(['git','commit','-m',msg])
		c.print(commit.stdout)
		c.print(commit.stderr)



	# FINAL PUSH DIRECTLY AFTER COMMIT 
	if commit.returncode == 0:
		with c.status("",spinner="dots",spinner_style="#AB82FF"):
			pull = run(['git','pull','--rebase'])
			c.print(pull.stdout)
			c.print(pull.stderr)
			if pull.returncode == 0:
				push = run(['git','push'])
				c.print(push.stdout)
				c.print(push.stderr)
				if push.returncode == 0:
					c.print("[green]DONE!![/]")
				else:
					c.print("[red]Push Failed!![/]")
			else:
				c.print('[red]Pull Failed [/]')
	else:
		c.print("[red]Commit Failed!![/]")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		c.print('[yellow]\nAborted By User![/]')