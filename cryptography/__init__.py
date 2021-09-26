"""
File Created: 25th September 2021
Author: Venkata Ravi K A
-----

"""

import sys, logging, time

# config for the root logger
logging.basicConfig(
    level=logging.NOTSET, format="%(levelname)s: %(name)s:%(funcName)s() - %(message)s"
)

# general purpose logging handler for modules in the application
stdout_logging_handler = logging.StreamHandler(sys.stdout)
stdout_logging_handler.setLevel(logging.DEBUG)
stdout_logging_formatter = logging.Formatter(
    "%(levelname)s: %(name)s:%(funcName)s() - %(message)s"
)
stdout_logging_handler.setFormatter(stdout_logging_formatter)

# timer logger
timer_logging_handler = logging.StreamHandler(sys.stdout)
timer_logging_handler.setLevel(logging.DEBUG)
timer_logging_formatter = logging.Formatter("%(name)s: %(message)s")
timer_logging_handler.setFormatter(timer_logging_formatter)
timer_logger = logging.getLogger("Timer")
timer_logger.addHandler(timer_logging_handler)
timer_logger.setLevel(logging.INFO)


class Timer:
    def __init__(self, timer_message=""):
        self.timer_message = timer_message

    def __enter__(self):
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        elapsed_time = time.perf_counter() - self._start_time
        timer_logger.info(
            f"{self.timer_message} elapsed time: {elapsed_time:0.4f} seconds"
        )
