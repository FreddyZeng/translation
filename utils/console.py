#!/usr/bin/env python3

"""Utils for printing string with colors and styles."""

_header = '\033[95m'
_blue = '\033[94m'
_green = '\033[92m'
_warning = '\033[93m'
_fail = '\033[91m'
_bold = '\033[1m'
_under_line = '\033[4m'
_end = '\033[0m'


def _print_color(color, string):
    print(color + string + _end)


def print_header(string):
    _print_color(_header, string)


def print_bold(string):
    _print_color(_bold, string)


def print_under_line(string):
    _print_color(_under_line, string)


def print_warning(string):
    _print_color(_warning, string)


def print_fail(string):
    _print_color(_fail, string)


def print_green(string):
    _print_color(_green, string)


def print_blue(string):
    _print_color(_blue, string)
