from abc import abstractmethod, ABC

class SteganographicMethod(ABC):

    @abstractmethod
    def hide_data(self, string: str):
        pass

    @abstractmethod
    def extract_data(self):
        pass