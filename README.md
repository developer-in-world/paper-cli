<p align="center">
  <h1 align="center">🧠 Paper CLI (v0.001)</h1>
  <p align="center"><strong>AI-powered command-line research assistant for Scientific Papers</strong></p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.8+-green?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/version-v0.001-blue" alt="Version">
    <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  </p>
</p>

---

> **"In 5 minutes, understand 10 papers."**

Paper CLI fetches the latest scientific papers from **arXiv**, discovers matching **GitHub repositories**, generates concise **AI summaries** via Mistral, and saves everything to a **local SQLite knowledge base** — all from your terminal.

**This is a fully open-source project.** You are free to use, modify, distribute, fork, and build upon this tool however you wish under the [MIT License](LICENSE).

---

## ✨ v0.001 Features

| Feature | Description |
|---|---|
| 🔍 **Google-Style Search** | Automatically tries exact-phrase matching first, gracefully falling back to related-words if no papers are found |
| 🔄 **Interactive Loop** | Double-click the Windows `.exe` to launch an endless conversational research loop |
| 💻 **Code Discovery** | Finds the best GitHub repo for each paper, ranked by stars + recency |
| 🧠 **AI Summaries** | 3-bullet-point summaries via Mistral (Problem / Method / Contribution) |
| 🛡️ **Rate-Limit Immune** | Global background timer rigidly enforces arXiv's 3-second limit to protect your IP address |
| 💾 **Knowledge Base** | Save papers to an offline SQLite database with custom tags |
| 🔐 **Hardened Security** | Protected against XML Billion Laughs (XXE), SQL injection, DoS, and credential leaks |

---

## 📖 Complete Documentation

Please read the official **[User Manual](USER_MANUAL.md)** for a deep dive into commands, advanced filtering, interactive mode execution, and troubleshooting.

---

## 🚀 Quick Installation

### 🪟 Windows Users — Download & Run (No Python Needed)

The fastest way. Download a single file and start using it immediately.

1. Go to the [**Releases**](https://github.com/yourusername/paper-cli/releases) page
2. Download **`paper-cli.exe`**
3. Double-click it anywhere on your computer to launch the **Interactive Research Assistant**.

No Python installation, no cloning, no dependencies. Just download and execute.

---

### 🍎 macOS & 🐧 Linux Users — Install via pip

macOS and Linux do not support the `.exe` binary natively. Install from source using pip instead:

```bash
# Requires Python 3.8+
git clone https://github.com/yourusername/paper-cli.git
cd paper-cli
pip install .
paper-cli --help
```

---

## ⚙️ First Run — API Keys

On your very first search, the CLI will securely prompt for two API keys. 

| Key | Required? | Get It | Purpose |
|---|---|---|---|
| `GITHUB_TOKEN` | Recommended | [GitHub Settings → Tokens](https://github.com/settings/tokens) | Raises rate limit from 10 to 30 req/min |
| `MISTRAL_API_KEY` | Optional | [Mistral Console](https://console.mistral.ai/) | Powers AI-generated summaries |

Keys are stored locally at `~/.paper_cli_config.json` with strict owner-only permissions. Both keys can be skipped by simply pressing `Enter`—the tool will still function without AI summaries.

---

## 🤝 Contributing & Reuse

**This project is fully open source under the MIT License.** Anyone is free to:

- **Use** — Download it, run it, use it for any purpose
- **Modify** — Change the code, add features, fix bugs
- **Distribute** — Share it, package it, host it anywhere
- **Fork** — Build your own version on top of it
- **Commercialize** — Use it in commercial products

### Extending the Tool

**Add a new paper source** — Create a function in `fetcher.py` returning `[{"title", "authors", "abstract", "url"}]`

**Swap the LLM** — Edit `summarizer.py` endpoint/payload. Keep the same signature: `summarize_abstract(abstract, api_key) -> str`

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, distribute, and build upon this tool however you wish. See [LICENSE](LICENSE) for full details.

---

<p align="center">
  <strong>Built with ❤️ for the global research community</strong><br>
  <em>(developed by mg)</em>
</p>
