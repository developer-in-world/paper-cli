import subprocess
import os

exe_path = os.path.join('dist', 'paper-cli.exe')
print(f"Testing {exe_path}...")

try:
    p = subprocess.run([exe_path], input=b"Q-Star Meets Scalable Posterior Sampling\nexit\n", capture_output=True, timeout=30)
    print(p.stdout.decode('utf-8', errors='ignore'))
    if p.stderr:
        print("ERRORS:", p.stderr.decode('utf-8', errors='ignore'))
except Exception as e:
    print("Failed to run:", e)
