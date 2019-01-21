#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Start the installation
"""

import json
from time import sleep
from boto3 import resource, client
from ...utils.python.config_parser import Parser
from .security import Security
from .cleaner import Cleaner
from .tagger import Tagger
from .vpc import Vpc
from .subnet import Subnet
from .create import Creator
from .ssh import Ssh
from .deploy import Deployer
from .role import Role

class Installator:
    """
    Install the infrastructure
    """
    @staticmethod
    def run():
        print("Create key")
        config = Parser.parse('instances.ini')
        Security.create_default_key_pair()
        client_aws = client('ec2')
        resource_aws = resource('ec2')
        # Create the vpc
        print("Checks if vpc already exists")
        if Vpc.get_our_vpc() is not None:
            print("VPC already exists : need to clean")
            print(Cleaner.auto_terminate())
            if Security.get_security_group(config["SECURITY"]["default_group_name"]) is None:
                print("Need to create a securiy group")
                Security.create_default_security_group(Vpc.get_vpcs()[0]["VpcId"])
        else:
            print('Need to create a vpc')
            vpc = resource_aws.create_vpc(CidrBlock=config['VPC']['cidr_block'])
            Tagger.attach_on_project(vpc.id)
            # vpc_id = response["Vpc"]["VpcId"]
            #pc = Installator._get_vpcs()
            #vpc.create_tags(Tags=[{'Key': config['VPC']['tag_key'], 'Value': config['VPC']['tag_value']}])
            vpc.wait_until_available()
            print("Authorize the dns resolution")
            # Activate dns
            client_aws.modify_vpc_attribute(
                EnableDnsHostnames={
                    'Value': True
                },
                VpcId=vpc.id
            )
            client_aws.modify_vpc_attribute(
                EnableDnsSupport={
                    'Value': True
                },
                VpcId=vpc.id
            )
            # Create security group
            print('Create security group')
            Security.create_default_security_group(vpc.id)
            print("Create internet gateway")
            # Create then attach internet gateway
            gateway = resource_aws.create_internet_gateway()
            print(gateway.id)
            vpc.attach_internet_gateway(InternetGatewayId=(gateway.id))
            Tagger.attach_on_project(gateway.id)
            # Create route table
            print("Create route table")
            route_table = vpc.create_route_table()
            route_table.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=gateway.id
            )
            # Create subnet
            print("Create subnet")
            subnet = resource_aws.create_subnet(CidrBlock=config['SUBNETS']['cidr_block'], VpcId=vpc.id)
            route_table.associate_with_subnet(SubnetId=subnet.id)
            Tagger.attach_on_project(subnet.id)
        print("Reset role part config")
        # Init the role part : need some time to be take in account.
        Role.reset()
        sleep(60)
        Role.init()
        sleep(60)
        # Create the EC2
        print("Create ec2 master")
        Creator.execute("master", 1, 1)

        print("Create ec2 workers")
        Creator.execute("worker", int(config["INSTANCES"]["number"]), int(config["INSTANCES"]["number"]))
