"""
This module contains various command declarations for working with TOTP

"""
################################################### Python Import ##################################

import pyotp
import click

################################################### Project Import #################################
################################################### Main Declaration ###############################


@click.command(help="Generate a TOTP token")
@click.argument("secret", type=click.STRING)
def get_totp(secret):
    """
    Generate a TOTP token

    Args:
        secret (string): The secret key to use for the TOTP token
    """
    totp = pyotp.TOTP(secret)
    click.echo(totp.now())
