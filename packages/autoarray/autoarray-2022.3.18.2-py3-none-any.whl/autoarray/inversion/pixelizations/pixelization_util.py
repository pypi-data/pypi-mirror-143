import numpy as np
import scipy.spatial
from typing import List, Tuple, Union

from autoarray import numba_util


@numba_util.jit()
def rectangular_neighbors_from(
    shape_native: Tuple[int, int]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the 4 (or less) adjacent neighbors of every pixel on a rectangular pixelization as an ndarray of shape
    [total_pixels, 4], called `pixel_neighbors`. This uses the uniformity of the rectangular grid's geometry to speed 
    up the computation.

    Entries with values of `-1` signify edge pixels which do not have neighbors. This function therefore also returns
    an ndarray with the number of neighbors of every pixel, `pixel_neighbors_sizes`, which is iterated over when using 
    the `pixel_neighbors` ndarray.

    Indexing is defined from the top-left corner rightwards and downwards, whereby the top-left pixel on the 2D array
    corresponds to index 0, the pixel to its right pixel 1, and so on.

    For example, on a 3x3 grid:

    - Pixel 0 is at the top-left and has two neighbors, the pixel to its right  (with index 1) and the pixel below
    it (with index 3). Therefore, the pixel_neighbors[0,:] = [1, 3, -1, -1] and pixel_neighbors_sizes[0] = 2.

    - Pixel 1 is at the top-middle and has three neighbors, to its left (index 0, right (index 2) and below it
    (index 4). Therefore, pixel_neighbors[1,:] = [0, 2, 4, -1] and pixel_neighbors_sizes[1] = 3.

    - For pixel 4, the central pixel, pixel_neighbors[4,:] = [1, 3, 5, 7] and pixel_neighbors_sizes[4] = 4.

    Parameters
    ----------
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.

    Returns
    -------
    The ndarrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """

    pixels = int(shape_native[0] * shape_native[1])

    pixel_neighbors = -1 * np.ones(shape=(pixels, 4))
    pixel_neighbors_sizes = np.zeros(pixels)

    pixel_neighbors, pixel_neighbors_sizes = rectangular_corner_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )
    pixel_neighbors, pixel_neighbors_sizes = rectangular_top_edge_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )
    pixel_neighbors, pixel_neighbors_sizes = rectangular_left_edge_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )
    pixel_neighbors, pixel_neighbors_sizes = rectangular_right_edge_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )
    pixel_neighbors, pixel_neighbors_sizes = rectangular_bottom_edge_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )
    pixel_neighbors, pixel_neighbors_sizes = rectangular_central_neighbors(
        pixel_neighbors=pixel_neighbors,
        pixel_neighbors_sizes=pixel_neighbors_sizes,
        shape_native=shape_native,
    )

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_corner_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are on the corners.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """

    pixels = int(shape_native[0] * shape_native[1])

    pixel_neighbors[0, 0:2] = np.array([1, shape_native[1]])
    pixel_neighbors_sizes[0] = 2

    pixel_neighbors[shape_native[1] - 1, 0:2] = np.array(
        [shape_native[1] - 2, shape_native[1] + shape_native[1] - 1]
    )
    pixel_neighbors_sizes[shape_native[1] - 1] = 2

    pixel_neighbors[pixels - shape_native[1], 0:2] = np.array(
        [pixels - shape_native[1] * 2, pixels - shape_native[1] + 1]
    )
    pixel_neighbors_sizes[pixels - shape_native[1]] = 2

    pixel_neighbors[pixels - 1, 0:2] = np.array(
        [pixels - shape_native[1] - 1, pixels - 2]
    )
    pixel_neighbors_sizes[pixels - 1] = 2

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_top_edge_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are on the top edge.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """
    for pix in range(1, shape_native[1] - 1):
        pixel_index = pix
        pixel_neighbors[pixel_index, 0:3] = np.array(
            [pixel_index - 1, pixel_index + 1, pixel_index + shape_native[1]]
        )
        pixel_neighbors_sizes[pixel_index] = 3

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_left_edge_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are on the left edge.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """
    for pix in range(1, shape_native[0] - 1):
        pixel_index = pix * shape_native[1]
        pixel_neighbors[pixel_index, 0:3] = np.array(
            [
                pixel_index - shape_native[1],
                pixel_index + 1,
                pixel_index + shape_native[1],
            ]
        )
        pixel_neighbors_sizes[pixel_index] = 3

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_right_edge_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are on the right edge.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """
    for pix in range(1, shape_native[0] - 1):
        pixel_index = pix * shape_native[1] + shape_native[1] - 1
        pixel_neighbors[pixel_index, 0:3] = np.array(
            [
                pixel_index - shape_native[1],
                pixel_index - 1,
                pixel_index + shape_native[1],
            ]
        )
        pixel_neighbors_sizes[pixel_index] = 3

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_bottom_edge_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are on the bottom edge.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """
    pixels = int(shape_native[0] * shape_native[1])

    for pix in range(1, shape_native[1] - 1):
        pixel_index = pixels - pix - 1
        pixel_neighbors[pixel_index, 0:3] = np.array(
            [pixel_index - shape_native[1], pixel_index - 1, pixel_index + 1]
        )
        pixel_neighbors_sizes[pixel_index] = 3

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def rectangular_central_neighbors(
    pixel_neighbors: np.ndarray,
    pixel_neighbors_sizes: np.ndarray,
    shape_native: Tuple[int, int],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the `pixel_neighbors` and `pixel_neighbors_sizes` arrays described in the function 
    `rectangular_neighbors_from()` for pixels on the rectangular pixelization that are in the centre and thus have 4
    adjacent neighbors.

    Parameters
    ----------
    pixel_neighbors
        An array of dimensions [total_pixels, 4] which provides the index of all neighbors of every pixel in
        the rectangular pixelization (entries of -1 correspond to no neighbor).
    pixel_neighbors_sizes
        An array of dimensions [total_pixels] which gives the number of neighbors of every pixel in the rectangular 
        pixelization.
    shape_native
        The shape of the rectangular 2D pixelization which pixels are defined on.
        
    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """
    for x in range(1, shape_native[0] - 1):
        for y in range(1, shape_native[1] - 1):
            pixel_index = x * shape_native[1] + y
            pixel_neighbors[pixel_index, 0:4] = np.array(
                [
                    pixel_index - shape_native[1],
                    pixel_index - 1,
                    pixel_index + 1,
                    pixel_index + shape_native[1],
                ]
            )
            pixel_neighbors_sizes[pixel_index] = 4

    return pixel_neighbors, pixel_neighbors_sizes


@numba_util.jit()
def delaunay_triangle_area_from(
    corner_0: Tuple[float, float],
    corner_1: Tuple[float, float],
    corner_2: Tuple[float, float],
) -> float:
    """
    Returns the area within a Delaunay triangle where the three corners are located at the (x,y) coordinates given by
    the inputs `corner_a` `corner_b` and `corner_c`.

    This function actually returns the area of any triangle, but the term `delaunay` is included in the title to
    separate it from the `rectangular` and `voronoi` methods in `pixelization_util.py`.

    Parameters
    ----------
    corner_0
        The (x,y) coordinates of the triangle's first corner.
    corner_1
        The (x,y) coordinates of the triangle's second corner.
    corner_2
        The (x,y) coordinates of the triangle's third corner.

    Returns
    -------
    The area of the triangle given the input (x,y) corners.
    """

    x1 = corner_0[0]
    y1 = corner_0[1]
    x2 = corner_1[0]
    y2 = corner_1[1]
    x3 = corner_2[0]
    y3 = corner_2[1]

    return 0.5 * np.abs(x1 * y2 + x2 * y3 + x3 * y1 - x2 * y1 - x3 * y2 - x1 * y3)


def delaunay_interpolated_array_from(
    shape_native: Tuple[int, int],
    interpolation_grid_slim: np.ndarray,
    pixel_values: np.ndarray,
    delaunay: scipy.spatial.Delaunay,
) -> np.ndarray:
    """
    Given a Delaunay triangulation and 1D values at the node of each Delaunay pixel (e.g. the connecting points where
    triangles meet), interpolate these values to a uniform 2D (y,x) grid.

    By mapping the delaunay's value to a regular grid this enables a source reconstruction of an inversion to be
    output to a .fits file.

    The `grid_interpolate_slim`, which gives the (y,x) coordinates the values are evaluated at for interpolation,
    need not be regular and can have undergone coordinate transforms (e.g. it can be the `source_pixelization_grid`)
    of a `Mapper`.

    The shape of `grid_interpolate_slim` therefore must be equal to `shape_native[0] * shape_native[1]`, but the (y,x)
    coordinates themselves do not need to be uniform.

    Parameters
    ----------
    shape_native
        The 2D (y,x) shape of the uniform grid the values are interpolated on too.
    interpolation_grid_slim
        A 1D grid of (y,x) coordinates where each interpolation is evaluated. The shape of this grid must be equal to
        shape_native[0] * shape_native[1], but it does not need to be uniform itself.
    pixel_values
        The values of the Delaunay nodes (e.g. the connecting points where triangles meet) which are interpolated
        to compute the value in each pixel on the `interpolated_grid`.
    delaunay
        A `scipy.spatial.Delaunay` object which contains all functionality describing the Delaunay triangulation.

    Returns
    -------
    The input values interpolated to the `grid_interpolate_slim` (y,x) coordintes given the Delaunay triangulation.

    """
    simplex_index_for_interpolate_index = delaunay.find_simplex(interpolation_grid_slim)

    simplices = delaunay.simplices
    pixel_points = delaunay.points

    interpolated_array = np.zeros(len(interpolation_grid_slim))

    for slim_index in range(len(interpolation_grid_slim)):

        simplex_index = simplex_index_for_interpolate_index[slim_index]
        interpolating_point = interpolation_grid_slim[slim_index]

        if simplex_index == -1:
            cloest_pixel_index = np.argmin(
                np.sum((pixel_points - interpolating_point) ** 2.0, axis=1)
            )
            interpolated_array[slim_index] = pixel_values[cloest_pixel_index]
        else:
            triangle_points = pixel_points[simplices[simplex_index]]
            triangle_values = pixel_values[simplices[simplex_index]]

            area_0 = delaunay_triangle_area_from(
                corner_0=triangle_points[1],
                corner_1=triangle_points[2],
                corner_2=interpolating_point,
            )
            area_1 = delaunay_triangle_area_from(
                corner_0=triangle_points[0],
                corner_1=triangle_points[2],
                corner_2=interpolating_point,
            )
            area_2 = delaunay_triangle_area_from(
                corner_0=triangle_points[0],
                corner_1=triangle_points[1],
                corner_2=interpolating_point,
            )
            norm = area_0 + area_1 + area_2

            weight_abc = np.array([area_0, area_1, area_2]) / norm

            interpolated_array[slim_index] = np.sum(weight_abc * triangle_values)

    return interpolated_array.reshape(shape_native)


@numba_util.jit()
def voronoi_neighbors_from(
    pixels: int, ridge_points: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the adjacent neighbors of every pixel on a Voronoi pixelization as an ndarray of shape
    [total_pixels, voronoi_pixel_with_max_neighbors], using the `ridge_points` output from the `scipy.spatial.Voronoi()`
    object.

    Entries with values of `-1` signify edge pixels which do not have neighbors. This function therefore also returns
    an ndarray with the number of neighbors of every pixel, `pixel_neighbors_sizes`, which is iterated over when using
    the `pixel_neighbors` ndarray.

    Indexing is defined in an arbritrary manner due to the irregular nature of a Voronoi pixelization.

    For example, if `pixel_neighbors[0,:] = [1, 5, 36, 2, -1, -1]`, this informs us that the first Voronoi pixel has
    4 neighbors which have indexes 1, 5, 36, 2. Correspondingly `pixel_neighbors_sizes[0] = 4`.

    Parameters
    ----------
    pixels
        The number of pixels on the Voronoi pixelization.
    ridge_points
        Contains the information on every Voronoi source pixel and its neighbors.

    Returns
    -------
    The arrays containing the 1D index of every pixel's neighbors and the number of neighbors that each pixel has.
    """

    pixel_neighbors_sizes = np.zeros(shape=(pixels))

    for ridge_index in range(ridge_points.shape[0]):
        pair0 = ridge_points[ridge_index, 0]
        pair1 = ridge_points[ridge_index, 1]
        pixel_neighbors_sizes[pair0] += 1
        pixel_neighbors_sizes[pair1] += 1

    pixel_neighbors_index = np.zeros(shape=(pixels))
    pixel_neighbors = -1 * np.ones(shape=(pixels, int(np.max(pixel_neighbors_sizes))))

    for ridge_index in range(ridge_points.shape[0]):
        pair0 = ridge_points[ridge_index, 0]
        pair1 = ridge_points[ridge_index, 1]
        pixel_neighbors[pair0, int(pixel_neighbors_index[pair0])] = pair1
        pixel_neighbors[pair1, int(pixel_neighbors_index[pair1])] = pair0
        pixel_neighbors_index[pair0] += 1
        pixel_neighbors_index[pair1] += 1

    return pixel_neighbors, pixel_neighbors_sizes


def voronoi_revised_from(
    voronoi: scipy.spatial.Voronoi
) -> Union[List[Tuple], np.ndarray]:
    """
    To plot a Voronoi pixelization using the `matplotlib.fill()` function a revised Voronoi pixelization must be
     computed, where 2D infinite voronoi regions are converted to finite 2D regions.

    This function returns a list of tuples containing the indices of the vertices of each revised Voronoi cell and
    a list of tuples containing the revised Voronoi vertex vertices.

    Parameters
    ----------
    voronoi
        The input Voronoi diagram that is being plotted.
    """

    if voronoi.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    region_list = []
    vertex_list = voronoi.vertices.tolist()

    center = voronoi.points.mean(axis=0)
    radius = voronoi.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(voronoi.ridge_points, voronoi.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(voronoi.point_region):
        vertices = voronoi.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            region_list.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = voronoi.points[p2] - voronoi.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # hyper

            midpoint = voronoi.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = voronoi.vertices[v2] + direction * radius

            region.append(len(vertex_list))
            vertex_list.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([vertex_list[v] for v in region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        region = np.array(region)[np.argsort(angles)]

        # finish
        region_list.append(region.tolist())

    return region_list, np.asarray(vertex_list)


def voronoi_nn_interpolated_array_from(
    shape_native: Tuple[int, int],
    interpolation_grid_slim: np.ndarray,
    pixel_values: np.ndarray,
    voronoi: scipy.spatial.Voronoi,
) -> np.ndarray:

    try:
        from autoarray.util.nn import nn_py
    except ImportError as e:
        raise ImportError(
            "In order to use the VoronoiNN pixelization you must install the "
            "Natural Neighbor Interpolation c package.\n\n"
            ""
            "See: https://github.com/Jammy2211/PyAutoArray/tree/master/autoarray/util/nn"
        ) from e

    pixel_points = voronoi.points

    interpolated_array = nn_py.natural_interpolation(
        pixel_points[:, 0],
        pixel_points[:, 1],
        pixel_values,
        interpolation_grid_slim[:, 1],
        interpolation_grid_slim[:, 0],
    )

    return interpolated_array.reshape(shape_native)
