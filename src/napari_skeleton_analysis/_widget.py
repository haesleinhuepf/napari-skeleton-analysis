
import numpy as np
from napari_tools_menu import register_function

@register_function(menu="Segmentation post-processing > Skeletonize (scikit-image, n-skan)")
def skeletonize(binary_image:"napari.types.LabelsData") -> "napari.types.LabelsData":
    from skimage import morphology
    skeleton = morphology.skeletonize(binary_image)
    return skeleton


@register_function(menu="Segmentation post-processing > Skeleton image (n-skan)")
def skeleton_image(binary_image:"napari.types.LabelsData") -> "napari.types.LabelsData":
    skeleton = _image_to_skeleton(binary_image)
    return skeleton.skeleton_image


@register_function(menu="Segmentation post-processing > Skeleton path image (n-skan)")
def path_label_image(binary_image: "napari.types.LabelsData") -> "napari.types.LabelsData":
    skeleton = _image_to_skeleton(binary_image)
    return skeleton.path_label_image()


@register_function(menu="Measurement > Skeleton path length image (n-skan)")
def path_length_image(binary_image: "napari.types.LabelsData") -> "napari.types.ImageData":
    from napari_skimage_regionprops import relabel
    skeleton = _image_to_skeleton(binary_image)
    path_image = skeleton.path_label_image()
    path_lengths = skeleton.path_lengths()
    return relabel(path_image, path_lengths.tolist())


@register_function(menu="Measurement > Skeleton branch statistics (n-skan)")
def branch_statistics(binary_image: "napari.types.LabelsData", napari_viewer:"napari.Viewer" = None) -> "pandas.DataFrame":
    import skan
    skeleton = _image_to_skeleton(binary_image)
    results = skan.summarize(skeleton)

    if napari_viewer is not None:
        from napari_workflows._workflow import _get_layer_from_data
        labels_layer = _get_layer_from_data(napari_viewer, binary_image)
        # Store results in the properties dictionary:
        labels_layer.properties = results

        # turn table into a widget
        from napari_skimage_regionprops import add_table
        add_table(labels_layer, napari_viewer)
    else:
        import pandas
        return pandas.DataFrame(results)


@register_function(menu="Measurement > Skeleton branch lines (n-skan)")
def branch_lines(binary_image: "napari.types.LabelsData", edge_width: float = 0.1) -> "napari.types.LayerDataTuple":
    return _make_branch_lines(binary_image, edge_width, "plain")


@register_function(menu="Measurement > Skeleton branch type lines (n-skan)")
def branch_type_lines(binary_image: "napari.types.LabelsData",
                      edge_width: float = 0.1) -> "napari.types.LayerDataTuple":
    return _make_branch_lines(binary_image, edge_width, "branch_type")


@register_function(menu="Measurement > Skeleton degree image (n-skan)")
def degree_image(binary_image:"napari.types.LabelsData") -> "napari.types.ImageData":
    import skan
    return skan.csr.make_degree_image(binary_image)



branch_type_colors = [
    [0, 1, 0, 1],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 0.5, 0, 1],
]


def _make_branch_lines(binary_image: "napari.types.LabelsData", edge_width: float = 0.1,
                       line_color_type='plain') -> "napari.types.LayerDataTuple":
    stats = branch_statistics(binary_image)

    all_coords = []
    all_shape_type = []
    all_edge_width = []
    all_edge_colors = []

    is_3d = "image-coord-src-2" in stats.keys()
    for s in stats.index:
        if not is_3d:
            start = [stats["coord-src-0"][s], stats["coord-src-1"][s]]
            stop = [stats["coord-dst-0"][s], stats["coord-dst-1"][s]]
        else:
            start = [stats["coord-src-0"][s], stats["coord-src-1"][s], stats["coord-src-2"][s]]
            stop = [stats["coord-dst-0"][s], stats["coord-dst-1"][s], stats["coord-dst-2"][s]]

        coords = [start, stop]
        all_coords.append(coords)
        all_shape_type.append("line")
        all_edge_width.append(edge_width)

        if line_color_type == 'plain':
            all_edge_colors.append([1, 1, 1])
        elif line_color_type == 'branch_type':
            all_edge_colors.append(branch_type_colors[stats["branch-type"][s]])

    return (
    np.asarray(all_coords), {'shape_type': all_shape_type, 'edge_width': all_edge_width, 'edge_color': all_edge_colors},
    'shapes')


def _image_to_skeleton(skeleton_image:"napari.types.LabelsData") -> "skan.Skeleton":
    import skan
    return skan.Skeleton(skeleton_image)

