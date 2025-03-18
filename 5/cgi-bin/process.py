#!/usr/bin/env python3

import cgi
import itertools


def find_longest_sequence(s):
    if not s:
        return "", 0
    max_seq = max(((char, len(list(seq))) for char, seq in itertools.groupby(s)), key=lambda x: x[1])
    return max_seq


def generate_html(input_string, max_char, max_len):
    highlighted = "No input provided." if not input_string else input_string.replace(
        max_char * max_len, f"<span style='color:red; font-weight:bold;'>{max_char * max_len}</span>")

    return f"""
    <html>
    <head>
        <title>Longest Sequence Finder</title>
        <style>body {{ font-family: Arial, sans-serif; }}</style>
    </head>
    <body>
        <h2>Input String:</h2>
        <p>{highlighted}</p>
        <h3>Longest sequence: {max_char} ({max_len} times)</h3>
        <br>
        <a href='/'>Go Back</a>
    </body>
    </html>
    """


def main():
    print("Content-type: text/html\n")
    form = cgi.FieldStorage()
    input_string = form.getvalue("input_string", "")
    max_char, max_len = find_longest_sequence(input_string)
    html_output = generate_html(input_string, max_char, max_len)
    print(html_output)


if __name__ == "__main__":
    main()
