import winsound #Liibrary for Windows OS
#It provides access to the basic sound-playing machinery of Windows, allowing you to play simple sounds like beeps.
from time import sleep #Used to create pauses in program's execution

from backend.hardware.buzzer.base_buzzer import BaseBuzzer #An import statement from a local project file that has ABC
from backend.utils.logging import logging_default #a pre-configured logging object to print status messages to the console or a file


class WindowsBuzzer(BaseBuzzer): # creates a new class named WindowsBuzzer. By inheriting from BaseBuzzer
    def __init__(self):
        self.setup()

    def setup(self) -> None:
        # In Windows, there are no special requirement whatsoever
        # We can directly use the `winsound` package provided by Python
        logging_default.info("Setting up Buzzer in Windows")
        logging_default.info("Triggering the first beep.")

        # Just gonna sound this to make sure everythings ok
        winsound.Beep(2000, 200) #Beep function from the winsound library to generate two quick beeps
        winsound.Beep(2000, 200) #First Argument is Frequency in Hertz (2000) and 2nd one is Duration in milliseconds (200)
    

    def beep(self, times : int, duration : int, pause : int, frequency: int = 1000): #core logic for making the buzzer beep. It accepts parameters for the number of beeps, duration, pause, and frequency. It provides a default frequency of 1000 Hz if none is specified.
        """
        Beeps the buzzer in a periodic way

        '''
            t0 ____ x _____ ..... tn
        '''

        x means the beep happen, and ____ is the pause
        For now, wether In windows or linux Raspberry Pi, 
        frequency will be hardcoded as there is no meaning to have the ability

        Parameters
        ----------
        times : int
            How many number of beeps will happen in a sequence
        duration : float
            Time buzzer will stays ON in each beep (in miliseconds)
        pause : float
            Pause between each beeps, this will decide wether it is slow or fast temp. In second
        """
        for _ in range(times): #for loop
            winsound.Beep(frequency, duration)
            sleep(pause)

    def beep_first_stage(self):
        """
        Stage 1: light drowsiness alert — slow beeps.
        """
        self.beep(1, 1000, 1)

    def beep_second_stage(self):
        """
        Stage 2: light drowsiness alert — medium beeps.
        """
        self.beep(1, 1000, 0.5)

    def beep_third_stage(self):
        """
        Stage 3: light drowsiness alert — fast beeps.
        """
        self.beep(1, 1000, 0.1)

    def cleanup(self):
        pass

    

    




