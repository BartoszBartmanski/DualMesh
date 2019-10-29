#!/usr/bin/env python

import meshio
import numpy as np


def array_intersection(a, b):
    """Returns a boolean array of where b array's elements appear in the a array"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    if not isinstance(b, np.ndarray):
        b = np.array(b)
    tmp=np.prod(np.swapaxes(a[:,:,None],1,2)==b,axis=2)
    return np.sum(np.cumsum(tmp,axis=0)*tmp==1,axis=1).astype(bool)


def get_area(points):
    """Returns the area of a polygon given the vertices.

    Parameters:
        points:     numpy.ndarray
            Vertices of the polygon

    Warning: the points need to be ordered clockwise or anticlockwise."""

    # shift all the points by one
    shifted = np.roll(points, 1, axis=0)
    # Use the shoelace formula
    area = 0.5 * np.sum((shifted[:, 0] + points[:, 0])*(shifted[:, 1] - points[:, 1]))
    return np.abs(area)


def get_dual_points(mesh, index):
    """Returns the points of the dual mesh nearest to the point in the mesh given by the index.

    Parameters:
        mesh:       meshio._mesh.Mesh object
            Input mesh.

        index:      int
            Index of the point in the input mesh for which to calculate the nearest points of the dual mesh.

    """
    assert isinstance(mesh, meshio._mesh.Mesh)
    v1 = mesh.points[mesh.cells["vertex"][np.where(mesh.cells["vertex"] == index)[0]]].mean(axis=1)
    v2 = mesh.points[mesh.cells["line"][np.where(mesh.cells["line"] == index)[0]]].mean(axis=1)
    v3 = mesh.points[mesh.cells["triangle"][np.where(mesh.cells["triangle"] == index)[0]]].mean(axis=1)
    verts = np.concatenate((v1, v2, v3), axis=0)
    return verts


def get_dual(mesh, order=False):
    """Returns the dual mesh held in a dictionary with dual["points"] giving the coordinates and
    dual["cells"] giving the indicies of all the cells of the dual mesh.

    Parameters:
        mesh:       meshio._mesh.Mesh object
            Input mesh.

        order:      boolean
            Whether to reorder the indices of each cell, such that they are in anticlockwise order.
    """
    assert isinstance(mesh, meshio._mesh.Mesh)

    # Get the first set of points of the dual mesh
    new_points = get_dual_points(mesh, 0)

    # Create the dictionary that will hold the points of the mesh, as well as the indices
    dual = {"points": new_points, "cells": [np.arange(len(new_points)).tolist()]}

    for idx in range(1, len(mesh.points)):
        # Get the dual mesh points for a given mesh vertex
        new_points = get_dual_points(mesh, idx)

        # Find which of these new_points are already present in the dual["points"]
        inter = array_intersection(new_points, dual["points"])

        # Add new_points to the dual mesh points that are not already there
        dual["points"] = np.concatenate((dual["points"], new_points[~inter]))

        # Add the indices for the new cell to dual["cells"]
        inter = array_intersection(dual["points"], new_points)
        vert_idxs = np.where(inter)[0].tolist()

        if order:
            # Reorder the indices, such that points are anticlockwise
            verts = dual["points"][vert_idxs]
            c = verts.mean(axis=0)
            angles = np.arctan2(verts[:,1] - c[1], verts[:,0] - c[0])
            vert_idxs = np.array(vert_idxs)[np.argsort(angles)].tolist()

        dual["cells"].append(vert_idxs)

    return dual
