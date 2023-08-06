# GeoLab

GeoLab is a pure Python library for geometric computing based on [NumPy](https://numpy.org/) arrays and [SciPy](https://www.scipy.org/) sparse matrices.
GeoLab provides a halfedge data structure for manifold and orientable meshes with arbitrary polygonal faces.
Moreover, GeoLab provides plotting functions and a GUI environment based on [MayaVi](https://docs.enthought.com/mayavi/mayavi/) and [TraitsUI](https://docs.enthought.com/traitsui/) for the development of custom 3D interactive applications.

GeoLab data structures are specifically designed for vectorized computing with NumPy and SciPy and for fast visualization with MayaVi.

GeoLab [code](https://github.com/DavidePellis/geolab) is open source.

## Installation

GeoLab requires [NumPy](https://numpy.org/), [SciPy](https://www.scipy.org/), [Matplotlib](https://matplotlib.org/), and [MayaVi](https://docs.enthought.com/mayavi/mayavi/) to run.


### Windows + Anaconda
An environment with all dependencies can be created as:
```sh
 conda create -n <env_name> -c anaconda mayavi scipy
 conda activate <env_name>
 pip install geolab
```

### MacOS
TODO


License
----

MIT

## Getting started
In Python, import GeoLab as
```sh
 import geolab as geo
```
### Open a mesh
To open an obj file, type
```sh
 v, f = geo.read_mesh('file_name.obj')
```
Here `v` is an array containing the coordinate of vertices and `f` the list of faces.
The halfedges can be built as
```sh
 h = geo.halfedges(f)
```
### Navigate halfedges
To get, for instance, the origin of halfedges, type
```sh
 origin = geo.navigate_halfedges(h, 'o')
```
The origin of the next halfedge can be get as
```sh
 next_origin = geo.navigate_halfedges(h, 'n-o')
```
while the face of the previous of the twin of the next halfedge as
```sh
 next_twin_previous_face = geo.navigate_halfedges(h, 'n-t-p-f')
```
and so on...

### Plot a mesh
A plotter can be initialized as
```sh
 plotter = geo.plotter()
```
To add the faces of a mesh to the plot type
```sh
 plotter.plot_faces(v, f)
```
and for edges type
```sh
 plotter.plot_edges(v, h)
```
Finally, to show the plot type
```sh
 plotter.show()
```





