import sys

from abc import ABC, abstractmethod, ABCMeta

if sys.version_info < (3, 4, 0):
    class AI:
        __metaclass__ = ABCMeta

        @abstractmethod
        def getCurrentStateActionFromPolicy(self):
            pass

        @abstractmethod
        def updateCurrentState(self, player, keys, wormholes):
            pass
# else:
#     # Do 2.6+ stuff



