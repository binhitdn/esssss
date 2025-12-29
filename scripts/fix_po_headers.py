#!/usr/bin/env python3
"""
Fix header issues in Vietnamese .po files
"""
import re
from pathlib import Path

def fix_header(filepath):
    """Fix header formatting issues"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix lines 16-25 which have the header info
    fixed_lines = []
    in_header = False
    header_buffer = []
    
    for i, line in enumerate(lines, 1):
        # Detect start of header (line with msgid "")
        if line.strip() == 'msgid ""' and i < 15:
            in_header = True
            fixed_lines.append(line)
            continue
        
        # Collect header lines
        if in_header and line.strip().startswith('"'):
            # Fix any broken strings
            if not line.strip().endswith('\\n"') and not line.strip().endswith('"'):
                line = line.rstrip() + '\\n"\n'
            fixed_lines.append(line)
            
            # End of header
            if line.strip() == '""':
                in_header = False
        else:
            fixed_lines.append(line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

def main():
    vi_dir = Path('locales/vi/LC_MESSAGES')
    po_files = list(vi_dir.glob('*.po'))
    
    print(f"Fixing {len(po_files)} .po files...")
    
    for po_file in sorted(po_files):
        if po_file.name == 'babel.po':
            continue  # Skip manually created file
        try:
            fix_header(po_file)
            print(f"  ✓ Fixed {po_file.name}")
        except Exception as e:
            print(f"  ✗ Error fixing {po_file.name}: {e}")
    
    print("Done!")

if __name__ == '__main__':
    main()
