################################################### Python Import ##################################
"""
Main entry point for the notoil CLI application.

This module sets up the Click command group and registers subcommands.
"""

import click

################################################### Project Import #################################

from notoil.commands.network import ip_network
from notoil.commands.totp import get_totp

from notoil.commands.k8s.main import kubernetes_main

################################################### Main Declaration ###############################

@click.group()
def cli():
    """
    Main Click command group for the notoil CLI.
    """

cli.add_command(ip_network)
cli.add_command(get_totp)
cli.add_command(kubernetes_main)