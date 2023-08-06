"""Layer controls."""
import napari._qt.layer_controls.qt_layer_controls_container
from napari._qt.layer_controls.qt_layer_controls_container import QtLayerControlsContainer  # noqa

from ...layers import Centroids, InfLine, Line, MultiLine, Region, Scatter
from .qt_centroids_controls import QtCentroidControls
from .qt_infline_controls import QtInfLineControls
from .qt_line_controls import QtLineControls
from .qt_multiline_controls import QtMultiLineControls
from .qt_region_controls import QtRegionControls
from .qt_scatter_controls import QtScatterControls

layer_to_controls = {
    Line: QtLineControls,
    Centroids: QtCentroidControls,
    Scatter: QtScatterControls,
    Region: QtRegionControls,
    InfLine: QtInfLineControls,
    MultiLine: QtMultiLineControls,
}


# need to overwrite napari' default mapping of layer : control of layers to add our custom layers
napari._qt.layer_controls.qt_layer_controls_container.layer_to_controls.update(layer_to_controls)
