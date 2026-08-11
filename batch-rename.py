import os
import re
import argparse
import sys

VERSION = 'v1.0.0'

COLORS = {
    "red": '\033[31m',
    "green": '\033[32m',
    "yellow": '\033[33m',
    "blue": '\033[34m',
    "magenta": '\033[35m',
    "cyan": '\033[36m',
    "white": '\033[37m',
    "reset" : '\033[0m',
}

silent = False

def p(str, force_print = False):
    if not silent or force_print:
        print(str)

def main():
    global silent

    parser = argparse.ArgumentParser(
        description='Rename files using regex patterns',
        epilog=f"""Examples:
    {sys.argv[0]} \"^xxx(.*)$\" \"yyy-\\1\"
    {sys.argv[0]} \"(.*)\\.txt$\" \"\\1_backup.txt\"
    {sys.argv[0]} \"^file_(\\d+)\\.txt$\" \"doc_\\1.txt\"""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-v', '--version', action='version', version=f'batch-rename {VERSION}')
    parser.add_argument('pattern', help='Regex pattern to match files')
    parser.add_argument('replacement', help='Replacement string')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Show what would be renamed without actually renaming')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode - no output')
    parser.add_argument('-t', '--type', choices=['f', 'd', 'a'], default='f',
                        help='Entry type to rename: f=files only (default), d=directories only, a=all')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively rename in all subdirectories')
    
    args = parser.parse_args()
    
    silent = args.silent

    # Compile the regex pattern, exit early on invalid pattern
    try:
        pattern = re.compile(args.pattern)
    except re.error as e:
        p(f"{COLORS['red']}Invalid regex pattern: {e}{COLORS['reset']}\nUse --help to see example usage.", force_print=True)
        sys.exit(1)

    entry_type = args.type
    matched_files = []

    if args.recursive:
        # Walk bottom-up so children are always renamed before their parent directory.
        # For each directory visited, collect files first then the directory itself,
        # preserving the correct rename order even when parent dirs also match.
        for dirpath, dirnames, filenames in os.walk('.', topdown=False):
            if entry_type in ('f', 'a'):
                for filename in filenames:
                    if pattern.match(filename):
                        new_name = pattern.sub(args.replacement, filename)
                        if new_name != filename:
                            matched_files.append((
                                os.path.join(dirpath, filename),
                                os.path.join(dirpath, new_name)
                            ))
            if entry_type in ('d', 'a') and dirpath != '.':
                dirname = os.path.basename(dirpath)
                if pattern.match(dirname):
                    new_name = pattern.sub(args.replacement, dirname)
                    if new_name != dirname:
                        matched_files.append((
                            dirpath,
                            os.path.join(os.path.dirname(dirpath), new_name)
                        ))
    else:
        # Non-recursive: current directory only
        entries = [
            f for f in os.listdir('.')
            if (entry_type == 'a')
            or (entry_type == 'f' and os.path.isfile(f))
            or (entry_type == 'd' and os.path.isdir(f))
        ]
        for entry in entries:
            if pattern.match(entry):
                new_name = pattern.sub(args.replacement, entry)
                if new_name != entry:
                    matched_files.append((entry, new_name))
    
    if not matched_files:
        p("No entries matched the pattern")
        return
    
    # Display files to be renamed
    p(f"Found {len(matched_files)} matches:")
    for old, new in matched_files:
        p(f"{COLORS['red']}{old}{COLORS['reset']}->\t{COLORS['green']}{new}{COLORS['reset']}", args.dry_run)
    
    # Perform renaming
    if args.dry_run:
        p("Dry run complete - no entries were renamed")
        return
    
    # Ask for confirmation
    if not args.yes:
        choice = input("\nProceed? (Y/N): ")
        if choice.upper() != "Y":
            p("Cancelled")
            return
    
    for old, new in matched_files:
        try:
            os.rename(old, new)
        except OSError as e:
            p(f"Error renaming {old}: {e}")

if __name__ == "__main__":
    main()

