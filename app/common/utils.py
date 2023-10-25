import functools
import hashlib
import logging
import time
from typing import Any, Callable, Iterable, Optional

from factory.random import randgen

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_time_func(func: Callable):
    @functools.wraps(func)
    def wrapper_timer_func(*args, **kwargs):
        start_time = time.perf_counter()
        response = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"...............Finished {func.__name__!r} in {run_time:.4f} seg")
        return response

    return wrapper_timer_func


def hash_string(string: str) -> str:
    """Returns the hash of a string using SHA-256 algorithm."""
    encoded_string = string.encode("utf-8")
    return hashlib.sha256(encoded_string).hexdigest()


def random_choice(sequence: Iterable[Any]) -> Optional[Any]:
    """
    Picks an element from the sequence at random
    Returns None if the sequence is empty
    """
    if not sequence:
        return None
    return randgen.choice(list(sequence))
