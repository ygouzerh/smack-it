#! /usr/bin/env python3

"""
author : ygouzerh
date: 26/11/2018

API to manage roles
"""
from boto3 import client, resource
import boto3
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
            default_role_name = response['Role']['RoleName']
            client_iam = boto3.client('iam')
            client_iam.tag_role(
                RoleName=default_role_name,
                Tags=[Tagger.k8s_get_tag(), Tagger.project_get_tag()]
            )
            print("We have attached the role to the project")
            client('iam').attach_role_policy(
                RoleName=Role.get_default_role().role_name,
                PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess"
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
        client('iam').create_instance_profile(
            InstanceProfileName=config["INSTANCES"]["profile_name"]
        )
        print("We have created the default instance profile")
        #print("We have tag the instance profile")
        # instance_profile = Role.get_instance_profile()
        # print(instance_profile)
        # instance_profile_id = instance_profile.id
        # Tagger.attach_on_project(instance_profile_id)
        # Tagger.k8s_attach(instance_profile_id)
        Role.get_instance_profile().add_role(RoleName=config["INSTANCES"]["role_name"])
        print("We have added the default role to the defaut instance profile")

    @staticmethod
    def delete_instance_profile():
        """
            Delete the default instance profile.
            Check if exists.
            Warning : Deprecated, as it has unarbitrary behavior. Need to be better tested.
        """
        config = Parser.parse('instances.ini')
        instance_profile = Role.get_instance_profile()
        if instance_profile is not None:
            print("A default instance profile was already created, we need delete it...")
            if Role.get_default_role() is not None :
                for role in instance_profile.roles:
                    print(".....Detach role : ", role.name)
                    client('iam').remove_role_from_instance_profile(InstanceProfileName=config["INSTANCES"]["profile_name"],
                        RoleName=role.name)
                    print(".....Delete role : ", role.name)
                    print("Attached policies")
                    for policy in role.attached_policies.all():
                        print("Detach policy : ", policy)
                        role.detach_policy(
                            PolicyArn=policy.arn
                        )
                    for instance in role.instance_profiles.all():
                        print("INSTANCE PROFILE : ", instance)
                    client('iam').delete_role(RoleName=role.name)
                    print("...Role deleted")
            print("...Remove instance profile")
            client('iam').delete_instance_profile(InstanceProfileName=config["INSTANCES"]["profile_name"])
            print("...Default instance deleted")

    @staticmethod
    def delete_role(role_name):
        """
            Delete role and all ressources associated
        """
        role = Role.get_role(role_name)
        if role is not None :
            print("## Start deletion of : "+role_name+" ##")
            # Delete all instance profiles associated
            for instance_profile in role.instance_profiles.all():
                print("..Remove "+instance_profile.name)
                client('iam').remove_role_from_instance_profile(InstanceProfileName=instance_profile.name,
                    RoleName=role.name)
                # Delete recursively other instance profile's roles
                for instance_role in instance_profile.roles:
                    # Verify that we do not start the same process, as we could have consistency problems
                    if instance_role.name != role.name:
                        print("..Start the process of role deletion \
                                for instance profile : {} with role : {}".format(instance_profile.name, instance_role.name))
                        Role.delete_role(instance_role.name)
                # Delete instance profile
                print("..Delete instance : ", instance_profile.name)
                client('iam').delete_instance_profile(InstanceProfileName=instance_profile.name)
            # Delete policies associated
            for policy in role.attached_policies.all():
                print("..Detach policy : ", policy.arn)
                role.detach_policy(
                    PolicyArn=policy.arn
                )
                # The policy is not delete as it is AWS's managed policy
            # Delete the role
            print("..Deletion END")
            client('iam').delete_role(RoleName=role.name)
        else:
            print("No need to delete "+role_name+", because he no longer exist")

    @staticmethod
    def delete_default_role():
        """
            Delete the default role and all ressources associated
        """
        config = Parser.parse('instances.ini')
        Role.delete_role(config["INSTANCES"]["role_name"])

    @staticmethod
    def get_instance_profile():
        """
            Retrieve the instance profile
            TODO : passes a name in parameter
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
        print("Delete the instance profile and the associated roles")
        Role.delete_default_role()
