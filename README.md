# Batch Rename
A simple command-line tool for renaming multiple files using regex patterns.

## Features
- Rename multiple files using regular expressions
- Preview changes before applying them
- Dry-run mode to test without actually renaming
- Silent mode for automated use
- Color-coded output for better visibility
- Confirmation prompts to prevent accidental changes

## Installation
1. Downlaod the latest executable from [Releases](/releases) section.
2. add to paths
    - windows: add executable path to `Environment Variables/(User/System)/PATH -> new`
    - unix: 
        1. copy executable to `/bin`
        2. give executaion permission 

## Usage
```bash
batch-rename <pattern> <replacement> \[options]
```

### Arguments
- `pattern`: Regular expression pattern to match files
- `replacement`: Replacement string (can include regex groups like $1, $2, etc.)

### Options
- `-y, --yes`: Skip confirmation prompt
- `-d, --dry-run`: Show what would be renamed without actually renaming
- `-s, --silent`: Suppress all output

## Examples
### Basic renaming
```bash
batch-rename "old" "new"
```
### Rename files with extension
```bash
batch-rename "\\.txt$" ".bak"
```
### Rename with capture groups
```bash
batch-rename "file\_(\\d+)\\.txt" "document\_$1.txt"
```
### Preview changes
```bash
batch-rename "old" "new" --dry-run
```
### Silent mode
```bash
batch-rename "old" "new" --silent
```

## Development Requirements
- Python 3.x

## Contribution
- You can open Issues for any bug report or feature request.
- You are free to contribute to this project by following these steps:
   1. Fork this Repo.
   2. Create a new branch for your feature/bugfix in your forked Repo.
   3. Commit your changes to the new branch you just made.
   4. Create a pull request from your branch into the `master` branch of This Repo([https://github.com/IPdotSetAF/batch-rename](https://github.com/IPdotSetAF/batch-rename)).

---

**This tool was developed in the unlawful Nation-wide Internet cutoff in Iran due to lack of access to similar tools on the Internet.**

**Differentiated Internet Access is against Iranian Constitutional Law**
**Each and every people have the right to access Internet as equals.**

**Internet was cutoff on us (and still is) with the excuse of US and Israel ter\*rist regime unlawful war against Iran which ki\*led thousonds of innocent people and hundreds of children.**

**This tool was designed to be minimal and get its job done. Share our voice with the world by staring, using and inviting others to use this tool.**