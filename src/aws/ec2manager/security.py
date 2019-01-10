#! /usr/bin/env python3

"""
author : ygouzerh
date: 26/11/2018

API to manage security
"""
import boto3
import os
from pathlib import Path
from .tagger import Tagger
from ...utils.python.config_parser import Parser
import sh

class Security:
    """
        Manage ec2 security
    """

    # Path where we will store the keys
    ssh_path="ssh/"

    @staticmethod
    def create_key_pair(name):
        """
            Create the key pair for the instances
        """
        ec2 = boto3.client('ec2')
        response = ec2.create_key_pair(KeyName=name)
        path = Security.get_key_path(name)
        key_file = open(path,"w+")
        key_file.write(response["KeyMaterial"])
        key_file.close()
        print("Modify the right on the local key : ", path)
        sh.chmod("400", path)

    @staticmethod
    def create_default_key_pair():
        """
            Create default key pair
        """
        config = Parser.parse('instances.ini')
        key_name = config['INSTANCES']['key_name']
        Security.delete_key(key_name)
        Security.create_key_pair(key_name)

    @staticmethod
    def get_key_path(name):
        """
            Get the key path of a key
        """
        return Security.ssh_path+name

    @staticmethod
    def get_default_key_path():
        """
            Get the path of the default key
        """
        config = Parser.parse('instances.ini')
        key_name = config['INSTANCES']['key_name']
        return Security.get_key_path(key_name)

    @staticmethod
    def list_keys():
        """
            List the name of the keys
        """
        ec2 = boto3.client('ec2')
        response = ec2.describe_key_pairs()
        print("List of keys: ")
        for key in response["KeyPairs"]:
            print(key["KeyName"])

    @staticmethod
    def delete_key(name):
        """
            Delete a key on aws and on local
        """
        ec2 = boto3.client('ec2')
        # Delete the key on aws
        response = ec2.delete_key_pair(KeyName=name)
        print("Deleting the key {} on aws...done".format(name))
        # Delete the key in local
        key_path = Security.ssh_path+name
        if os.path.exists(key_path):
            os.remove(key_path)
            print("Deleting the key file in local...done")

    @staticmethod
    def create_default_security_group(vpc_id):
        """
            Create the defautl security group
            for the vpc of vpc_id
        """
        ec2 = boto3.client('ec2')
        try:
            config = Parser.parse('instances.ini')
            group_name = config["SECURITY"]["default_group_name"]
            description = "Security group by default"
            response = ec2.create_security_group(GroupName=group_name, Description=description, VpcId=vpc_id)
            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
            data = ec2.authorize_security_group_ingress(GroupId=security_group_id,
                # TODO TRANSFORM IN JSON
                IpPermissions=[
                    {'IpProtocol': -1, 'FromPort': 0, 'ToPort': 65635, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    # {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 0, 'ToPort': 65535, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 6443, 'ToPort': 6443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 2379, 'ToPort': 2380, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 10250, 'ToPort': 10250, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 10251, 'ToPort': 10251, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 30000, 'ToPort': 32767, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 10248, 'ToPort': 10248, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 53, 'ToPort': 53, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    # {'IpProtocol': 'tcp', 'FromPort': 10252, 'ToPort': 10252, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ]
            )
            # Attach on project
            Tagger.attach_on_project(security_group_id)
            print('Ingress Successfully Set %s' % data)
        except Exception as e:
            print(e)

    @staticmethod
    def get_security_group(name):
        """
            Get back the security group with her name
        """
        groups = boto3.client('ec2').describe_security_groups()['SecurityGroups']
        for group in groups:
            if group['GroupName'] == name:
                return boto3.resource('ec2').SecurityGroup(group['GroupId'])
        return None
