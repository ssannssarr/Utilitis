# Utilitis

Utilitis is a collection of utility scripts and aliases designed to streamline daily development workflows. Currently, it features Gitpush — a tool that automates git push with AI-generated commit messages.

---

## Features

· AI-Powered Commit Messages – Automatically generates meaningful, conventional commit messages using AI.
· Git Automation – Simplifies the git add, commit, and push flow.
· Modular Structure – Each utility lives in its own folder with a dedicated README.
· Lightweight & Extensible – Built with Python and easily customizable.

---

## Project Structure

```
Utilitis/
├── README.md
├── gitpush/
│   └── main.py
├── pyproject.toml
└── uv.lock
```

Each script is self-contained under its respective folder.

---

## Installation

### Prerequisites

· Python 3.14 or higher
· uv (recommended) or pip

### Steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/ssannssarr/Utilitis
   cd Utilitis
   ```
2. **Install dependencies**
   ```bash
   uv sync
   ```
   **or**

   ```bash
   pip install -e .
   ```
3. **Set up your API key (for AI commit messages)**
   The tool uses [OpenRouter]("https://openrouter.ai/") by default. Set your API key as an environment variable:

   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

---

## Projects

### Gitpush

Automates the git push workflow. When you're ready to commit, Gitpush:

1. Stages all changes (git add .)
2. Analyzes the diff
3. Generates a conventional commit message via AI
4. Commits and pushes the changes

**Usage**:

```bash
gitpush
```

> Why? Repetitive commits often lead to meaningless messages. Gitpush ensures every commit is clear and consistent.

---

### Dependencies

· requests >= 2.34.2 – For API calls to OpenRouter
· rich >= 15.0.0 – For beautiful terminal output

---

## Contributing

Contributions are welcome! Before starting, please read the [contributing guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is open source. See the repository for details.

---

> ⭐ If you find this useful, consider giving the repo a star!
