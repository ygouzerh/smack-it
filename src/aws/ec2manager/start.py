#!/usr/bin/env python3

"""
author : ygouzerh
date : 19/10/2018

Start action.
"""

# Relative import
from .action import ActionOnInstance
from boto3 import client
from fire import Fire

class Start(ActionOnInstance):
    """
        Could be used to start instance
    """
    @classmethod
    def _concrete_action(cls, instances_ids, dry_run):
        """
            Inner action to start instances
        """
        client('ec2').start_instances(InstanceIds=instances_ids, DryRun=dry_run)