#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Start the installation
"""

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

class Installator:
    """
    Install the infrastructure
    """
    @staticmethod
    def run():
        Deployer.deploy()
        _ = input()
        print("Create key")
        config = Parser.parse('instances.ini')
        Security.create_default_key_pair()
        print("Create vpc")
        print("Checks if vpc already exists")
        client_aws = client('ec2')
        resource_aws = resource('ec2')
        print(Security.get_security_group("DEFAULT_SECURITY_GROUP"))
        if Vpc.get_our_vpc() is not None:
            print("VPC already exists : need to clean")
            print(Cleaner.auto_terminate())
        else:
            print('Need to create a vpc')
            vpc = resource_aws.create_vpc(CidrBlock=config['VPC']['cidr_block'])
            Tagger.attach_on_project(vpc.id)
            # vpc_id = response["Vpc"]["VpcId"]
            #pc = Installator._get_vpcs()
            #vpc.create_tags(Tags=[{'Key': config['VPC']['tag_key'], 'Value': config['VPC']['tag_value']}])
            vpc.wait_until_available()
            print('Create security group')
            Security.create_default_security_group(vpc.id)
            print("Create internet gateway")
            # create then attach internet gateway
            gateway = resource_aws.create_internet_gateway()
            print(gateway.id)
            vpc.attach_internet_gateway(InternetGatewayId=(gateway.id))
            Tagger.attach_on_project(gateway.id)
            print("Create route table")
            route_table = vpc.create_route_table()
            route = route_table.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=gateway.id
            )
            print("Create subnet")
            subnet = resource_aws.create_subnet(CidrBlock=config['SUBNETS']['cidr_block'], VpcId=vpc.id)
            route_table.associate_with_subnet(SubnetId=subnet.id)
            Tagger.attach_on_project(subnet.id)
        print("Create ec2")
        Creator.execute(int(config["INSTANCES"]["number"]), int(config["INSTANCES"]["number"]))
        print("Provisionning ec2 in ssh")
        Deployer.deploy()
