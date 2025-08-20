import os #Provides tools to interact with the OS, such as findoing out its name


def get_camera(): #figure out which camera class to use, create an instance of it, and return it
    if os.name == "posix": #checks the name attribute of the os module
        from backend.hardware.camera.rpi_camera import RPiCamera #If True then import RPICamera class
        return RPiCamera() #Creates insatcne of RPICamera class
    from backend.hardware.camera.cv_camera import CVCamera #It imports the CVCamera class
    return CVCamera()#Creates instacne of CVCamera

def get_buzzer():
    if os.name == "posix":
        from backend.hardware.buzzer.rpi_buzzer import RaspberryBuzzer#It imports the RaspberryBuzzer class
        return RaspberryBuzzer() #returns an instance of the RaspberryBuzzer class, which controls the physical GPIO pins
    from backend.hardware.buzzer.windows_buzzer import WindowsBuzzer
    return WindowsBuzzer() # imports and returns an instance of the WindowsBuzzer class, which uses the winsound library to make sounds through the computer's speakers
