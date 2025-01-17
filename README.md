# arc2bookmarks

Convert Arc browser history to Chrome-compatible bookmarks.
This tool helps you export your frequently visited sites from Arc browser as bookmarks that can be imported into any
browser supporting the Netscape Bookmark file format (Chrome, Firefox, Safari, etc.).

## Features

- Export Arc browser history as browser-compatible bookmarks
- Filter URLs by minimum visit count
- Sort by visit frequency and last visit time
- Compatible with Chrome, Firefox, Safari, and other browsers
- Clean and simple command-line interface

## Installation

```bash
# Clone the repository
git clone https://github.com/kei-yamazaki/arc2bookmarks.git
cd arc2bookmarks

# Make the script executable
chmod +x arc2bookmarks.py

# Optional: Create a symbolic link to make it globally available
ln -s "$(pwd)/arc2bookmarks.py" /usr/local/bin/arc2bookmarks
```

## Usage

```bash
# Basic usage (exports all visited URLs)
./arc2bookmarks.py

# Export only URLs visited at least 5 times
./arc2bookmarks.py -v 5

# Specify custom output file
./arc2bookmarks.py -o my_bookmarks.html

# Export from a specific profile
./arc2bookmarks.py -p "Profile 1"

# Combine multiple options
./arc2bookmarks.py -v 5 -o my_bookmarks.html -p "Profile 1"

# Show help
./arc2bookmarks.py --help
```

### Options

- `-v, --min-visits`: Minimum number of visits required (default: 1)
- `-o, --output`: Output file path (default: arc_bookmarks.html)
- `-p, --profile`: Arc profile name (default: Default)

## Importing Bookmarks

1. Open Chrome, Arc, or your preferred browser
2. Open the Bookmarks Manager
3. Look for "Import bookmarks" option
4. Select the exported HTML file
5. Your bookmarks will be imported under "Arc History Import" folder

## Requirements

- Python 3.6 or later
- macOS / Windows (Arc browser installed)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Documentation

- [Database Schema](docs/SCHEMA.md) - Detailed information about the Arc/Chrome history database structure

## License

MIT License - see [LICENSE](LICENSE) file for details
