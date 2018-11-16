#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

API to delete our instances
automatically.
Warning : time between
creation and terminate to take in account.

# Todo : could stop them too : here are in each action ?
"""

from .read import ReaderNotTerminated
from .terminate import Terminate

class Cleaner:
    """
        Check which instances are still
        activated and delete them.
    """
    @classmethod
    def auto_terminate(cls):
        """
            Read all not terminated instances,
            and delete them
        """
        # Get the ids of the ec2 not_terminated instances
        not_terminated_ids = ReaderNotTerminated.ids()
        if len(not_terminated_ids) > 0:
            # Print the instances found
            print("Theses instances are not terminated, so we will terminate them : ")
            for not_terminated_id in not_terminated_ids:
                print(not_terminated_id)
            # Terminate the instances
            Terminate.execute_multiple(ReaderNotTerminated.ids())
            # Verify the termination
            if(len(ReaderNotTerminated.ids()) == 0):
                print("Termination order send to everybody : success.")
            else:
                print("Termination order send to everybody : failure.")
        else:
            print("No instances activated : Nothing to do.")
