
from https://ssb22.user.srcf.net/css/eulerian.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/css/eulerian.html) just in case)

# Eulerian paths around polygons

If you have an $n$-sided convex polygon (with $n$ corners), how close can you get to tracing out *all* possible straight lines between corners (including the ones that cut across the middle of the polygon) without lifting the pen from the page and without going over any line twice?

The “handshake problem” tells us that the number of links in a strongly-connected network of $n$ nodes (which is the maximum possible number of lines we want to aim for) is the $n$<sup>th</sup> triangle number, i.e. $(n^2-n)/2$. The *degree* (number of links) of each vertex will be $n-1$ which is even if $n$ is odd. Since a **Eulerian circuit** exists when every vertex is even, it follows that **for odd-sided polygons, the complete path is possible**.

For even-sided polygons, you can at least make a Eulerian path (not a circuit) if you delete one connection from all but two of the corners. That will leave you with $n-2$ nodes of degree $n-2$ (which is even), and 2 nodes of degree $n-1$ (which is odd). These two nodes will be the starting and finishing points of the Eulerian path.

Since each removed link deprives *two* corners of a connection, the number of links you have to leave out (none of which are connected to each other) is $(n-2)/2 = (1/2)n-1$.

Or to put it another way, the number of links you *can* draw (connecting two corners each time) is 

$1/2 ((n-2)(n-2) + 2(n-1)) $

$ = 1/2 (n^2-4n+4 + 2n-2) $

$ = 1/2(n^2-2n+2) $

$ = (1/2)n^2-n+1 $

so the number left out is 

$ (n(n-1)/2) -(1/2)n^2+n-1$

$ = ((n^2 - n - n^2)/2)+n-1$

$ = n-n/2-1 = (1/2)n-1$

![eulerian.png](https://ssb22.user.srcf.net/css/eulerian.png)If you are trying to draw this, be careful: once you get to about $n=8$ it can be easy to “hem yourself in” by drawing the lines in the wrong order. To be safe, always go to one of the “least full” vertices. Or choose a direction (e.g. clockwise) and always go to the first one in that direction that is not yet linked from the current one (this will favour “around the edge” links over “across the middle” ones; as demonstrated by a [BBC Micro one-liner](https://ssb22.user.srcf.net/adjuster/twitter.html#eulerian), it results in line-crossings for all $n≥5$, and in regular polygons gives one bisection if and only if $n$ is even).

(You could also transform it into a Hamiltonian path problem by placing three new nodes along the length of each line and changing each polygon vertex into a dense web of edges linking the nearest nodes on each of its lines, but that’s inefficient and I wouldn’t recommend it for cryptographic purposes.)

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Any [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
