"""
The pathfinding module can be used to find the shortest
path between two points in a graph.

To use the pathfinder for the default case:

>>> finder = pathfinder()
>>> finder( (0,0), (1,1) )
(2, [(0, 0), (1, 0), (1, 1)])

Or, to customize the pathfinder via passed in functions to handle for your
particular graph implementation:

>>> finder = pathfinder( distance=absolute_distance,        \\
...                      cost=fixed_cost(2),                \\
...                      neighbors=grid_neighbors(10,10) );
>>> finder( (0,0), (2,2) )
(8, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])

If a maximum cost is specified, then an empty path will be returned if
the cost exceeded the specified maximum

>>> finder( (0,0), (2,2), 7 )
(None, [])
"""

import math

def manhattan_distance( start, end ):
    """
    Calculate the manhattan distance between two points.
    >>> manhattan_distance( (0,0), (5,5) )
    10
    """
    return abs( start[ 0 ] - end[ 0 ] ) + abs( start[ 1 ] + end[ 1 ] )

def absolute_distance( start, end ):
    """
    Calculate the distance between two points using the distance formula.
    >>> absolute_distance( (1,2), (5,5) )
    5.0
    """
    return math.sqrt( ( start[0] - end[0] )**2 + ( start[1] - end[1] )**2 )

def fixed_cost( cost ):
    """
    Return a fixed cost for all coordinates in the graph.
    >>> cost = fixed_cost( 20 )
    >>> cost( (1, 2) )
    20
    >>> cost( (3, 4) )
    20
    """
    def func( coord ):
        return cost
    return func

def grid_neighbors( height, width ):
    """
    Calculate neighbors for a simple grid where
    a movement can be made up, down, left, or right.

    Arguments:
    height - The height of the grid
    width - The width of the grid

    >>> neighbor = grid_neighbors( 10, 10 )
    >>> neighbor( (0,0) )
    [(0, 1), (1, 0)]
    >>> neighbor( (1,1) )
    [(1, 2), (1, 0), (2, 1), (0, 1)]

    """
    def func( coord ):
        neighbor_list = [ ( coord[ 0 ], coord[ 1 ] + 1),
                          ( coord[ 0 ], coord[ 1 ] - 1),
                          ( coord[ 0 ] + 1, coord[ 1 ]),
                          ( coord[ 0 ] - 1, coord[ 1 ])]

        return [ c for c in neighbor_list
                 if c != coord
                 and c[0] >= 0 and c[0] < width
                 and c[1] >= 0 and c[1] < height ]
    
    return func

def pathfinder( neighbors=grid_neighbors( 100, 100 ),
                distance=absolute_distance,
                cost=fixed_cost( 1 ) ):
    """
    Find the shortest distance between two nodes in a graph using the 
    astar algorithm. By default, the graph is a coordinate plane where 
    every node has the same cost and nodes can be traversed horizontally 
    and vertically.

    Keyword Arguments:
    neighbor - Callable that takes a node and returns a list
               of neighboring nodes.
    distance - Callable that returns the estimated distance
               between two nodes.
    cost     - Callable that returns the cost to traverse
               a given node.
    """
    
    def reconstruct_path( came_from, current_node ):
        """Reconstruct the path from a given node to the beginning"""
        if current_node in came_from:
            p = reconstruct_path( came_from, came_from[ current_node ] )
            p.append( current_node )
            return p
        else:
            return [ current_node ]

    def func( start, end, max_cost=None ):
        """
        Perform a-star pathfinding from a start to an
        end coordinate.

        Returns a tuple containing the cost associated with
        the path, and a list of coordinates in the path

        This implementation is based on the wikipedia pseudocode, which
        translated almost directly into python.
        http://en.wikipedia.org/wiki/A*_search_algorithm
        """
        open_set = set( [ start ] )
        closed_set = set()
        came_from = {}

        g_score = { start : 0 }
        f_score = { start : cost( start ) }

        while len( open_set ) != 0:
            current = min( open_set, key=lambda c: f_score[c] )

            if max_cost != None and g_score[ current ] > max_cost:
                break

            if current == end:
                return g_score[ current ], reconstruct_path( came_from, end )

            open_set.discard( current )
            closed_set.add( current )
            for neighbor in neighbors( current ):

                tentative_score = g_score[ current ] + cost( current )

                if neighbor in closed_set and ( neighbor in g_score and tentative_score >= g_score[ neighbor ] ):
                    continue

                if neighbor not in closed_set or ( neighbor in g_score and tentative_score < g_score[ neighbor ] ):
                    came_from[ neighbor ] = current
                    g_score[ neighbor ] = tentative_score
                    f_score[ neighbor ] = tentative_score + distance( neighbor, end )
                    open_set.add( neighbor )

        return None, []
    
    return func

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
