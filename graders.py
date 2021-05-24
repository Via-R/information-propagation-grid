from math import sin, pi


class GraderError(Exception):
    pass


class Falling:
    """Falling functions used for fuzzy sets."""

    @staticmethod
    def binary(c: float):
        def inner(x: float) -> float:
            """Return 1 if x is smaller than c and 0 otherwise."""

            if x <= c:
                return 1
            return 0

        return inner

    @staticmethod
    def steep(a: float, b: float):
        def inner(x: float) -> float:
            """Graph starts at 1, starts falling linearly at a and becomes 0 at b."""

            if a >= b:
                raise GraderError("Parameter a should be less than b in steep function")

            if x <= a:
                return 1
            elif x > b:
                return 0

            return (a - x) / (b - a) + 1

        return inner

    @staticmethod
    def continuous(beta: float, c: float):
        def inner(x: float) -> float:
            """Sigmoid function in range from 0 to c with values starting from 1 to 0.

            The most usual option for beta is 2."""

            if beta <= 1:
                raise GraderError("Parameter beta should be greater than 1")
            if c <= 0:
                raise GraderError("Parameter c should be bigger than 0")

            if x >= c:
                return 0

            return 1 - 1 / (1 + (x / (c - x) ** -beta))

        return inner


class Peaking:
    """Peaking functions using for fuzzy sets."""

    @staticmethod
    def binary(a: float, b: float):
        def inner(x: float) -> float:
            """Return 1 if x between a and b and 0 otherwise."""

            if a >= b:
                raise GraderError("Parameter a should be less than b in binary peaking function")

            return a <= x < b

        return inner

    @staticmethod
    def steep(a: float, b: float):
        def inner(x: float) -> float:
            """Triangle-shaped graph with center in between a and b."""

            if a >= b:
                raise GraderError("Parameter a should be less than b in peaking functions")

            if x <= a or x > b:
                return 0

            midpoint = (a + b) / 2

            if x <= midpoint:
                return (x - a) / (midpoint - a)

            return (midpoint - x) / (b - midpoint) + 1

        return inner

    @staticmethod
    def continuous_sigmoid(c: float, beta: float):
        def inner(x: float) -> float:
            """Paraboloid peaking in c, so expected range should be 2c.

            The most usual option for beta is 2."""

            if beta <= 1:
                raise GraderError("Parameter beta should be greater than 1")

            if x <= c:
                return 1 / (1 + (x / (c - x) ** -beta))

            if x >= 2 * c:
                return 0

            return 1 - 1 / (1 + ((x - c) / (2 * c - x)) ** -beta)

        return inner

    @staticmethod
    def continuous_sinusoid(c: float):
        def inner(x: float) -> float:
            """Sinusoid peaking in c, so expected range should be 2c."""

            return (sin((x - 0.5 * c) * pi / c) + 1) / 2

        return inner


class Growing:
    """Growing functions used for fuzzy sets."""

    @staticmethod
    def binary(c: float):
        def inner(x: float) -> float:
            """Return 1 if x is greater or equal to c and 0 otherwise."""

            if x > c:
                return 1
            return 0

        return inner

    @staticmethod
    def steep(a: float, b: float):
        def inner(x: float) -> float:
            """Graph starts at 0, starts growing linearly at a and becomes 1 at b."""

            if a >= b:
                raise GraderError("Parameter a should be less than b in steep function")

            if x <= a:
                return 0
            elif x > b:
                return 1

            return (x - a) / (b - a)

        return inner

    @staticmethod
    def continuous(beta: float, c: float):
        def inner(x: float) -> float:
            """Sigmoid function in range from 0 to c with values starting from 0 to 1.

            The most usual option for beta is 2."""

            if beta <= 1:
                raise GraderError("Parameter beta should be greater than 1")
            if c <= 0:
                raise GraderError("Parameter c should be bigger than 0")

            if x >= c:
                return 1

            return 1 / (1 + (x / (c - x)) ** -beta)

        return inner
