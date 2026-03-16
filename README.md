# clipboard-py
Clipboard manager with persistent history. Works on macOS (pbcopy) and Linux (xclip).
```bash
echo "hello" | python clipboard.py copy
python clipboard.py paste
python clipboard.py history -n 20
python clipboard.py get 5
```
## Zero dependencies. Python 3.6+.
