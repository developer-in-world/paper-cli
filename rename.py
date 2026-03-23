import os

def update_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = text.replace("ML papers", "research papers")
    text = text.replace("ML paper", "research paper")
    text = text.replace("What ML topic", "What scientific topic")
    text = text.replace("ML research community", "global research community")
    text = text.replace("ML topic", "scientific topic")
    text = text.replace("ML Paper", "Research Paper")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

for f in ["README.md", "main.py", "summarizer.py"]:
    update_file(f)
