import logging


def setup_logging(
    logger: logging.Logger,
    log_to_file: bool = False,
    file_path: str = "yahoo_search.logs",
) -> None:
    """
    Sets up a logger to
    - Have a logging level (indicates the minimum level for a log to be shown)
    - Set the logging formatter
    - Setup the logger to log to a file

    If log_to_file is True, log to a file
    """
    # set the logger to only log stuff that is info and above
    logger.setLevel(logging.INFO)

    """
    setup the logging formatter
    to format the logs with time logged, name, 
    level of the message, and the message itself
    """
    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # in production, replace this with a filehandler -
    # a streamhandler prints the logs like a typical print()
    # we use a filehandler so the logs are sent into the file,
    # then the log management system reads from there
    if log_to_file:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = (
            logging.StreamHandler()
        )  # this receives the logs from the logger
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
