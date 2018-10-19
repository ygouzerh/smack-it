#!/usr/bin/env python3

"""
author : ygouzerh
date : 19/10/2018

Abstract class for the possible actions on ec2 instances
"""

from botocore.exceptions import ClientError

class ActionOnInstance:
    """
        Inner action to perform on ec2 instances
    """
    @classmethod
    def _concrete_action(cls, instance_ids, dry_run):
        raise NotImplementedError()

    @classmethod
    def execute_multiple(cls, instance_ids):
        """
            API for the user to execute the action
            on multiple ids.
            Need to pass a list in argument.
        """
        # Check the permission first
        if cls.verify_permission(instance_ids):
            # Indicate to the user if we have succeed are not the operation
            try:
                cls._concrete_action(instance_ids, False)            
                print("Operation succeed")
            except Exception as exception:
                print(exception)
                raise exception
        else:
            raise RuntimeError("You have no rights to perform this action")

    @classmethod
    def execute_one(cls, instance_id):
        """
            API for the user to execute the
            action on one id.
            WRAPPER of execute_multiple.
        """
        cls.execute_multiple([instance_id])

    @classmethod
    def verify_permission(cls, instance_ids):
        """
            Do a dryrun to verify the permissions.
            Return : True if we have the permission, false otherwise
        """
        try:
            cls._concrete_action(instance_ids, True)
        except ClientError as error:
            if 'DryRunOperation' not in str(error):
                print(error)
                return False
        return True
