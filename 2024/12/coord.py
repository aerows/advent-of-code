import typing as t


class Coord(t.NamedTuple):
    row: int
    col: int

    def __add__(self, other) -> "Coord":
        """Add two coordinates or a coordinate and a tuple."""
        if isinstance(other, Coord):
            return Coord(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return Coord(self.row + other[0], self.col + other[1])
        else:
            raise TypeError(
                "Can only add Coord with another Coord or a tuple of length 2"
            )

    def __sub__(self, other) -> "Coord":
        return self + (other * -1)

    def __eq__(self, other) -> bool:
        """Check if two coordinates are equal."""
        if not isinstance(other, Coord):
            return False
        return self.row == other.row and self.col == other.col

    def __mul__(self, scalar: int) -> "Coord":
        """Multiply coordinate by an integer scalar."""
        if not isinstance(scalar, int):
            raise TypeError("Can only multiply Coord by an integer")
        return Coord(self.row * scalar, self.col * scalar)

    def __rmul__(self, scalar: int) -> "Coord":
        """Support multiplication from the right side."""
        return self.__mul__(scalar)

    def __repr__(self) -> "Coord":
        """String representation of the coordinate."""
        return f"Coord(row={self.row}, col={self.col})"

    def __mod__(self, other) -> "Coord":
        """Modules two coordinates or a coordinate and a tuple."""
        if isinstance(other, Coord):
            return Coord(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return Coord(self.row + other[0], self.col + other[1])
        else:
            raise TypeError(
                "Can only add Coord with another Coord or a tuple of length 2"
            )
