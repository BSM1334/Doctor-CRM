#!/usr/bin/env python3
import re

po_file = r"crm\locale\ar\LC_MESSAGES\django.po"

with open(po_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

untranslated = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Look for msgid lines
    if line.startswith('msgid "'):
        msgid_text = line[7:-2]  # Strip 'msgid "' and '"\n'
        
        # Handle multiline msgid
        while msgid_text.endswith('\\') or (i + 1 < len(lines) and lines[i + 1].startswith('"')):
            if msgid_text.endswith('\\'):
                msgid_text = msgid_text[:-1]
            i += 1
            if i + 1 < len(lines) and lines[i + 1].startswith('"'):
                i += 1
                msgid_text += lines[i][1:-2]  # Strip leading quote and trailing '"\n'
        
        # Check next non-comment line for msgstr
        i += 1
        while i < len(lines) and lines[i].startswith('#'):
            i += 1
        
        if i < len(lines) and lines[i].startswith('msgstr ""'):
            untranslated.append(msgid_text)
    
    i += 1

print(f"Found {len(untranslated)} untranslated entries\n")
print("ALL Untranslated messages:")
for i, msg in enumerate(untranslated, 1):
    print(f"{i}. {msg[:100]}")
    
print("\n\nAlert-related only:")
for i, msg in enumerate(untranslated, 1):
    if any(keyword in msg.lower() for keyword in ['error', 'success', 'warning', 'alert', 'confirm', 'delete', 'sure', 'save', 'update', 'create', 'check']):
        print(f"{i}. {msg}")
