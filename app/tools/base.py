from abc import ABC, abstractmethod

class Tool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def execute(
        self,
        **kwargs
    ):
        ...