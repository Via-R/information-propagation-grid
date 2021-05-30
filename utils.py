import json
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List, Dict, Union
from scipy.stats import truncnorm


def force_async(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Turn sync function to async function using threads."""

    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, args, *kwargs)
        return asyncio.wrap_future(future)

    return wrapper


def frange(start: float, stop: float, step: float):
    """Analog to 'range' but with float step and bounds."""

    while start < stop:
        yield start
        start += step


def print_json(obj: Union[Dict[Any, Any], List[Any]]) -> None:
    """Display a dictionary or a list with indent."""

    print(json.dumps(obj, default=str, indent=4))


def get_truncated_normal(mean: float = 0, sd: float = 1, low: float = 0, upp: float = 10) -> float:
    """Get variable with normal distribution in selected bounds."""

    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs()
