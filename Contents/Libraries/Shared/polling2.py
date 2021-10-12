"""Polling2 module containing all exceptions and helpers used for the polling function

Never write another polling function again.

"""

__version__ = '0.4.6'

import logging
import time
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


LOGGER = logging.getLogger(__name__)


class PollingException(Exception):
    """Base exception that stores all return values of attempted polls"""
    def __init__(self, values, last=None):
        self.values = values
        self.last = last


class TimeoutException(PollingException):
    """Exception raised if polling function times out"""


class MaxCallException(PollingException):
    """Exception raised if maximum number of iterations is exceeded"""


def step_constant(step):
    """Use this function when you want the step to remain fixed in every iteration
    (typically good for instances when you know approximately how long the function should poll for)

    :param step: a number

    :return: step
    """
    return step


def step_linear_double(step):
    """Use this function when you want the step to double each iteration
    (e.g. like the way ArrayList works in Java).
    Note that this can result in very long poll times after a few iterations

    :param step: a number, that is doubled

    :return: double of step
    """
    return step * 2


def is_truthy(val):
    """Use this function to test if a return value is truthy

    :return: boolean
    """
    return bool(val)


def is_value(val):
    """Use this function to create a custom checker.

    :param val: Whatever val is, the checker checks that whatever is returned from that target is that value.

    :return: checker function testing if parameter is val, call checker to get a boolean
    """
    def checker(_val):
        return val is _val
    return checker


def log_value(check_success, level=logging.DEBUG):
    """A decorator for a check_success function that logs the return_value passed to check_success.

    :param level: (optional) the level at which to log the return value, defaults to debug. Must be
        one of the values in logging._levelNames (i.e. an int or a string).

    :return: decorator check_success function.
    """
    def wrap_check_success(return_val):
        LOGGER.log(level, "poll() calls check_success(%s)", return_val)
        return check_success(return_val)
    return wrap_check_success


def poll(target, step, args=(), kwargs=None, timeout=None, max_tries=None, check_success=is_truthy,
         step_function=step_constant, ignore_exceptions=(), poll_forever=False, collect_values=None,
         log=logging.NOTSET, log_error=logging.NOTSET):
    """Poll by calling a target function until a certain condition is met.

    You must specify at least a target function to be called and the step -- base wait time between each function call.

    :param step: Step defines the amount of time to wait (in seconds)

    :param args: Arguments to be passed to the target function

    :type kwargs: dict
    :param kwargs: Keyword arguments to be passed to the target function

    :param timeout: The target function will be called until the time elapsed is greater than the maximum timeout
        (in seconds). NOTE that the actual execution time of the function *can* exceed the time specified in the timeout.
        For instance, if the target function takes 10 seconds to execute and the timeout is 21 seconds, the polling
        function will take a total of 30 seconds (two iterations of the target --20s which is less than the timeout--21s,
        and a final iteration)

    :param max_tries: Maximum number of times the target function will be called before failing

    :param check_success: A callback function that accepts the return value of the target function. It should
        return true if you want the polling function to stop and return this value. It should return false if you want it
        to continue executing. The default is a callback that tests for truthiness (anything not False, 0, or empty
        collection).

    :param step_function: A callback function that accepts each iteration's "step." By default, this is constant,
        but you can also pass a function that will increase or decrease the step. As an example, you can increase the wait
        time between calling the target function by 10 seconds every iteration until the step is 100 seconds--at which
        point it should remain constant at 100 seconds

        >>> def my_step_function(step):
        >>>     step += 10
        >>>     return max(step, 100)

    :type ignore_exceptions: tuple
    :param ignore_exceptions: You can specify a tuple of exceptions that should be caught and ignored on every
        iteration. If the target function raises one of these exceptions, it will be caught and the exception
        instance will be pushed to the queue of values collected during polling. Any other exceptions raised will be
        raised as normal.

    :param poll_forever: If set to true, this function will retry until an exception is raised or the target's
        return value satisfies the check_success function. If this is not set, then a timeout or a max_tries must be set.

    :type collect_values: Queue
    :param collect_values: By default, polling will create a new Queue to store all of the target's return values.
        Optionally, you can specify your own queue to collect these values for access to it outside of function scope.

    :type log: int or str, one of logging._levelNames
    :param log: (optional) By default, return values passed to check_success are not logged. However, if this param is
        set to a log level greater than NOTSET, then the return values passed to check_success will be logged.
        This is done by using the decorator log_value.

    :type log_error: int or str, one of logging._levelNames
    :param log_level: (optional) If ignore_exception has been set, you might want to log the exceptions that are
        ignored. If the log_error level is greater than NOTSET, then any caught exceptions will be logged at that
        level. Note: the logger.exception() function is not used. That would print the stacktrace in the logs. Because
        you are ignoring these exceptions, it seems unlikely that'd you'd want a full stack trace for each exception.
        However, if you do what this, you can retrieve the exceptions using the collect_values parameter.

    :return: Polling will return first value from the target function that meets the condions of the check_success
        callback. By default, this will be the first value that is not None, 0, False, '', or an empty collection.

    Note: a message is written to polling2 logger when poll() is called. This logs a message like so:

        >>> Begin poll(target=<>, step=<>, timeout=<>, max_tries=<>, poll_forever=<>)

    This message should allow a user to work-out how long the poll could take, and thereby detect a hang in real-time
    if the poll takes longer than it should.
    """

    assert (timeout is not None or max_tries is not None) or poll_forever, \
        ('You did not specify a maximum number of tries or a timeout. Without either of these set, the polling '
         'function will poll forever. If this is the behavior you want, pass "poll_forever=True"')

    assert not ((timeout is not None or max_tries is not None) and poll_forever), \
        'You cannot specify both the option to poll_forever and max_tries/timeout.'

    kwargs = kwargs or dict()
    values = collect_values or Queue()

    timeout = time.time() + timeout if timeout else None
    tries = 0

    # Always log what polling is about to take place.
    msg = ("Begin poll(target=%s, step=%s, timeout=%s, max_tries=%s, poll_forever=%s)")
    LOGGER.debug(msg, target, step, timeout, max_tries, poll_forever)

    if log:
        check_success = log_value(check_success, level=log)

    last_item = None
    while True:

        if max_tries is not None and tries >= max_tries:
            raise MaxCallException(values, last_item)

        try:
            val = target(*args, **kwargs)
            last_item = val
        except ignore_exceptions as e:
            last_item = e

            if log_error: # NOTSET is 0, so it'll evaluate to False.
                LOGGER.log(log_error, "poll() ignored exception %r", e)

        else:
            # Condition passes, this is the only "successful" exit from the polling function
            if check_success(val):
                return val

        values.put(last_item)
        tries += 1

        # Check the max tries at this point so it will not sleep before raising the exception
        if max_tries is not None and tries >= max_tries:
            raise MaxCallException(values, last_item)

        # Check the time after to make sure the poll function is called at least once
        if timeout is not None and time.time() >= timeout:
            raise TimeoutException(values, last_item)

        time.sleep(step)
        step = step_function(step)
