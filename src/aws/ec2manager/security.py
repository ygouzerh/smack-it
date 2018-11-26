#! /usr/bin/env python3

"""
author : ygouzerh
date: 26/11/2018

API to manage security
"""
import boto3
import os
from pathlib import Path

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
        print(response)
        key_file = open(Security.ssh_path+name,"w+")
        key_file.write(response["KeyMaterial"])

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
