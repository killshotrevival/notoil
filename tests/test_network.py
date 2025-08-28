################################################### Python Import ##################################

################################################### Project Import #################################

from notoil.commands.network import ip_network

from tests.setup import runner

################################################### Main Declaration ###############################

def test_ip_network_pass():
    result = runner.invoke(ip_network, ["19.205.73.132", "19.128.0.0/9"])
    assert "is present" in result.output

def test_ip_network_fail():
    result = runner.invoke(ip_network, ["19.205.73.132", "19.128.0.0/10"])
    assert "is not present" in result.output
