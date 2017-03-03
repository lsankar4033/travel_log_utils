"""Converts org subtree corresponding to a travel log entry to markdown to be inserted into an e-mail.

Usage:
  org_to_md.py <org_file> <entry_heading>

Options:
  -h --help     Show this screen.

"""
from docopt import docopt
from itertools import islice, takewhile

import re

def _is_subheader_fn(header_depth):
    def is_subheader(line):
        header_match = re.match(r"(\*+)", line)

        if not header_match:
            return True
        else:
            sub_header_depth = len(header_match.group(0))
            return sub_header_depth > header_depth

    return is_subheader

def _org_line_to_md_line_fn(header_depth):
    def org_line_to_md_line(line):
        def header_replace(matchobj):
            subheader_depth = len(matchobj.group(0)) - header_depth
            # Ensures that first header of entry will have depth of 5 and no headers will have depth > 6
            return "#" * min(subheader_depth + 4, 6)
        line = re.sub(r"(\*+)", header_replace, line)

        def link_replace(matchobj):
            href = matchobj.group(1)
            link_name = matchobj.group(2)
            return "[{}]({})".format(link_name, href)
        return re.sub(r"\[\[(.+)\]\[(.+)\]\]", link_replace, line)

    return org_line_to_md_line

def build_markdown_str(org_file, entry_heading):
    org_lines = []
    with open(org_file, "r") as f:
        org_lines = list(f)

    # Figure out what line the entry starts at
    entry_pattern = r"(\*+)\s*({})\s*".format(entry_heading)
    entry_matches = [(i, re.fullmatch(entry_pattern, l).groups())
                      for i, l in enumerate(org_lines) if re.fullmatch(entry_pattern, l)]
    if len(entry_matches) == 0:
        return False

    (start, (header, entry_name)) = entry_matches[0]
    entry_header_depth = len(header)

    # Figure out where then entry ends by taking lines until we hit a header of <= depth as the start header
    entry_to_doc_end = org_lines[start+1:]
    entry_lines = takewhile(_is_subheader_fn(entry_header_depth), entry_to_doc_end)
    md_lines = map(_org_line_to_md_line_fn(entry_header_depth), entry_lines) # Is this better than a list comp?

    return "".join(md_lines)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    markdown_str = build_markdown_str(arguments["<org_file>"], arguments["<entry_heading>"])

    if not markdown_str:
        print("Couldn't find entry with heading {}".format(arguments["<entry_heading>"]))
    else:
        print(markdown_str)
