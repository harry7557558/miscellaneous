# merge shapes with the same color to reduce bytes

from pygame import Vector2
from trig_spline import TrigSpline
import math
import numpy as np
import svg_to_desmos


def load_svg_to_trig_splines(filename: str, decimals: int) -> list[dict]:
    shapes, errors = svg_to_desmos.load_svg_shapes(filename)
    if len(errors) != 0:
        print(*errors, sep='\n')
    print("SVG shapes loaded")

    shapes_filtered = []
    for i in range(len(shapes)):
        if (i+1) % 1000 == 0:
            print(f"{i+1}/{len(shapes)} shapes...")
        shape = shapes[i]
        # FFT shape
        expressions = svg_to_desmos.compress_shape_fft_to_desmos(
            shape['curve'], shape['transform'], decimals)
        if len(expressions) == 0:
            continue
        # store TrigSpline and Desmos expression
        shape['trigSplines'] = []
        shape['desmos'] = []
        for expr in expressions:
            shape['trigSplines'].append(expr['trigSpline'])
            shape['desmos'].append({
                'latex': expr['latex'],
                'parametricDomain': expr['parametricDomain']
            })
        # approximate min/max
        shape['min'] = Vector2(float('inf'))
        shape['max'] = -shape['min']
        for tsp in shape['trigSplines']:
            xs, ys = tsp.evaluate_n(256, raw=True)
            shape['min'].x = min(shape['min'].x, np.min(xs))
            shape['min'].y = min(shape['min'].y, np.min(ys))
            shape['max'].x = max(shape['max'].x, np.max(xs))
            shape['max'].y = max(shape['max'].y, np.max(ys))
        shapes_filtered.append(shape)
    shapes = shapes_filtered

    # debug
    if 1:
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="2400"><g transform="scale(1,-1)">'
        for shape in shapes:
            x = shape['min'].x
            y = shape['min'].y
            width = shape['max'].x - x
            height = shape['max'].y - y
            fill = shape['fill']
            svg += f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}"/>'
        svg += '</g></svg>'
        open(".svg", 'w').write(svg)

    return shapes


if __name__ == "__main__":

    filename = "info/full.svg"
    load_svg_to_trig_splines(filename, 1)
