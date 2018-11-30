#! /usr/bin/env python3

"""
author : ygouzerh
date: 26/11/2018

API to manage roles
"""
from boto3 import client, resource
import json
from .tagger import Tagger
from ...utils.python.config_parser import Parser

class Role:
    """
        Manage roles
    """

    @staticmethod
    def get_role(name):
        """
            Retrieve a role
        """
        return resource('iam').Role('name')

    @staticmethod
    def get_default_role():
        """
            Retrieve the default role
        """
        config = Parser.parse('instances.ini')
        return Role.get_role(config["INSTANCES"]["role_name"])

    @staticmethod
    def create_default_role():
        """
            Create default role
        """
        config = Parser.parse('instances.ini')
        if Role.get_default_role() is None :
            response = client('iam').create_role(
                RoleName=config["INSTANCES"]["role_name"],
                Description='Give all access to all'
            )
            client.attach_role_policy(
                RoleName=Role.get_default_role().role_name,
                PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
            )

    @staticmethod
    def verify_instance_profile_exists():
        """
            Verify that the instance profile exists
        """
        response = client('iam').list_instance_profiles()
        config = Parser.parse('instances.ini')
        for instance_profile in response['InstanceProfiles']:
            if instance_profile["InstanceProfileName"] == config["INSTANCES"]["profile_name"]:
                return True
        return False

    @staticmethod
    def create_instance_profile():
        """
            Create instance profile
        """
        Role.create_default_role()
        config = Parser.parse('instances.ini')
        if not Role.verify_instance_profile_exists():
            client('iam').create_instance_profile(
                InstanceProfileName=config["INSTANCES"]["profile_name"]
            )
            Role.get_instance_profile().add_role(RoleName=config["INSTANCES"]["role_name"])

    @staticmethod
    def get_instance_profile():
        """
            Retrieve the instance profile
        """
        config = Parser.parse('instances.ini')
        return resource('iam').InstanceProfile(config["INSTANCES"]["profile_name"])
