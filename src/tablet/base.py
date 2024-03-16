from dataclasses import dataclass


@dataclass
class Pen:
    """
    Parameters
    ----------
    @param x X position of pen
    @param y Y position of pen
    @param azimuth Clockwise angle of pen around the Z axis in degrees
    @param tilt The angle with the XY plane in range in degrees
    @param pressure Normal pressure of the pen in range [0, 1]
    """

    x: int = 0
    y: int = 0
    azimuth: float = 0.0
    tilt: float = 0.0
    pressure: float = 0.0


class Tablet:
    """
    Base tablet class.
    """

    def __init__(self):
        self.pen = Pen()