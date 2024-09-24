**_REPO SUMMARY_**

This Repository was created to create an implementation using RustworkX Python Library to create, filter, and visualize a Graph.
This was also made with PyCharm.
____
**DISCLAIMER**

_rxGraspi_ file and both tests and _images_/_filtered_images_ directories are considered obsolete right now. The main file to run is _rxGraspiWebsite.py_, this file contains all the proper and necessary functions needed to create, filter, and visualize a graph. As well as finding the shortest path between the cathode node and all black nodes. The new outputted images from this file will not be outputted to the _graph_ directory and all the necessary test files are now in the _testCases_ directory. Future work will be done to remove these obsolete files but for now remain for further debugging strategies. 
Furthermore, this will mean that a new api description for the new _rxGraspiWebsite.py_ will be created in the future. But for now, all the functions described in the current _rxGraspi API_ still have the same goals so this is not necessary at the moment but will be changed in the near future.
______
**_REPO DIRECTORY INFORMATION_**

All main files are in the src directory including the rxGraspi.py file, which holds the code to creating, filtering, and visualizing graphs, as well as two additional directory's: testS, images, and filtered_images directory.
Add all tests in given test directory with proper formatting starting with the "x, y, z" dimensions in that order and format then a newline and fill graph based on Graspi documentation, follow link for more details: https://owodolab.github.io/graspi/inputFormats.html
Graph visualizations will go into images while their filtered counterparts will go into filtered_images.
______
***DOWNLOADS NEEDED***

You will need to download 2-3 packages
1. rustworkx package (used 15.1 version)
   
   _pip install rustoworkx_
   
3. graphviz
4. matplotlib
5. Also need to install pillow and pydot

According to rustworkx documentation, using Graphviz for graphs with a lot of nodes and matplotlib for smaller graphs is recommended. Our implementation has two functions for visualizing a graph but mainly works with graphviz, this is due to the fact we are working with bigger graphs.
______
***DOWNLOADS (ADVANCED)***

For a more in-depth representation of what packages were present during coding here is the output when running the terminal command "pip freeze":
* contourpy==1.3.0
* cycler==0.12.1
* fonttools==4.53.1
* graphviz==0.20.3
* kiwisolver==1.4.7
* matplotlib==3.9.2
* numpy==2.1.1
* packaging==24.1
* pillow==10.4.0
* pyparsing==3.1.4
* python-dateutil==2.9.0.post0
* rustworkx==0.15.1
* six==1.16.0
________
***_rxGraspi API_***

GLOBAL VARIABLES:
* graph: using the PyGraph class provided by rustworkx, nodes will be added to this variable to visualize a graph.
* filteredGraph: created to store the filtered original "graph" and be able to call it later on when looking for shortest paths.
* file_list: list of filenames which have already been established above it.
* image: list of image files to place graph visualizations
* filtered_images: list of image files to place filtered graph visualization

CLASSES:
Node: Custom class that stores node data:
* Label (node number/indice)
* Color
* X coordinate
* Y coordinate
* Z coordinate

Edge: Custom class that stores edge data:
* From node
* To node
* Weight

FUNCTIONS:

_createGraph(filename):_
* Takes in a string file name as a parameter which is used to read a file and graphs the nodes depending on the format of the file. Currently only allows for structured data Adds a node and edges between it and all its possible neighbors. 

_add_cathode_node(dimX, dimY, dimZ):_
* takes in dimension parameters given in file which should have already been initialized in the createGraph() function.
* Called at end of createGraph to add cathode node and connects it to bottom black layer.

_node_attr_fn(node):_
* Takes in a node class as a parameter.
* Makes a dictionary that adds attributes onto the nodes for graph visualization.
* Class is used as a parameter when visualizing graph using graphViz format. 

_visualizeGraphMPL(g):_
* Takes in a graph g
* Visualizes the graph using mpl_draw function given by the rustworkx package and matplotlib package

_visualizeGraphGV(g, file):_
* Takes in a graph g and a filename to store the filtered graph visualization.
* Visualizes graph using the graphviz_draw() format.
* Recommended by rustworkx documentation for graphs with a lot of nodes. 

_testGraphRuntime(filename, visualize, times):_
* Takes in a string filename, a boolean variable visualize that states if user wants a visual of graph, and an int variable of how many times it wishes the program to run.

_connectedComponents(edge):_
* Function used to filter edges by node color
* Required for built in graph filtering

_def filterGraph(g, visualize):_
* Filtering function that takes in the variable that allows for visualization or no visualization as well as a given graph and an image filename of where to output the visualization
* Uses connected components to get desired filtered edge list.which we use to make a tuple of nodes.
* uses this list of node tuples to create filtered graph with rustworkx built in function edge_subgraph().

_def testFilterGraph(g, filename, visualize, times, filteredFileName):_
* Takes in a graph, string filename, a boolean variable visualize that states if the user wants a visual of the graph after filtering, int variable times of how many times the user wishes the program to run, and an image extension name called filteredFileName of where to put the visualization

_def dfs_search(g, source):_
* Takes in graph as well as a source node to start a dfs search.
* outputs a list of all connected nodes found from source node while running dfs.

_def bfs_search(g, source):_
* Takes in graph as well as a source node to start a bfs search.
* outputs a list of all connected nodes found from source node while running bfs.

_def shortest_path_btwn_nodes(g, source ,target):_
* takes in 3 parameters, a graph, a source node, and a target node 
* uses dijkstra_shortest_path() function given by rustworkx in order to find the shortest path between the source node and the target node.
* outputs a dict with the nodes in order that will result in the shortest path if path exists. 

_def shortest_path_from_cathode(g, target):_
* does same thing as shotrest_path_btwn_nodes() but only takes in a target node to find the shortest path between cathode and target node.

_def run_all_three_functions(filename):_
* takes in a filename and runs multiple tests to figure out total runtime as well as memory usage of functions used to create, filter, and output shortest path of a graph.
* Does not visualize since some files can not visualize and produce an error due to Integer Overflow.

_def run_functions_w_visualization(filename, graphVisualFileName, filteredFileName):_
* runs testGraphRunTime(), testFilterGraph(), and shortest_path_from_cathode() functions for a given file and outputs both graph and filtered graph visualizations into given image file names.
