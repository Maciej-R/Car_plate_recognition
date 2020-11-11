from Intermediary import Intermediary


class Backend:
    """
    Reads input data (format check, required conversions to provide data ready for further processing)
    Recognizes, counts and categorizes silhouettes on input video
    Prepares output video (with conversion to output format)
    Generates log data
    """

    def __init__(self, intermediary: Intermediary):
        """

        :param intermediary:
        """
        pass

    def read_data(self, pth: str):
        """
        Reads and if needed converts data
        :param pth: Path to input file
        :return:
        """

    def compute(self, n):
        """
        Run recognition, count and categorization process
        :param n: Number of threads to run in parallel
        :return: None
        """

    class Worker:
        """
        Job is scheduled to it
        """

        def __init__(self, Backend, start, end):
            """
            Saves needed information
            :param Backend: Reference providing access to needed data
            :param start: Time at which to start processing
            :param end: Time at which to end processing
            """
            pass

        def run(self):
            """
            Executes recognition algorithms
            :return:
            """
            pass
