class StreamError(Exception):
    """
        Exception raised for errors relating to the stream in sohmetrics.
    """

    # def __init__(self, message):
    #     self.message = message
    #     super().__init__(self.message)

    # def __str__(self):
    #     return f'{self.message}'


class MetricHandlerError(Exception):
    """
        Exception raised for errors in the metric handler.
    """

    # def __init__(self, message):
    #     self.message = message
    #     super().__init__(self.message)

    # def __str__(self):
    #     return f'{self.message}'


class GeneratePlotError(Exception):
    """
        Exception raised for errors in the generate plot.

    """

    # def __init__(self, message):
    #     self.message = message
    #     super().__init__(self.message)

    # def __str__(self):
    #     return f'{self.message}'
