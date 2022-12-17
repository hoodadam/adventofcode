import itertools
from typing import Iterable, List, TypeVar

V = TypeVar("V")


def chunk(iterable: Iterable[V], chunk_size: int) -> Iterable[List[V]]:
    """
    Given an iterable and chunk_size, break up the input iterable into a
    generator of lists of items.  Each chunk is of length at most chunk_size.
    """
    grouped = itertools.groupby(enumerate(iterable), lambda v: v[0] // chunk_size)
    return ([elem for ix, elem in group] for i, group in grouped)
