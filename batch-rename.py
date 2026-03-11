import os
import re
import argparse
import sys

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
    parser.add_argument('pattern', help='Regex pattern to match files')
    parser.add_argument('replacement', help='Replacement string')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Show what would be renamed without actually renaming')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode - no output' )
    
    args = parser.parse_args()
    
    silent = args.silent

    # Find all files in current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Filter files matching pattern
    matched_files = []
    for file in files:
        if re.match(args.pattern, file):
            new_name = re.sub(args.pattern, args.replacement, file)
            if new_name != file:
                matched_files.append((file, new_name))
    
    if not matched_files:
        p("No files matched the pattern")
        return
    
    # Display files to be renamed
    p(f"Found {len(files)} matches:")
    for old, new in matched_files:
        p(f"{old} -> {new}", args.dry_run)
    
    # Perform renaming
    if args.dry_run:
        p("Dry run complete - no files were renamed")
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
