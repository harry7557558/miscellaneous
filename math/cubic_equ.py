# A neater cubic equation solver in SymPy

# Sometimes, the root of a cubic equation can be written neatly
# using trigonometric/hyperbolic functions.

# Useful when a lot of coefficients of the cubic function are
# constant and nice integer.

# Try all return values and find the root(s) that work.


import sympy


def solve_cubic(a, b, c, d):
    """ Return possible roots of ax³+bx²+cx=d
        a, b, c, d are SymPy symbols (assuming real numbers) """
    from sympy import sympify, simplify
    from sympy import sqrt, sin, asin, sinh, asinh, cosh, acosh, pi
    a, b, c, d = sympify(a), sympify(b), sympify(c), sympify(d)
    b, c, d = b/a, c/a, d/a
    # shift the cubic function so it becomes x³+px+q
    f = -b/3
    p = 3*f**2 + 2*b*f + c
    q = f**3 + b*f**2 + c*f + d
    # different cases when the sign of p is different
    u = simplify(2*sqrt(-p/3))
    mq = simplify((4/u**3)*q)
    v = simplify(2*sqrt(p/3))
    nq = simplify((4/v**3)*q)
    # three roots
    r1 = [u*sin(asin(mq)/3)+f, -v*sinh(asinh(nq)/3)+f]
    r2 = [u*sin((asin(mq)-2*pi)/3)+f, -u*cosh(acosh(mq)/3)+f]
    r3 = [u*sin((asin(mq)+2*pi)/3)+f, u*cosh(-acosh(-mq)/3)+f]
    # return roots
    return [r1, r2, r3]
    # deprived because SymPy isn't quite smart in doing this
    return [[simplify(r[0]), simplify(r[1])] for r in [r1, r2, r3]]


if __name__ == "__main__":

    r = solve_cubic(2, -3, 0, 'v')
    print(r)

