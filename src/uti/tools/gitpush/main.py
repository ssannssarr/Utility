from rich.console import Console
import subprocess as sp
import os
import sys
import requests as rq
api = os.getenv("OPENROUTER_API_KEY")

c = Console()


def run(cmd):
	return sp.run(
		cmd,
		text=True,
		capture_output=True,
		encoding="utf-8",
		errors="replace"
	)

def to_ai(prompt,API_KEY = api): # The messages that will go to Cloud or local AI
    url = "http://localhost:8080/v1/chat/completions"

    headers={
		"Authorization": "ollama",
		"Content-Type": "application/json",
	}

    data = {
		"model":"openrouter/free",
		"messages":[
			{
				"role":"system",
				"content":"""Return exactly one conventional commit message.

Rules:
- Output only the commit message.
- No quotes.
- No markdown.
- No explanation.
- Max 72 characters.
- Format: <type>: <message>

Valid types:
feat
fix
docs
refactor
style
test
chore
perf
ci
build"""
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


def build_prompt(stat, raw_diff):
	note = ""
	if len(raw_diff) > 4000:
		c.print('[yellow]Diff truncated at 4000 chars.[/]')
		note = "\n\nNote: The diff was truncated to the first 4000 characters."

	return f"""
	Generate ONE conventional commit message.

	Changed files:
	{stat}
	{note}

	Diff:
	{raw_diff[:4000]}
	"""


def is_repo():
	if run(['git','rev-parse','--is-inside-work-tree']).returncode != 0:
		c.print('[red]Not Inside Git Repo[/]')
		exit()

def this_branch():
	branch = run(["git",'branch','--show-current']).stdout.strip() or ''
	if not branch:
		c.print('[red]Detached HEAD detected. Please checkout a branch before using gitpush.[/]')
		exit()
	c.print(f'[#ffd39b]Will you push to branch:[/] [green] {branch} [/]')
	branch_check = input("[y/n]>> ").strip()
	if not branch_check.lower() in ('y','yes'):
		c.print('[yellow]User Aborted[/]')
		c.print('[yellow]hint: use git push -u origin <branch>')
		exit()

def this_files():
	files = run(['git','status','--short']).stdout.strip() or ''
	if not files:
		c.print('[yellow]No Changes To commit[/]')
		exit()
	c.print('[#ffd39b]\nThis Files will be added[/]')
	c.print(files)
	f_check = input("[y/n]>>").strip()
	if not f_check.lower() in ('yes','y'):
		c.print("[yellow]Add in your Own[/]")
		exit()


def get_ai_message(prompt):
	with c.status("Thinking...",spinner="dots",spinner_style="#AB82FF"):
		try:
			return to_ai(prompt)
		except Exception as e:
			run(['git','reset'])
			c.print(f"[red]\n{type(e).__name__}[/]:\n{e}")
			exit()

def get_custom_message():
	msg = ''
	while not msg:
		c.print("[#ffd39b]Enter commit message:[/] ")
		msg = input(">> ").strip()
	return msg

def commit_and_push(msg):
	with c.status("",spinner="dots",spinner_style="#AB82FF"):	
		commit = run(['git','commit','-m',msg])
		c.print(commit.stdout)
		c.print(commit.stderr)

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

		run(['git','add','-A'])
def NORMAL():
	try:		
		is_repo()
		this_branch()
		this_files()
		run(['git','add','-A'])

		stat = run(['git','diff','--cached','--stat']).stdout or ""
		raw_diff  = run(['git','diff','--cached']).stdout or ""
		if not raw_diff.strip():
			c.print("[yellow]No Changes To commit.[/]")
			return 

		prompt = build_prompt(stat, raw_diff)
		msg = get_ai_message(prompt)

		c.print(f'\nAI:{msg}')
		c.print('[yellow]\nUse this? [y/n][/]')
		confirm = input(">> ").strip()
		if not confirm.lower() in ('y','yes'):
			msg = get_custom_message()

		commit_and_push(msg)
	except KeyboardInterrupt:
		c.print('[yellow]Aborted By User[/]')
	except Exception as e:
		run(['git','reset'])
		c.print(f"[red]\n{type(e).__name__}[/]:\n{e}")
		exit()

def YOLO():
	try:
		API_KEY = os.getenv("OPENROUTER_API_KEY")
		if not API_KEY:
			c.print('[red]OPENROUTER_API_KEY Not Found IN ENVIROMENT!![/]')
			c.print('[yellow]hint:export OPENROUTER_API_KEY="sk-or-v1-...<your-API-key>"')
			exit()

		is_repo()

		branch = run(["git",'branch','--show-current']).stdout.strip() or ''
		if not branch:
			c.print('[red]Detached HEAD detected. Please checkout a branch before using gitpush-y.[/]')
			exit()

		run(['git','add','-A'])

		with c.status("Extracting Diff ...", spinner="dots",spinner_style="#AB82FF"):
			stat = run(['git','diff','--cached','--stat']).stdout or ""
			raw_diff  = run(['git','diff','--cached']).stdout or ""
			if not raw_diff.strip():
				c.print("[yellow]No Changes To commit.[/]")
				return 

		prompt = build_prompt(stat, raw_diff)
		msg = get_ai_message(prompt)

		c.print(f'\nAI:{msg}')
		c.print('[yellow]\nUse this? [y/n][/]')
		confirm = input(">> ").strip()
		if confirm.lower() in ('n','no'):
			msg = get_custom_message()

		commit_and_push(msg)
	except KeyboardInterrupt:
		c.print('[yellow]Aborted By User[/]')
	except Exception as e:
		run(['git','reset'])
		c.print(f"[red]\n{type(e).__name__}[/]:\n{e}")
		exit()


if __name__ == '__main__':
	if sys.argv[1] == '-y':
		YOLO()
	else:
		NORMAL()
