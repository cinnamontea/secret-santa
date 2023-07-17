"""
This module provides functions based on strong randomness using the `secrets` module.
"""

from secrets import choice



def shufflelist(l):
	"""
    Returns a random permutation of the elements of the given list.

    Arguments
    ---------
        l : list[Any] - List where the elements will be sampled from.
	
	Returns
	-------
        list[Any] - Resulting permutation.

    Examples
    --------
        shufflelist([1,2,3,4,5,6,7,8]) ==> [3, 7, 2, 1, 4, 8, 6, 5]
    """
	li = [*range(len(l))]
	sl=[]
	for _ in range(len(li)):
		i = choice(li)
		sl.append(l[i])
		li.remove(i)
	return sl