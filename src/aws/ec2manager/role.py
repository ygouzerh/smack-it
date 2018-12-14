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
        for role in client('iam').list_roles()['Roles']:
            if role['RoleName'] == name:
                return resource('iam').Role(name)
        return None

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
                Description='Give all access to all',
                AssumeRolePolicyDocument='{"Version": "2012-10-17","Statement": {"Effect": "Allow","Principal": { "Service" : "ec2.amazonaws.com" },"Action": "sts:AssumeRole"}}'
            )
            print("We have created the default role")
            client('iam').attach_role_policy(
                RoleName=Role.get_default_role().role_name,
                PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
            )
            print("We have attached the default role to the AdministratorAccess policy")
        else:
            print("The default role was already created")

    @staticmethod
    def create_instance_profile():
        """
            Create instance profile
        """
        config = Parser.parse('instances.ini')
        instance_profile = Role.get_instance_profile()
        if instance_profile is None:
            client('iam').create_instance_profile(
                InstanceProfileName=config["INSTANCES"]["profile_name"]
            )
            print("We have created the default instance profile")
            Role.get_instance_profile().add_role(RoleName=config["INSTANCES"]["role_name"])
            print("We have added the default role to the defaut instance profile")
        else:
            print("The default instance profile was already created")

    @staticmethod
    def get_instance_profile():
        """
            Retrieve the instance profile
        """
        config = Parser.parse('instances.ini')
        name = config["INSTANCES"]["profile_name"]
        for instance in client('iam').list_instance_profiles()['InstanceProfiles']:
            if instance['InstanceProfileName'] == name:
                return resource('iam').InstanceProfile(config["INSTANCES"]["profile_name"])
        return None

    @staticmethod
    def init():
        """
            Link a role and an instance profile
        """
        print("Start the creation of the default role")
        Role.create_default_role()
        print("Start the creation of the default instance profile")
        Role.create_instance_profile()

    @staticmethod
    def reset():
        """
            TODO
            Reset all the configuration.
        """
        pass
        print("Delete the instance profile")
        #Role.delete_instance_profile()
        print("Delete the default role")
        #Role.delete_role()

    @staticmethod
    def delete_instance_profile():
        """
            TODO
            Delete the default instance profile
        """
        config = Parser.parse('instances.ini')
        if Role.get_instance_profile() is not None:
            client('iam').delete_instance_profile(InstanceProfileName=config["INSTANCES"]["profile_name"])
            print("We have deleted the instance profile")

    @staticmethod
    def delete_role():
        """
            TODO
            Delete a role
        """
        config = Parser.parse('instances.ini')
        if Role.get_default_role() is not None:
            client('iam').delete_role(RoleName=config["INSTANCES"]["role_name"])
            print("We have deleted the default role")
