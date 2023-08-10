from typing import Optional


_possible_kwargs = ["dpi", "figsize", "x_axis", "y_axis", "cmap", "title"]

print(_possible_kwargs)


class PlotterBase:
    def __init__(
        self,
        dpi: int = 800,
        figsize: tuple = (10, 8),
        x_axis: Optional[str] = "Time (s)",
        y_axis: Optional[str] = None,
        title: Optional[str] = None,
        cmap: Optional[str] = None,
    ):
        """Base class to assess kwargs values for all plotting classess"""

        self.dpi = dpi
        self.figsize = figsize
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.title = title
        self.cmap = cmap
        self._possible_kwargs = _possible_kwargs

    def _check_kwargs(self, **kwargs):
        for key in kwargs:
            assert key in self._possible_kwargs, f"{key} is not a possible kwarg"

    def _set_kwargs(self, **kwargs):
        if "dpi" in kwargs:
            self.dpi = kwargs["dpi"]
        if "x_axis" in kwargs:
            self.x_axis = kwargs["x_axis"]
        if "y_axis" in kwargs:
            self.y_axis = kwargs["y_axis"]
        if "cmap" in kwargs:
            self.cmap = kwargs["cmap"]
        if "title" in kwargs:
            self.title = kwargs["title"]
        if "figsize" in kwargs:
            self.figsize = kwargs["figsize"]


"""
"""
from typing import Optional


class PlotterBase:
    def __init__(
        self,
        dpi: int = 800,
        figsize: tuple = (10, 8),
        x_axis: Optional[str] = "Time (s)",
        y_axis: Optional[str] = None,
        title: Optional[str] = None,
        cmap: Optional[str] = None,
    ):
        """Base class to assess kwargs values for all plotting classes"""
        self.dpi, self.figsize, self.x_axis, self.y_axis, self.title, self.cmap = (dpi,)
        figsize, x_axis, y_axis, title, cmap

    def _check_kwargs(self, **kwargs):
        _possible_kwargs = ["dpi", "figsize", "x_axis", "y_axis", "cmap", "title"]
        for key in kwargs:
            assert key in _possible_kwargs, f"{key} is not a possible kwarg"

    def _set_kwargs(self, **kwargs):
        valid_keys = ["dpi", "x_axis", "y_axis", "cmap", "title", "figsize"]
        for key, value in kwargs.items():
            if key in valid_keys:
                setattr(self, key, value)


print()
