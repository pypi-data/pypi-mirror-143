import sys

from je_auto_control.utils.executor.action_executor import execute_action
from je_auto_control.utils.exception.exception_tag import macos_record_error
from je_auto_control.utils.exception.exceptions import AutoControlException
from je_auto_control.utils.exception.exceptions import AutoControlJsonActionException
from je_auto_control.wrapper.platform_wrapper import recorder


def record():
    """
    start record keyboard and mouse event until stop_record
    """
    if sys.platform == "darwin":
        raise AutoControlException(macos_record_error)
    return recorder.record()


def stop_record():
    """
    stop current record
    """
    if sys.platform == "darwin":
        raise AutoControlException(macos_record_error)
    action_queue = recorder.stop_record()
    if action_queue is None:
        raise AutoControlJsonActionException
    action_list = list(action_queue.queue)
    new_list = list()
    for action in action_list:
        if action[0] == "type_key":
            new_list.append([action[0], dict([["keycode", action[1]]])])
        else:
            new_list.append([action[0], dict(zip(["mouse_keycode", "x", "y"], [action[0], action[1], action[2]]))])
    return new_list

