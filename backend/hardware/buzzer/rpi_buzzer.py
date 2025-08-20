from time import sleep #Sleep function that pauses the execution of the program for a specified number of seconds

from gpiozero import Buzzer, Device # Imports Buzzer and Device classes from gpiozero library which is library for controlling GPIO pins of Raspi
from gpiozero.pins.lgpio import LGPIOFactory #Specific driver that tells gpiozero how to communicate with GPIO hardware

from backend.hardware.buzzer.base_buzzer import BaseBuzzer #It imports the BaseBuzzer class from a local file within the project.
from backend.utils.logging import logging_default #a pre-configured logging object that is used to print informative messages to the console for debugging

# Set the pin factory for Raspberry Pi 5 compatibility
Device.pin_factory = LGPIOFactory() # sets up the gpiozero library for the specific hardware being used

class RaspberryBuzzer(BaseBuzzer): #It creates a new class named RaspberryBuzzer. The (BaseBuzzer) part means it inherits from BaseBuzzer.
    def __init__(self, pin: int = 23): #The constructor method for the class
        #self: A reference to the specific object instance being created.
        #pin: int = 23: Defines a parameter named pin. The : int is a type hint suggesting it should be an integer 23.
        self.pin = pin 
        self.buzzer = Buzzer(self.pin) 
        logging_default.info("Setting up Buzzer on Raspberry Pi 5 using lgpio")


    def beep(self, times: int, duration: int, pause: float, frequency: int = None):
        for _ in range(times): #for loop
            self.buzzer.on()
            sleep(duration / 1000.0)
            self.buzzer.off()
            sleep(pause)

    def beep_first_stage(self):
        self.beep(1, 1000, 1) # beep 1 time for 1000 ms with a 1 second pause.

    def beep_second_stage(self):
        self.beep(1, 1000, 0.5) # beep 1 time for 1000 ms with a 0.5 second pause.

    def beep_third_stage(self):
        self.beep(1, 1000, 0.1) #beep 1 time for 1000 ms with a 0.1 second pause.

    def cleanup(self):
        self.buzzer.off()
