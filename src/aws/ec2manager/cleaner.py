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

from .read import ReaderRunning
from .terminate import Terminate

class Cleaner:
    """
        Check which instances are still
        running and delete them.
    """
    @classmethod
    def auto_terminate(cls):
        """
            Read all running instances,
            and delete them
        """
        # Get the ids of the ec2 running instances
        running_ids = ReaderRunning.ids()
        if len(running_ids) > 0:
            # Print the instances found
            print("Theses instances are running, we will terminate them : ")
            for running_id in running_ids:                
                print(running_id)
            # Terminate the instances
            Terminate.execute_multiple(ReaderRunning.ids())
            # Verify the termination
            if(len(ReaderRunning.ids()) == 0):
                print("Termination : success.")
            else:
                print("Termination : failure.")
        else:
            print("No running instances.")
