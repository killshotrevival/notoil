################################################### Python Import ##################################

from click.testing import CliRunner

################################################### Project Import #################################

from notoil.commands.network import ip_network

################################################### Main Declaration ###############################

runner = CliRunner()

def test_ip_network_pass():
    result = runner.invoke(ip_network, ["19.205.73.132", "19.128.0.0/9"])
    assert "is present" in result.output

def test_ip_network_fail():
    result = runner.invoke(ip_network, ["19.205.73.132", "19.128.0.0/10"])
    assert "is not present" in result.output
