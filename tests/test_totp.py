################################################### Python Import ##################################

from pyotp import TOTP

################################################### Project Import #################################

from notoil.commands.totp import get_totp

from tests.setup import runner

################################################### Main Declaration ###############################

def test_get_totp():
    """
    Test the get_totp command
    """
    result = runner.invoke(get_totp, ["JQ3GCDISNYQBSKTW"])
    assert TOTP("JQ3GCDISNYQBSKTW").now() in result.output