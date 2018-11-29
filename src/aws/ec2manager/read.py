#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

API to read our instances in many ways.
"""

from boto3 import resource
from fire import Fire
from ...utils.python.config_parser import Parser
from .tagger import Tagger

class Reader:
    """
    Startegy Design Pattern
    Get informations on our ec2 instances in many differents ways.
    """

    @classmethod
    def instances(cls):
        """
            Return a filtered list of our instances
        """
        raise NotImplementedError

    @classmethod
    def ids(cls):
        """
            Return the id of the filtered instances
        """
        return [instance.id for instance in cls.instances()]

    @classmethod
    def public_ips(cls):
        """
            Return the public ips of our instances
        """
        return [instance.public_ip_address for instance in cls.instances()]

    @classmethod
    def private_ips(cls):
        """
            Return the private ips of our instances
        """
        return [instance.private_ip_address for instance in cls.instances()]

class ReaderAll(Reader):
    """
        Get all the instances
    """

    @classmethod
    def instances(cls):
        """
            Return all the instances
        """
        return resource('ec2').instances.filter(Filters=[Tagger.get_project_filter()])

class ReaderRunning(Reader):
    """
        Get the running instances
    """

    @classmethod
    def instances(cls):
        """
            Return the running instances
        """
        return resource('ec2').instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}, Tagger.get_project_filter()])

class ReaderNotTerminated(Reader):
    """
        Get the instances which are not terminated
    """

    @classmethod
    def instances(cls):
        """
            Return the running instances
        """
        return resource('ec2').instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ["pending", \
                                                        "running", "stopping", "stopped"]}, Tagger.get_project_filter()])

class ReaderCli:
    """
        Return each strategy to be used in the CLI
    """
    @staticmethod
    def all():
        """
            All instances
        """
        return ReaderAll

    @staticmethod
    def running():
        """
            Running instances
        """
        return ReaderRunning

    @staticmethod
    def not_terminated():
        """
            Not terminated instances
        """
        return ReaderNotTerminated
