from UI import UI


class Intermediary:
    """
    Provides interface with functions handling GUI events. Manages communication between UI and Backend.
    When it's necessary synchronizes actions. Controls program execution
    """

    def __init__(self, gui: UI):
        """
        Prepares required resources
        :arg gui: Reference to UI class that allows to send updates, interact with UI
        """

    #________________________ Handlers ________________________
    # Section of handlers for GUI events
    # Name format handle_<event>

    def handle_xxx(self):
        """

        :return:
        """
