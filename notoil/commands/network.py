"""
This module contains various command declarations for working with networks

"""
################################################### Python Import ##################################

import ipaddress

import click

################################################### Project Import #################################
################################################### Main Declaration ###############################


@click.command(help="Check if an IP address is present inside a subnet or not")
@click.argument("ip", type=click.STRING)
@click.argument("net", type=click.STRING)
def ip_network(ip, net):
    """Can be used for checking if a IP string is present in a network or not

    Args:
        ip (string): IP address to test
        net (string): Network to test the IP against 
    """
    _ip = ipaddress.ip_address(ip)
    _network = ipaddress.ip_network(net)

    if _ip in _network:
        click.echo(f"{_ip} address is present in {_network} network")
    else:
        click.echo(f"{_ip} address is not present in {_network} network")
