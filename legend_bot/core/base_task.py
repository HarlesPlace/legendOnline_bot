from abc import ABC, abstractmethod

class BaseTask(ABC):
    @abstractmethod
    def should_run(self) -> bool:
        """Decide se a tarefa deve ser executada agora."""
        pass

    @abstractmethod
    def run(self):
        """Executa a tarefa propriamente dita."""
        pass