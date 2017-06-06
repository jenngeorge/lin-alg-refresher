from math import acos, sqrt, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(c) for c in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.coordinates):
            raise StopIteration
        else:
            current_value = self.coordinates[self.current]
            self.current += 1
            return current_value

    def __len__(self):
        return len(self.coordinates)

    def __getitem__(self, i):
        return self.coordinates[i]

    def __str__(self):
        return 'Vector: {}'.format([round(coord, 3)
                                    for coord in self.coordinates])

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])

    def plus(self, v):
        return Vector(map(sum, zip(self.coordinates, v.coordinates)))

    def minus(self, v):
        return Vector([coords[0] - coords[1]
                       for coords in zip(self.coordinates, v.coordinates)])

    def times_scalar(self, factor):
        return Vector([Decimal(factor) * coord for coord in self.coordinates])

    def magnitude(self):
        return Decimal(sqrt(sum([coord * coord
                                 for coord in self.coordinates])))

    def normalize(self):
        try:
            return self.times_scalar(Decimal('1.0') / self.magnitude())
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def dot_product(self, v):
        return sum(x * y for x, y in zip(self.coordinates, v.coordinates))

    def get_angle_rad(self, v):
        dot_prod = round(self.normalize().dot_product(v.normalize()), 3)
        return acos(dot_prod)

    def get_angle_deg(self, v):
        degrees_per_rad = 180. / pi
        return degrees_per_rad * self.get_angle_rad(v)

    def is_parallel(self, v):
        return (self.is_zero() or v.is_zero() or
                self.get_angle_rad(v) in [0, pi])

    def is_orthogonal(self, v):
        return round(self.dot_product(v), 3) == 0

    def get_projected_vector(self, v):
        b_normalized = v.normalize()
        return b_normalized.times_scalar(self.dot_product(b_normalized))

    def get_orthogonal_vector(self, v):
        return self.minus(self.get_projected_vector(v))

    def cross_product(self, v):
        [x1, y1, z1] = self.coordinates
        [x2, y2, z2] = v.coordinates
        x = (y1 * z2) - (y2 * z1)
        y = -((x1 * z2) - (x2 * z1))
        z = (x1 * y2) - (x2 * y1)
        return Vector([x, y, z])

    def area_parallelogram(self, v):
        return self.cross_product(v).magnitude()

    def area_triangle(self, v):
        return self.cross_product(v).magnitude() / 2
