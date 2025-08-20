from abc import ABC, abstractmethod

import numpy as np


class BaseCamera(ABC):
    @abstractmethod
    def get_capture(self) -> tuple[bool, np.ndarray]: #This is a type hint. It specifies that this method must return a tuple containing two elements: a boolean value (bool) and a NumPy array (np.ndarray)
        """
        Returns a tuple of (ret, frame) just like OpenCV,
        where `ret` is a boolean and `frame` is a numpy ndarray (or None).
        """
        pass

    @abstractmethod
    def release(self):
        """
        Optional clean-up method.
        """
        pass
