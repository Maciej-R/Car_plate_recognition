

class UI:
    """
     Class initialized and prepares user's interface so that it's fully operational before forwarding processing to
     other parts of program.
     Provides functions to interact with user (displaying information, updating GUI, etc.)
     Program operates serving manually made user's requests so there's no need for and kind of pre-processing or
     initialization so UI is entry point to whole program and it starts first.
    """

    def __init__(self, pth: str) -> None:
        """
        Loads required data and configuration for GUI, binds appropriate listeners from Intermediary class to GUI
        elements, initializes it to be displayed.
        :arg pth: Path to GUI definition file
        :type pth: String
        :raises RuntimeError: When configuration file has wrong format
        :raises FileNotFoundError: When provided file points to file that does not exists
        :return: None
        """
        pass

    def add_listeners(self) -> None:
        """
        Called upon initialization of GUI to bind all required listeners
        :raises NotImplementedError: When function attempts to bind GUI element's listener to nonexistent function
        :return: None
        """
        pass

    def results_ready_notify(self):
        """
        Display information about completed process to user and allow him to open output file in player
        :return:
        """