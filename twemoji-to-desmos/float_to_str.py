from pygame import Vector2
import math
import re


def float_to_str(x: float, decimals: int) -> str:
    """For _get_latex_dim, with sign"""
    if type(x) == Vector2:
        y = float_to_str(x.y, decimals).lstrip('+')
        x = float_to_str(x.x, decimals).lstrip('+')
        s = '+'
        if x[0] == '-' and y[0] == '-':
            s = '-'
            x, y = x.lstrip('-'), y.lstrip('-')
        return f"{s}({x},{y})"
    x = float(x)
    if not math.isfinite(x):
        return "0"
    s = format(x, f".{decimals}f")
    if s[0] != '-':
        s = '+' + s
    s = re.sub(r"(\.\d*?)0+$", r"\g<1>", s)
    s = re.sub(r"([+-])0\.", r"\g<1>.", s)
    s = s.rstrip('.')
    if s in ["+", "-", "-0"]:
        s = "+0"
    return s


def join_terms(terms: list[str]) -> str:
    """Join term returned by float_to_str"""
    def is_zero(s: str):
        return s.lstrip('+') in ['0', '(0,0)']
    s = ""
    for term in terms:
        if type(term) == str:
            if not is_zero(term):
                s += term
        elif type(term) == tuple:
            if is_zero(term[0]):
                continue
            s += term[0]
            if term[1][0].isnumeric():
                s += '*'
            s += term[1]
    if s == "":
        return "0"
    return s.lstrip('+')
