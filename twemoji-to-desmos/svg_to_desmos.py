from pygame import Vector2
from spline import Ellipse, BezierCurve, BezierSpline, clean_spline
import math
import xml.dom.minidom
import re
import json
import warnings


def parse_path(s: str) -> BezierSpline:
    """Parse an SVG path
    Additional info:
        Translated from a JavaScript function I wrote previously.
        The specification of SVG path string can be found at
        https://www.w3.org/TR/SVG/paths.html#DProperty
    Args:
        s: the SVG path string
    Returns:
        a parsed spline, or None if there is an error during parsing
    """
    cmd = ''  # MZLHVCSQTA
    p_start = Vector2(0, 0)  # starting point
    p0 = Vector2(0, 0)  # ending point
    s_prev, t_prev = Vector2(0, 0), Vector2(
        0, 0)  # reflection in smoothed curves
    spline = BezierSpline()  # result

    d = 0  # index
    while d < len(s):

        # parsing functions

        def is_float(c: str) -> bool:
            if c in ['-', '.']:
                return True
            try:
                x = float(c)
            except ValueError:
                return False
            return not math.isnan(x)

        def read_float() -> float:
            """Read the next float in s and increase d"""
            nonlocal s, d
            while d < len(s) and re.match(r"^[\s\,]$", s[d]):
                d += 1
            if d >= len(s) or not is_float(s[d]):
                return float('nan')
            ns = ""
            while d < len(s):
                if s[d] in "0123456789" \
                    or (s[d] in '+-' and (ns == "" or ns[-1] == 'e')) \
                        or (s[d] in "Ee." and s[d].lower() not in ns):
                    ns += s[d].lower()
                else:
                    break
                d += 1
            try:
                return float(ns)
            except ValueError:
                return float('nan')

        def read_point() -> Vector2:
            """Read the next point in s and increase d"""
            x = read_float()
            y = read_float()
            return Vector2(x, y)

        # get command
        while d < len(s) and re.match(r"^[\s\,]$", s[d]):
            d += 1
        if s[d].upper() in "MZLHVCSQT":
            cmd = s[d]
            d += 1
        elif not is_float(s[d]):
            return None

        # case work for each command

        if cmd in "Mm":  # move
            p = read_point()
            if cmd.islower():
                p += p0
            p_start = p
            p0 = p

        elif cmd in "Zz":  # close
            spline.add_curve(BezierCurve((p0, p_start)))
            p0 = p_start

        elif cmd in "Ll":  # line
            p = read_point()
            if cmd.islower():
                p += p0
            spline.add_curve(BezierCurve((p0, p)))
            p0 = p

        elif cmd in "Hh":  # horizontal line
            x = read_float()
            if cmd.islower():
                p = Vector2(p0.x+x, p0.y)
            else:
                p = Vector2(x, p0.y)
            spline.add_curve(BezierCurve((p0, p)))
            p0 = p

        elif cmd in "Vv":  # vertical line
            y = read_float()
            if cmd.islower():
                p = Vector2(p0.x, p0.y+y)
            else:
                p = Vector2(p0.x, y)
            spline.add_curve(BezierCurve((p0, p)))
            p0 = p

        elif cmd in "Cc":  # cubic bezier curve
            p1 = read_point()
            p2 = read_point()
            p3 = read_point()
            if cmd.islower():
                p1 += p0
                p2 += p0
                p3 += p0
            spline.add_curve(BezierCurve((p0, p1, p2, p3)))
            s_prev = p2
            p0 = p3

        elif cmd in "Ss":  # smooth cubic bezier curve
            p2 = read_point()
            p3 = read_point()
            if cmd.islower():
                p2 += p0
                p3 += p0
            p1 = 2.0*p0 - s_prev
            spline.add_curve(BezierCurve((p0, p1, p2, p3)))
            s_prev = p2
            p0 = p3

        elif cmd in "Qq":  # quadratic bezier curve
            p1 = read_point()
            p2 = read_point()
            if cmd.islower():
                p1 += p0
                p2 += p0
            spline.add_curve(BezierCurve((p0, p1, p2)))
            t_prev = p1
            p0 = p2

        elif cmd in "Tt":  # smooth quadratic bezier curve
            p2 = read_point()
            if cmd.islower():
                p2 += p0
            p1 = 2.0*p0 - t_prev
            spline.add_curve(BezierCurve((p0, p1, p2)))
            t_prev = p1
            p0 = p2

        else:  # elliptic arc ?!
            return None

        if cmd not in "CcSs":
            s_prev = p0
        if cmd not in "QqTt":
            t_prev = p0

    return spline


def load_svg_shapes(filename: str):
    doc = xml.dom.minidom.parse(filename)
    svg = doc.firstChild
    assert svg.nodeName == "svg"

    def parse_node(node):
        nodeName = child.nodeName
        attributes = dict(child.attributes.items())

        if 'fill' not in attributes:
            raise AttributeError(
                "`fill` attribute does not appear in attributes list.")
        if 'transform' in attributes:
            raise NotImplementedError(
                "SVG `transform` attribute is not supported.")

        if nodeName == "path":
            spline = parse_path(attributes['d'])
            if spline == None:
                raise ValueError("SVG path parsing error.")
            shape = spline

        elif nodeName == "ellipse":
            ellipse = Ellipse(attributes['cx'], attributes['cy'],
                              attributes['rx'], attributes['ry'])
            shape = ellipse

        else:
            raise AttributeError(
                f"Unsupported node name {nodeName} in {filename}")

        shape.reverse_y()
        return {
            'fill': attributes['fill'],
            'curve': shape
        }

    shapes = []
    errors = []
    for child in svg.childNodes:
        try:
            shape = parse_node(child)
            shapes.append(shape)
        except BaseException as err:
            errors.append(err)
    return (shapes, errors)


def shapes_to_desmos(shapes: list[dict]) -> dict:
    expressions = [
        {
            "type": "expression",
            "id": "f",
            "color": "#000",
            "latex": "f=\\operatorname{mod}(t,1)",
            "hidden": True
        },
        {
            "type": "expression",
            "id": "c",
            "color": "#000",
            "latex": "c(t)=\\cos(t)",
            "hidden": True
        },
        {
            "type": "expression",
            "id": "s",
            "color": "#000",
            "latex": "s(t)=\\sin(t)",
            "hidden": True
        }
    ]
    for i in range(len(shapes)):
        shape = shapes[i]
        expression = shape['curve'].to_desmos(decimals=3)
        expression['parametricDomain']['min'] = ''
        expression['domain'] = {
            'min': '0',
            'max': expression['parametricDomain']['max']
        }
        expression['color'] = shape['fill']
        expression['fill'] = True
        expression['fillOpacity'] = '1'
        expression['type'] = "expression"
        expression['id'] = str(i+1)
        expressions.append(expression)
    print(json.dumps(expressions))


shapes, errors = load_svg_shapes("f7b3f6b926cb31a17d4928d076febab4.svg")
print(errors)
shapes_to_desmos(shapes)
