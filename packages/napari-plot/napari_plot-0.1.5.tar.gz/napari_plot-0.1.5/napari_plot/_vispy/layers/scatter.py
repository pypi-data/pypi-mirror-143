"""Scatter points layer"""
import typing as ty

import numpy as np
from napari._vispy.layers.base import VispyBaseLayer
from napari._vispy.utils.text import update_text

from ..visuals.scatter import ScatterVisual

if ty.TYPE_CHECKING:
    from ...layers import Scatter


MARKERS_MAIN = 0
MARKERS_HIGHLIGHT = 1
TEXT = 2


class VispyScatterLayer(VispyBaseLayer):
    """Line layer"""

    def __init__(self, layer: "Scatter"):
        node = ScatterVisual()
        super().__init__(layer, node)

        self.layer.events.size.connect(self._on_data_change)
        self.layer.events.edge_width.connect(self._on_data_change)
        self.layer.events.edge_width_is_relative.connect(self._on_data_change)
        self.layer.events.edge_color.connect(self._on_data_change)
        self.layer.events.face_color.connect(self._on_data_change)
        self.layer.events.symbol.connect(self._on_symbol_change)
        self.layer.events.scaling.connect(self._on_scaling_change)
        self.layer.text.events.connect(self._on_text_change)

        self.reset()
        self._on_data_change()

    def _on_scaling_change(self, event=None):
        """Set data"""
        self.node._subvisuals[MARKERS_MAIN].scaling = self.layer.scaling

    def _on_symbol_change(self, event=None):
        """Set data"""
        self.node._subvisuals[MARKERS_MAIN].symbol = self.layer.symbol

    def _on_data_change(self, event=None):
        """Set data"""
        if len(self.layer.data) > 0:
            edge_color = self.layer.edge_color
            face_color = self.layer.face_color
            edge_width = self.layer.edge_width
        else:
            edge_color = np.array([[0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
            face_color = np.array([[1.0, 1.0, 1.0, 1.0]], dtype=np.float32)
            edge_width = [0]

        if self.layer.edge_width_is_relative:
            edge_kw = {
                "edge_width": None,
                "edge_width_rel": edge_width,
            }
        else:
            edge_kw = {
                "edge_width": edge_width,
                "edge_width_rel": None,
            }

        self.node._subvisuals[MARKERS_MAIN].set_data(
            self.layer.data[:, ::-1], size=self.layer.size, edge_color=edge_color, face_color=face_color, **edge_kw
        )
        self.node._subvisuals[MARKERS_MAIN].scaling = self.layer.scaling
        self.node._subvisuals[MARKERS_MAIN].symbol = self.layer.symbol

        self._on_text_change(update_node=False)
        self.node.update()

    def _on_text_change(self, update_node=True):
        """Function to update the text node properties

        Parameters
        ----------
        update_node : bool
            If true, update the node after setting the properties
        """
        ndisplay = 2
        if self.layer._text.visible is False:
            text_coords = np.zeros((1, ndisplay))
            text = []
            anchor_x = "center"
            anchor_y = "center"
        else:
            text_coords, anchor_x, anchor_y = self.layer._view_text_coords
            if len(text_coords) == 0:
                text_coords = np.zeros((1, ndisplay))
            text = self.layer._view_text
        text_node = self.node._subvisuals[-1]

        update_text(
            text_values=text,
            coords=text_coords,
            anchor=(anchor_x, anchor_y),
            rotation=self.layer._text.rotation,
            color=self.layer._text.color,
            size=self.layer._text.size,
            ndisplay=ndisplay,
            text_node=text_node,
        )
        if update_node:
            self.node.update()
