import spline
import trig_spline
import svg_to_desmos

bezier_splines = svg_to_desmos.load_svg("f7b3f6b926cb31a17d4928d076febab4.svg")
trig_splines = []
for trig_spline in bezier_splines:
    points = trig_spline.evaluate_n_alp(100)
    trig_splines.append(trig_spline.TrigSpline(points))
for trig_spline in trig_splines:
    print(trig_spline.get_latex(digits=3, optimize=False))
