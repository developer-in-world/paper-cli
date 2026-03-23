# 📖 Paper CLI - Official User Manual

Welcome to the **Paper CLI V0.001** user manual! This guide covers everything you need to know to harness the full power of your terminal-based research assistant.

---

## 1. Launching the App

There are two ways to use Paper CLI:

### The Interactive Loop (Recommended for Windows)
Simply **double-click `paper-cli.exe`** in your File Explorer. 
- It will dramatically open a terminal window.
- It will welcome you with the `developed by mg` watermark.
- It will endlessly prompt you: `What scientific topic do you want to research?`
- To exit the program, type `exit` or just press `Enter` on a blank line.

### The Command-Line Interface (For Power Users)
If you prefer traditional terminal execution, you can run the executable (or the installed python package) directly via PowerShell, bash, or cmd:

```bash
# Basic single execution
paper-cli search "quantum computing"

# Save the papers locally
paper-cli search "diffusion model" --save
```

---

## 2. Advanced Searching Techniques

Paper CLI is equipped with a heavily modified **Dual-Phase "Google-Style" Engine**. You do not need to use Boolean logic (AND/OR). 

### How it works:
When you search for a long sentence like `Q-Star Meets Scalable Posterior Sampling`, the engine performs two invisible phases:
1. **Phase 1:** It forces the arXiv servers to search for that **exact phrase** unbroken. If a paper titled exactly that exists, you get it instantly.
2. **Phase 2:** If you were just typing broad topics (like `transformer robotics healthcare`), Phase 1 will fail. The engine will instantly recognize this, sleep for 3 seconds to protect your IP address, and seamlessly launch a loose broad-search finding papers related to any combination of your keywords!

### Optional Command Flags:
If you are using the CLI mode, you have access to powerful flags:

- `--limit N`: Tell the computer exactly how many papers to fetch (Default: 5).
  `paper-cli search "transformer" --limit 15`
- `--category CAT`: Restrict the entire search to a specific scientific domain (e.g. `cs.CV` for computer vision, `quant-ph` for quantum physics).
  `paper-cli search "diffusion" --category "cs.CV"`
- `--save`: Tell the CLI to physically save the fetched results to your personal offline database.
- `--tags "tags"`: Tag your saved databases.
  `paper-cli search "LLMs" --save --tags "AI, large models"`

---

## 3. Your Offline Knowledge Base

Whenever you use the `--save` flag, your papers, their GitHub codes, and their Mistral AI summaries are permanently etched onto your hard drive. 

This database is a standalone SQLite file automatically created at `~/.paper_cli_storage.db`. 

### Browsing Saved Papers
You can effortlessly recall anything you saved even if you don't have internet access:

```bash
# See EVERYTHING you have ever saved
paper-cli saved

# Search your saved database for a keyword
paper-cli saved "GAN"
paper-cli saved "quantum"
```

---

## 4. API Keys and Security

On your very first run, Paper CLI asks for keys.

- **GitHub Token:** Without this, GitHub only allows you to search for code 10 times a minute. Putting a token here safely bumps you to 30. Get it at github.com/settings/tokens.
- **Mistral API Key:** If you provide this, Mistral Small will instantly read the 5000-character abstract of the paper, understand it, and spit out exactly 3 bullet points: Problem, Method, Key Contribution. 

**Are they safe?**
Yes. Your keys are immediately encrypted into a `~/.paper_cli_config.json` file. The CLI forcefully applies strict Unix (`chmod 600`) and Windows (`icacls`) file-locks onto this document so ONLY your personal computer account can physically read the text.

---

## 5. Troubleshooting (429 Errors)

If you see a warning about a **429 API Limit**, do not panic! 

Because Paper CLI relies on `arXiv.org` and `GitHub.com`'s public databases, they occasionally flag users who hit their servers too fast. 
- Paper CLI has an onboard **Global Throttler**, which guarantees 3 seconds spacing between arXiv hits.
- If you still hit a 429, simply take a break, grab a cup of coffee, and try again in 5 minutes after the arXiv servers clear your IP.

*(developed by mg - V0.001)*
