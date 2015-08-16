from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.interfaces import UNDEFINED


def suppress_msgs(checker, method_name, test_func, *msg_ids):

    def patched_add_message(self, msg_id, line=None, node=None, args=None,
                            confidence=UNDEFINED):
        if not (test_func(node) and msg_id in msg_ids):
            try:
                checker.linter.add_message(msg_id, line, node, args, confidence)
            except AttributeError:  # when checker is turned off
                pass

    old_method = getattr(checker, method_name)

    def patched_method(*args, **kwargs):
        old_add_message = checker.add_message
        checker.add_message = patched_add_message
        old_method(*args, **kwargs)
        checker.add_message = old_add_message

    setattr(checker, method_name, patched_method)


def is_meta_class(node):
    if 'meta' in node.name.lower():
        return True
    return False
