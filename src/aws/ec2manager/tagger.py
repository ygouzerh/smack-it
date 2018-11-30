#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Tag our resources
"""

from boto3 import resource
from ...utils.python.config_parser import Parser

class Tagger:
    """
        Manage tags
    """

    @staticmethod
    def tag(resource_id, key, value):
        """
            Simply tag a resource
        """
        resource('ec2').create_tags(Resources=[resource_id], Tags=[{'Key': key, 'Value': value}])

    @staticmethod
    def create_tag(key, value):
        """
            Return a tag
        """
        return {'Key': key, 'Value': value}

    @staticmethod
    def attach_on_project(resource_id):
        """
            Tag the resource to be associated
            with the project
        """
        config = Parser.parse('instances.ini')
        key = config['GENERAL']['project_name_key']
        value = config['GENERAL']['project_name_value']
        Tagger.tag(resource_id, key, value)
        Tagger.k8s_attach(resource_id)

    @staticmethod
    def get_project_filter():
        """
            Get the tag of the project store
            in the instances.ini files,
            and return the filter.
        """
        config = Parser.parse('instances.ini')
        return {'Name': 'tag:'+config['GENERAL']['project_name_key'], 'Values': [config['GENERAL']['project_name_value']]}

    @staticmethod
    def k8s_attach(resource_id):
        """
            Tag the resource with k8s
        """
        Tagger.tag(resource_id, "kubernetes.io/cluster/kubernetes", "owned")

    @staticmethod
    def k8s_get_tag():
        """
            Get the tag for k8s
        """
        return Tagger.create_tag("kubernetes.io/cluster/kubernetes", "owned")
