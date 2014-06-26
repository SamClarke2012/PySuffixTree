PySuffixTree
============

A python implementation of a suffix tree object using Ukonnen's algorithm 
and it's optimisations.




Node 0

	Edge $ 0 suffix [9:9] connected to None 
	Edge a 2 suffix [0:2] connected to Node 1 Suffix linked to Node 2 ab
	Edge b 1 suffix [1:2] connected to Node 2 b
	Edge c 1 suffix [2:3] connected to Node 5 c
	Edge x 4 suffix [5:9] connected to None xabc


Node 1 Suffix linked to Node 2

	Edge c 1 suffix [2:3] connected to Node 3 Suffix linked to Node 4 Suffix linked to Node 5 c
	Edge x 4 suffix [5:9] connected to None xabc


Node 2

	Edge c 1 suffix [2:3] connected to Node 4 Suffix linked to Node 5 c
	Edge x 4 suffix [5:9] connected to None xabc


Node 3 Suffix linked to Node 4 Suffix linked to Node 5

	Edge $ 0 suffix [9:9] connected to None 
	Edge a 6 suffix [3:9] connected to None abxabc


Node 4 Suffix linked to Node 5

	Edge $ 0 suffix [9:9] connected to None 
	Edge a 6 suffix [3:9] connected to None abxabc


	
Node 5

	Edge $ 0 suffix [9:9] connected to None 
	Edge a 6 suffix [3:9] connected to None abxabc



[NODE 0]-------(ab)---------[NODE 1]----(c)-------[NODE 3]---($)
  |                             \                    \
  |                              \------(x)----X      \------(abxabc)
  |
  -------------(b)----------[NODE 2]----(c)-------[NODE 4]---($)
  |                              \                    \    
  |                               \-----(xabc)-X       \------(abxabc)
  |
  |------------(c)----------[NODE 5]----($)----X
  |                              \                        
  |                               \------(abxabc)
  |
  |------------(xabc)-------X
  |
  |
  |
  |------------($)----------X

