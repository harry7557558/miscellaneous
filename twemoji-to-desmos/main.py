import emoji
import merge_shapes
import svg_to_desmos
import json


def count_latex_ratio(filename):
    with open(filename, "r") as fp:
        content = fp.read()
    start = "var s=Calc.getState();s['expressions']['list']="
    end = ";Calc.setState(s);"
    content = content[len(start):len(content)-len(end)]

    tot_size = len(content)
    expressions = json.loads(content)

    latex_size = 0
    for expr in expressions:
        if "latex" in expr:
            latex_size += len(expr['latex'])

    ratio = latex_size/tot_size
    print(f"{latex_size}/{tot_size}", "{:.2f}%".format(ratio))


def main():

    # emoji.download_emojis()

    filename = "full.svg"
    scale = 2.0

    # emoji.generate_emoji_table(filename, False, ['nature'])
    # emoji.generate_emoji_table(filename, True, ['people'], slice(0, 100))
    # emoji.generate_emoji_table(filename, False, None)
    emoji.generate_emoji_table(filename, True, None)

    shapes = merge_shapes.load_svg_to_trig_splines(filename, scale)
    print(len(shapes), "shapes loaded.")
    shapes = merge_shapes.collect_shapes_greedy(shapes)
    print(len(shapes), "shapes after merging by color.")
    expressions_app = []
    expressions_app = merge_shapes.extract_common_latex(shapes)
    print(len(expressions_app), "common expressions extracted.")
    expressions = svg_to_desmos.shapes_to_desmos(shapes, expressions_app)
    expressions = json.dumps(expressions, separators=(',', ':'))
    expressions = f"var s=Calc.getState();s['expressions']['list']={expressions};Calc.setState(s);"
    open(".desmos", 'w').write(expressions)
    print(len(expressions), "bytes")


if __name__ == "__main__":
    main()
    # count_latex_ratio(".desmos")
