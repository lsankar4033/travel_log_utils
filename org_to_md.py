"""Converts org subtree corresponding to a travel log entry to markdown to be inserted into an e-mail.

Usage:
  org_to_md.py <org_file>

Options:
  -h --help     Show this screen.

"""
from docopt import docopt
from itertools import islice, takewhile

import re

# TODO Fix issue with multiple links on a single line
def org_line_to_md_line(line):
    def header_replace(matchobj):
        subheader_depth = len(matchobj.group(0))
        # Ensures that first header of entry will have depth of 5 and no headers will have depth > 6
        return "#" * min(subheader_depth + 4, 6)
    line = re.sub(r"(\*+)", header_replace, line)

    def link_replace(matchobj):
        href = matchobj.group(1)
        link_name = matchobj.group(2)
        return "[{}]({})".format(link_name, href)
    line = re.sub(r"\[\[(.+)\]\[(.+)\]\]", link_replace, line)

    # Remove extra newlines
    if line is "\n":
        line = "\n\n"
    elif line[-1] is '\n':
        line = line[:-1] + " "

    return line


def build_markdown_str(org_file):
    org_lines = []
    with open(org_file, "r") as f:
        org_lines = list(f)

    md_lines = [org_line_to_md_line(line) for line in org_lines]
    return "".join(md_lines)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    markdown_str = build_markdown_str(arguments["<org_file>"])

    print(markdown_str)
