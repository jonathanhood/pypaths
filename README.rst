PyPaths |buildstatus|
=====================

.. |buildstatus| image:: https://travis-ci.org/jonathanhood/pypaths.svg?branch=master
    :target: https://travis-ci.org/jonathanhood/pypaths
    
PyPaths is a small library useful for computing paths across simple in-memory graphs. Try it out by installing with pip::

  > pip install pypaths

Or, alternatively, install from source::

  > git clone https://github.com/jonathanhood/pypaths.git
  > cd pypaths
  > python setup.py install

For the simplest default case, usage is very simple:

.. sourcecode:: python

  from pypaths import astar
  
  finder = astar.pathfinder()
  
  print finder( (0,0), (2,2) )

We can also provide some parameters to help the algoriths understand your specific graph:

.. sourcecode:: python

  from pypaths import astar
  
  finder = astar.pathfinder( 
                    distance=my_distance_function,           # Calculate the absolute distance between two nodes
                    cost=my_cost_function,                   # Calculate the heuristic cost between nodes
                    neighbors=my_neighbors_function)         # Calculate the list of neighbors for a given node
  
  print finder( "MY NODE 1", "MY NODE 3" )

