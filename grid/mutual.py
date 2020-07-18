from collections import MutableMapping
from typing import Iterator, Any, Union, TypeVar

_KT = Any
_VT = Any
_T_co = TypeVar('_T_co')


class MutualDict(MutableMapping):
    """
    Both values are added as keys so as long as you have one you can access other
    """

    def __init__(self, map: dict = None):
        super(MutualDict, self).__init__()

        self._inner_dict: dict = {}

        # initialize with data
        if map is not None:
            for key, value in map.items():
                self.__setitem__(key, value)

    def __setitem__(self, k: _KT, v: _VT) -> None:
        self._inner_dict.__setitem__(k, v)
        self._inner_dict.__setitem__(v, k)

    def __delitem__(self, v: _VT) -> None:
        self._inner_dict.__delitem__(v)

    def __getitem__(self, k: _KT) -> Any:
        return self._inner_dict.__getitem__(k)

    def __len__(self) -> int:
        return self._inner_dict.__len__()

    def __iter__(self) -> Iterator[_T_co]:
        return self._inner_dict.__iter__()
