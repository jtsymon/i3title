#!/usr/bin/env python

import i3ipc
import argparse

parser = argparse.ArgumentParser(description='Print the active window\'s title')
parser.add_argument('-t', '--truncate', help='Truncate titles to a max length', type=int, default=None)
parser.add_argument('-s', '--subscribe', help='Monitor the active window and print whenever it changes', action='store_true')
args = parser.parse_args()

truncate_to = None
if args.truncate:
    truncate_to = max(1, args.truncate - 3)

def print_window_title(container):
    title = container.name
    if not title:
        print("")
        return
    if args.truncate and len(title) > args.truncate:
        title = title[:truncate_to] + '...'
    print(title)

def on_window_focus(i3, e):
    print_window_title(e.container)

i3 = i3ipc.Connection()
print_window_title(i3.get_tree().find_focused())
if args.subscribe:
    i3.on("window::focus", on_window_focus)
    i3.on("window::title", on_window_focus)
    i3.main()
