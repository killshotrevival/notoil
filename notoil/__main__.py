################################################### Python Import ##################################
"""
Main entry point for the notoil CLI application.

This module sets up the Click command group and registers subcommands.
"""

import click

################################################### Project Import #################################
# Import the ip_network command from the commands module.
from notoil.commands.network import ip_network

################################################### Main Declaration ###############################

@click.group()
def cli():
    """
    Main Click command group for the notoil CLI.
    """

cli.add_command(ip_network)
