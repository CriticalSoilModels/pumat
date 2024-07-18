from abc import ABC, abstractmethod

"""
Abstract class to serve as the base class for the possible load types in incremental driver.

Implement this in the future. 
"""

class Load(ABC):
    @abstractmethod
    def write_load(self, file):
        pass

    @abstractmethod
    def set_path(self, load_name, input_params):
        pass

