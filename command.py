import abc

class Command(abc.ABC):
    def __init__(self, usage: str):
        self.usage = usage

    @abc.abstractmethod
    async def command(self, img_path, **kwargs):
        pass
