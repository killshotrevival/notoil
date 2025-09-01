################################################### Python Import ##################################

import click

################################################### Project Import #################################

from .pod import pod


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
    pass

# Add pod subcommand to the kubernetes command group
kubernetes_main.add_command(pod)