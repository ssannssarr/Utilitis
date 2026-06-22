# Contributing

<b align="center">WELCOME! WELCOME!</b>

Thank you for your interest in contributing to **Utilitis**.

This repository contains scripts and utilities that I use in my daily workflow. Contributions are welcome as long as they align with the purpose of the project.

---

## Before You Start

Please:

- Read the project [README](./README.md) .
- Check existing [issues](https://github.com/ssannssarr/Utilitis/issues) and pull requests before creating a new one.
- Keep changes focused and easy to review.

---

## What Can Be Contributed?

Examples include:

- Bug fixes
- Code improvements
- Documentation improvements
- New utility scripts that fit the project's purpose
- Performance or reliability improvements

## Coding Guidelines

- Keep code simple and readable. (At least a human should know what is written😂)
- Add comments only when they improve understanding. (In simple words, don't make comment jungle. ^;^ )
- Avoid unnecessary dependencies. 

---

## Pull Requests

When opening a pull request:

1. Clearly describe what changed. (Simple? Short? -OK Just explain what you've done)
2. Explain why the change is useful.(Explain Why?)

---

## Reporting Issues

If you find a bug, please include:

- What happened
- What you expected to happen
- Steps to reproduce the issue
- Relevant error messages or screenshots

---

## Development 

> NOTE: This project uses `uv` as its package manager. If you don't have `uv`, download it from [Astral.sh](https://docs.astral.sh/uv/).

1. Fork the repo

2. Clone the repo & Go to the repo:
	```bash
	git clone https://github.com/<your-username>/Utilitis
	cd Utilitis
	```

3. Create new branch 
	```bash 
	git checkout -b "feat: <describe-the-feature>"
	```
	- Try to keep the branch name in this format:

		|**TYPE**|**DESCRIPTION**|
		|---|---|
		|feat:|when adding new feature|
		|fix:|when fixing a bug|
		|doc:|when working on documentation|

		> This helps to distinguish who is doing what!

4. Install the dependencies:
	```bash
	uv sync
	```
	**OR**
	```bash
	pip install -e . 
	```

5. Start working.

---

## Questions

If you are unsure whether a contribution fits the project, feel free to open an issue and discuss it first.

---

Thank you for helping improve Utilitis.
