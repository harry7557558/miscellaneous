from heapq import merge
from pygame import Vector2
from spline import Ellipse, BezierCurve, BezierSpline, clean_spline
from trig_spline import TrigSpline
from float_to_str import join_curves
import emoji
import merge_shapes
from copy import deepcopy
import math
import numpy as np
import xml.dom.minidom
import re
import json
import warnings


class Mat2x3:
    """2D transformation matrix"""

    def __init__(self, mat: list[list[float]]):
        self.mat = [
            [float(mat[0][0]), float(mat[0][1]), float(mat[0][2])],
            [float(mat[1][0]), float(mat[1][1]), float(mat[1][2])]
        ]

    def __mul__(a: "Mat2x3", b: "Mat2x3") -> "Mat2x3":
        """Matrix multiplication, returns the matrix when a is applied to b"""
        if type(b) is Vector2:
            return Vector2(
                a.mat[0][0]*b.x + a.mat[0][1]*b.y + a.mat[0][2],
                a.mat[1][0]*b.x + a.mat[1][1]*b.y + a.mat[1][2]
            )
        return Mat2x3([
            [
                a.mat[0][0]*b.mat[0][0] + a.mat[0][1]*b.mat[1][0],
                a.mat[0][0]*b.mat[0][1] + a.mat[0][1]*b.mat[1][1],
                a.mat[0][0]*b.mat[0][2] + a.mat[0][1]*b.mat[1][2] + a.mat[0][2]
            ],
            [
                a.mat[1][0]*b.mat[0][0] + a.mat[1][1]*b.mat[1][0],
                a.mat[1][0]*b.mat[0][1] + a.mat[1][1]*b.mat[1][1],
                a.mat[1][0]*b.mat[0][2] + a.mat[1][1]*b.mat[1][2] + a.mat[1][2]
            ]
        ])


def parse_css_transform(transform: str) -> Mat2x3:
    """Construct transformation matrix from a CSS transformation string
       https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
       Not well-tested, may have bug
    """
    transform = transform.strip().replace(",", " ")
    transform = re.sub(r"\s+", " ", transform)
    transform = transform.replace("( ", "(").replace(" )", ")")
    transform = [t.strip()+')' for t in transform.rstrip(')').split(')')]
    matrix = Mat2x3([[1, 0, 0], [0, 1, 0]])
    for ts in transform:
        # matrix
        regex = r"^matrix\(([0-9\.\+\-e]+) ([0-9\.\+\-e]+) ([0-9\.\+\-e]+) ([0-9\.\+\-e]+) ([0-9\.\+\-e]+) ([0-9\.\+\-e]+)\)$"
        match = re.match(regex, ts)
        if match:
            matrix *= Mat2x3([[
                float(match.group(1)),
                float(match.group(2)),
                float(match.group(3))
            ], [
                float(match.group(4)),
                float(match.group(5)),
                float(match.group(5))
            ]])
            continue
        # translate
        regex = r"^translate\(([0-9\.\+\-e]+) ([0-9\.\+\-e]+)\)$"
        match = re.match(regex, ts)
        if match:
            dx = float(match.group(1))
            dy = float(match.group(2))
            matrix *= Mat2x3([[1, 0, dx], [0, 1, dy]])
            continue
        # rotate about a point
        regex = r"^rotate\(([0-9\.\+\-e]+) ([0-9\.\+\-e]+) ([0-9\.\+\-e]+)\)$"
        match = re.match(regex, ts)
        if match:
            a = float(match.group(1)) * math.pi/180.
            sa, ca = math.sin(a), math.cos(a)
            dx = float(match.group(2))
            dy = float(match.group(3))
            rmat = Mat2x3([[1, 0, dx], [0, 1, dy]]) \
                * Mat2x3([[ca, -sa, 0], [sa, ca, 0]]) \
                * Mat2x3([[1, 0, -dx], [0, 1, -dy]])
            matrix *= rmat
            continue
        # not implemented
        raise ValueError("Transform attribute parse error", ts)
    return matrix


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


def reduce_color(col: str) -> str:
    """24 bit RGB hex color to 12 bit"""
    col = col.lstrip('#')
    if len(col) != 3:
        col = int(col, base=16)
        r, g, b = col//65536, (col//256) % 256, col % 256
        col = ((((0xf0 | r//16) << 4) | g//16) << 4) | b//16
        col = hex(col).lstrip('0x')[1:]
    return '#' + col


def load_svg_shapes(filename: str):
    doc = xml.dom.minidom.parse(filename)
    svg = doc.firstChild
    assert svg.nodeName == "svg"

    def parse_node(node, existing_attributes={}):
        nodeName = node.nodeName
        attributes = deepcopy(existing_attributes)
        for (attrib, value) in dict(node.attributes.items()).items():
            if attrib == 'transform' and attrib in attributes:
                value = attributes[attrib] + value
            attributes[attrib] = value

        if nodeName == "g":
            shapes = []
            for child in node.childNodes:
                shapes += parse_node(child, attributes)
            return shapes

        if 'fill' not in attributes:
            attributes['fill'] = '#000'
        if attributes['fill'] == "none":
            return []
        # case work for those appear in the list
        if attributes['fill'] == "green":
            attributes['fill'] = "#008000"
        if attributes['fill'] == "navy":
            attributes['fill'] = "#000080"

        if nodeName == "path":
            spline = parse_path(attributes['d'])
            if spline == None:
                raise ValueError("SVG path parsing error.")
            shape = spline

        elif nodeName == "ellipse":
            ellipse = Ellipse(attributes['cx'], attributes['cy'],
                              attributes['rx'], attributes['ry'])
            shape = ellipse

        elif nodeName == "circle":
            ellipse = Ellipse(attributes['cx'], attributes['cy'],
                              attributes['r'], attributes['r'])
            shape = ellipse

        else:
            raise AttributeError(
                f"Unsupported node name {nodeName} in {filename}")

        transform = Mat2x3([[1, 0, 0], [0, -1, 0]])
        if 'transform' in attributes:
            transform *= parse_css_transform(attributes['transform'])

        return [{
            'fill': reduce_color(attributes['fill']),
            'curve': shape,
            'transform': transform
        }]

    shapes = []
    errors = []
    for child in svg.childNodes:
        try:
            shapes += parse_node(child)
        except BaseException as err:
            raise err
            errors.append(err)
    return (shapes, errors)


def compress_shape_fft_to_desmos(curve, transform: Mat2x3, decimals: int) -> list[dict]:
    polygons = []
    if type(curve) == BezierSpline:
        for spline in clean_spline(curve):
            n = max(min(8*len(spline), 256), 32)
            polygons.append(spline.evaluate_n(n))
    else:
        polygons.append(curve.evaluate_n(64))
    curves = []
    for polygon in polygons:
        for i in range(len(polygon)):
            polygon[i] = transform * polygon[i]
        tsp = TrigSpline(polygon)
        tsp.phase_shift_xs1()
        latex = tsp.to_latex(decimals)
        if latex == "":
            continue
        curves.append({
            'trigSpline': tsp,
            'latex': latex,
            "parametricDomain": {"max": "1"},
        })
    return curves


def shapes_to_desmos(shapes: list[dict], fft_compress: bool, precision: float) -> dict:
    """Fit a list of shapes to Desmos
       @shapes: returned from `load_svg_shapes()` or `merge_shapes.collect_shapes_greedy()`
       The followings are meaningful if @shapes is returned from `load_svg_shapes()`:
       @fft_compress: use FFT compression or Bezier curve
       @precision: precision when rounding
    """

    decimals = -math.log10(precision)  # number of decimal places

    expressions_list = [
        {
            "type": "expression",
            "id": "c",
            "color": "#000",
            "latex": "c(t)=\\cos(2t\\pi)",
            "hidden": True
        },
        {
            "type": "expression",
            "id": "s",
            "color": "#000",
            "latex": "s(t)=\\sin(2t\\pi)",
            "hidden": True
        },
    ]
    if not fft_compress:
        # Bezier curve terms
        expressions_list.append({
            "type": "expression",
            "id": "f",
            "color": "#000",
            "latex": "f=\\operatorname{mod}(t,1)",
            "hidden": True
        })
        expressions_list.append({
            "type": "expression",
            "id": "b",
            "color": "#000",
            "latex": "b(x,y,x_1,y_1,x_2,y_2,x_3,y_3,t)=(x,y)(1-t)^3+(x+x_1,y+y_1)3t(1-t)^2+(x+x_2,y+y_2)3t^2(1-t)+(x+x_3,y+y_3)t^3",
            "hidden": True
        })

    for i in range(len(shapes)):
        shape = shapes[i]
        if 'curve' in shape:
            # returned from `load_svg_shapes()`
            if fft_compress:
                expressions = compress_shape_fft_to_desmos(
                    shape['curve'], shape['transform'], decimals)
                if len(expressions) == 0:
                    continue
                for expr in expressions:
                    expr.pop('trigSpline')
                expression = join_curves(expressions)
            else:
                expression = shape['curve'].to_desmos(decimals)
        else:
            # returned from `merge_shapes.collect_shapes_greedy()`
            expression = join_curves(shape['desmos'])

        expression['parametricDomain']['min'] = ''
        expression['domain'] = {
            # deprecated ?! still adding up bytes
            'min': '0',
            'max': expression['parametricDomain']['max']
        }
        expression['color'] = shape['fill']
        expression['fill'] = True
        expression['lines'] = False  # more bytes but much faster
        expression['fillOpacity'] = '1'
        expression['type'] = "expression"
        expression['id'] = str(i+1)
        expressions_list.append(expression)
    return json.dumps(expressions_list).replace(' ', '')


if __name__ == "__main__":

    def one_svg_to_desmos(filepath, precision: float):
        shapes, errors = load_svg_shapes(filepath)
        print(*errors, sep='\n')
        expressions = shapes_to_desmos(shapes, True, 0.5)
        expressions = f"var s=Calc.getState();s['expressions']['list']={expressions};Calc.setState(s);"
        print(expressions)
        open(".desmos", 'w').write(expressions)
        print(len(expressions))

    def one_svg_to_desmos_merge(filepath, precision: float):
        shapes = merge_shapes.load_svg_to_trig_splines(
            filepath, -math.log10(precision))
        print(len(shapes), "shapes loaded.")
        shapes = merge_shapes.collect_shapes_greedy(shapes)
        print("Merged:", len(shapes), "shapes.")
        expressions = shapes_to_desmos(shapes, True, precision)
        expressions = f"var s=Calc.getState();s['expressions']['list']={expressions};Calc.setState(s);"
        print(expressions)
        open(".desmos", 'w').write(expressions)
        print(len(expressions))

    filename = "full.svg"
    # emoji.generate_emoji_table(filename, False, None)
    one_svg_to_desmos_merge(filename, 0.5)
