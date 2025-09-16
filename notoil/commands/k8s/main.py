################################################### Python Import ##################################

import click

################################################### Project Import #################################

from .pod import root_execute, create_network_pod, list_network_pod, delete_network_pod, match_pod


################################################### Main Declaration ###############################

@click.group(name="k8s", help="Kubernetes commands")
def kubernetes_main():
    """
    Kubernetes command group for managing Kubernetes resources and operations.
    
    This command group provides various subcommands for interacting with Kubernetes
    clusters, including pod management, network operations, and other k8s-related tasks.
    
    Examples:
        notoil k8s pod list          # List pods
        notoil k8s pod exec          # Execute commands in pods
        notoil k8s pod ssh           # SSH into pods
    """

kubernetes_main.add_command(root_execute)
kubernetes_main.add_command(create_network_pod)
kubernetes_main.add_command(list_network_pod)
kubernetes_main.add_command(delete_network_pod)
kubernetes_main.add_command(match_pod)
