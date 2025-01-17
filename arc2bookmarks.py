#!/usr/bin/env python3
import argparse
import os
import shutil
import sqlite3
from datetime import datetime


def get_arc_history_path():
    """Get the path to Arc browser's history file"""
    return os.path.expanduser(
        "~/Library/Application Support/Arc/User Data/Default/History"
    )


def convert_chrome_time(chrome_time):
    """Convert Chrome time format (microseconds) to Unix timestamp
    Chrome time starts from January 1, 1601 UTC"""
    if chrome_time:
        return int(chrome_time / 1000000 - 11644473600)
    return ""


def generate_bookmark_html(bookmarks):
    """Generate bookmarks in HTML format compatible with Chrome"""
    html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="{current_time}" LAST_MODIFIED="{current_time}">Arc History Import</H3>
    <DL><p>
""".format(current_time=int(datetime.now().timestamp()))

    for bookmark in bookmarks:
        url, title, add_date = bookmark
        html += f'        <DT><A HREF="{url}" ADD_DATE="{add_date}">{title}</A>\n'

    html += """    </DL><p>
</DL><p>"""
    return html


def export_bookmarks(min_visits=1, output_file="arc_bookmarks.html"):
    """Export Arc browser history as Chrome-compatible bookmarks.

    Args:
        min_visits (int): Minimum number of visits required for a URL to be exported
        output_file (str): Path to the output HTML file
    """
    history_path = get_arc_history_path()

    if not os.path.exists(history_path):
        print(f"Error: History file not found at {history_path}")
        return

    # Create a temporary copy of the database to avoid locks
    temp_history = "temp_history"
    shutil.copy2(history_path, temp_history)

    try:
        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()

        # Fetch history data sorted by visit count
        cursor.execute(
            """
            SELECT url, title, last_visit_time
            FROM urls
            WHERE title IS NOT NULL
            AND title != ''
            AND visit_count >= ?
            ORDER BY visit_count DESC, last_visit_time DESC
        """,
            (min_visits,),
        )

        bookmarks = []
        for row in cursor.fetchall():
            url, title, last_visit_time = row
            add_date = convert_chrome_time(last_visit_time)
            if url and title and add_date:
                bookmarks.append((url, title, add_date))

        # Write to HTML file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(generate_bookmark_html(bookmarks))

        print(f"✓ Exported {len(bookmarks)} bookmarks to {output_file}")
        print(f"✓ Minimum visits threshold: {min_visits}")
        print("ℹ️  To import: Open Chrome/Arc → Bookmarks → Import bookmarks")

    except sqlite3.Error as e:
        print(f"Error: Database error occurred: {e}")
    finally:
        if conn:
            conn.close()
        if os.path.exists(temp_history):
            os.remove(temp_history)


def main():
    parser = argparse.ArgumentParser(
        prog="arc2bookmarks",
        description="Convert Arc browser history to Chrome-compatible bookmarks",
        epilog="Example: arc2bookmarks -v 5 -o frequently_visited.html",
    )
    parser.add_argument(
        "-v",
        "--min-visits",
        type=int,
        default=1,
        help="minimum number of visits required (default: 1)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="arc_bookmarks.html",
        help="output file path (default: arc_bookmarks.html)",
    )
    args = parser.parse_args()

    export_bookmarks(min_visits=args.min_visits, output_file=args.output)


if __name__ == "__main__":
    main()
