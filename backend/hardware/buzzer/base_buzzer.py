from abc import ABC, abstractmethod #ABC or Abstract Base CLass is a blueprint that dictates what methods any subclass must have
#  If a developer creates a new buzzer class (e.g., RaspberryPiBuzzer) that inherits from BaseBuzzer but forgets to define one of these methods, Python will raise an error.

class BaseBuzzer(ABC):
    @abstractmethod
    def beep(self, times: int, duration: int, pause: float, frequency: int = None):
        pass

    @abstractmethod
    def beep_first_stage(self):
        pass

    @abstractmethod
    def beep_second_stage(self):
        pass

    @abstractmethod
    def beep_third_stage(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
