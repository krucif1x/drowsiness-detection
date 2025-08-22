import threading

from backend.hardware.buzzer.base_buzzer import BaseBuzzer


class BuzzerService:
    def __init__(self, buzzer: BaseBuzzer):
        # Concrete buzzer implementation that exposes beep/cleanup/etc.
        self.buzzer = buzzer
        # Flag used by the background thread to keep running
        self.keep_beeping = False
        # The function that defines how the buzzer should behave in the loop
        self.buzzer_function = None
        # The background thread that runs the buzzer function
        self.buzzer_thread = None

    def beep_buzzer(self, times: int, duration: int, pause: float, frequency: int):
        """
        Trigger a finite sequence of beeps on the current thread.
        This is a synchronous helper that delegates to the buzzer implementation.
        """
        self.buzzer.beep(times, duration, pause, frequency)

    def start_buzzer(self, buzzer_function: callable):
        """
        Start or update the background buzzer loop with the provided function.

        - If no thread is running, create and start a daemon thread that will
          repeatedly call `buzzer_function()` until `stop_buzzer()` is called.
        - If a thread is already running:
          - If the new function differs from the current one, swap it in.
          - If it's the same function, do nothing (avoid restarting).
        """
        # If a background thread is already active...
        if self.buzzer_thread and self.buzzer_thread.is_alive():
            # ...and the requested function differs, update it in-place (hot-swap behavior)
            if self.buzzer_function != buzzer_function:
                self.buzzer_function = buzzer_function
            # Do not start another thread to avoid multiple concurrent loops
            return

        # No active thread: set the control flag and function
        self.keep_beeping = True
        self.buzzer_function = buzzer_function

        # Create a daemon thread so it won't block application shutdown
        self.buzzer_thread = threading.Thread(target=self._buzzer_loop, daemon=True)
        self.buzzer_thread.start()

    def stop_buzzer(self):
        """
        Stop the background buzzer loop and clean up hardware state.

        - Set `keep_beeping` to False so the loop exits gracefully.
        - Clear the function reference.
        - Call `buzzer.cleanup()` to reset/quiet the hardware.

        Note: We don't join the thread here; since it's a daemon, it will end when the loop exits.
              If you need deterministic shutdown, consider joining the thread.
        """
        self.keep_beeping = False
        self.buzzer_function = None
        # Optional: You could join the thread here to ensure the loop has fully stopped:
        # if self.buzzer_thread and self.buzzer_thread.is_alive():
        #     self.buzzer_thread.join(timeout=1.0)
        self.buzzer.cleanup()

    def test_buzzer(self):
        """
        Quick hardware check: run a predefined 'first stage' beep pattern.
        Useful for verifying wiring/hardware without starting the background loop.
        """
        self.buzzer.beep_first_stage()

    def _buzzer_loop(self):
        """
        Background worker loop.

        Repeatedly calls the current `buzzer_function` while:
        - `keep_beeping` is True, and
        - `buzzer_function` is not None.

        This allows hot-swapping the function while the thread is running
        (by assigning a new callable to `self.buzzer_function`).
        """
        # Loop until stop_buzzer() flips the flag or clears the function
        while self.keep_beeping and self.buzzer_function:
            # Execute the buzzer behavior (should be short or cooperative)
            # Consider adding small sleeps inside the function or here to avoid tight loops.
            self.buzzer_function()
