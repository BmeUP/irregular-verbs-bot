from abc import ABC, abstractmethod


class IState(ABC):
    @abstractmethod
    def process_message(self):
        pass