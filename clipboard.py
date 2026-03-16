#!/usr/bin/env python3
"""clipboard - Clipboard manager with history."""
import subprocess, argparse, json, os, sys, time

HISTORY_FILE = os.path.expanduser('~/.clipboard_history.json')

def copy(text):
    p = subprocess.Popen(['pbcopy'] if sys.platform == 'darwin' else ['xclip', '-selection', 'clipboard'],
                         stdin=subprocess.PIPE)
    p.communicate(text.encode())

def paste():
    cmd = ['pbpaste'] if sys.platform == 'darwin' else ['xclip', '-selection', 'clipboard', '-o']
    return subprocess.check_output(cmd, text=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f: return json.load(f)
    return []

def save_history(history, max_items=100):
    with open(HISTORY_FILE, 'w') as f: json.dump(history[-max_items:], f, indent=2)

def main():
    p = argparse.ArgumentParser(description='Clipboard manager')
    sub = p.add_subparsers(dest='cmd')
    
    cp = sub.add_parser('copy', help='Copy text to clipboard')
    cp.add_argument('text', nargs='?', help='Text (or stdin)')
    
    pa = sub.add_parser('paste', help='Paste from clipboard')
    
    hi = sub.add_parser('history', help='Show clipboard history')
    hi.add_argument('-n', type=int, default=10)
    
    cl = sub.add_parser('clear', help='Clear history')
    
    sv = sub.add_parser('save', help='Save current clipboard to history')
    
    gt = sub.add_parser('get', help='Get item from history by index')
    gt.add_argument('index', type=int)
    
    args = p.parse_args()
    if not args.cmd: args.cmd = 'paste'
    
    if args.cmd == 'copy':
        text = args.text if args.text else sys.stdin.read()
        copy(text)
        history = load_history()
        history.append({'text': text[:500], 'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'len': len(text)})
        save_history(history)
        print(f"Copied ({len(text)} chars)")
    
    elif args.cmd == 'paste':
        print(paste(), end='')
    
    elif args.cmd == 'save':
        text = paste()
        history = load_history()
        history.append({'text': text[:500], 'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'len': len(text)})
        save_history(history)
        print(f"Saved ({len(text)} chars)")
    
    elif args.cmd == 'history':
        history = load_history()
        for i, item in enumerate(history[-args.n:]):
            idx = len(history) - args.n + i
            preview = item['text'][:60].replace('\n', '\\n')
            print(f"  [{idx}] {item['time']} ({item['len']}ch) {preview}")
    
    elif args.cmd == 'get':
        history = load_history()
        if 0 <= args.index < len(history):
            text = history[args.index]['text']
            copy(text)
            print(text)
        else:
            print(f"Index out of range (0-{len(history)-1})")
    
    elif args.cmd == 'clear':
        save_history([])
        print("History cleared")

if __name__ == '__main__':
    main()
