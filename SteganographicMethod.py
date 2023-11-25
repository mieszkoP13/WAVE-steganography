from abc import abstractmethod, ABC

class SteganographicMethod(ABC):

    @abstractmethod
    def init_hide(self, inputFilePath: str):
        pass

    @abstractmethod
    def hide_data(self, string: str):
        pass

    @abstractmethod
    def init_extract(self, inputFilePath: str):
        pass

    @abstractmethod
    def extract_data(self):
        pass