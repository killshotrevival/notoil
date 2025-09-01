################################################### Python Import ##################################

import click
from uuid import uuid4

from kubernetes import client, config
from kubernetes.client.api import core_v1_api

################################################### Project Import #################################

from .ssh import ssh_into_node
from .exec import exec_commands


################################################### Main Declaration ###############################


@click.group(name="pod", help="List of pod related commands")
def pod():
    """CLI group for pod-related commands in Kubernetes.
    
    This group provides various utilities for interacting with Kubernetes pods,
    including container ID extraction and root execution capabilities.
    """
    pass


@click.command(name="container-id", help="Extract container id of a pod")
@click.argument("name", type=click.STRING)
@click.option('--namespace', '-n', help="Namespace of the pod", type=click.STRING, default="default")
@click.option("--container-name", '-c', help="Name of the container in the pod", type=click.STRING, default="*")
def get_container_id(name: str, namespace: str="default", container_name: str = "*"):
    """Extract container ID from a specified pod.
    
    This function retrieves the container ID(s) from a Kubernetes pod. It can
    extract IDs for all containers in a pod or filter by a specific container name.
    
    Args:
        name (str): The name of the pod to query
        namespace (str, optional): The namespace where the pod is located. Defaults to "default"
        container_name (str, optional): The name of the specific container to query. 
                                      Use "*" to get all containers. Defaults to "*"
    
    Returns:
        None: Outputs container information to stdout
    """
    config.load_config()

    pod: client.V1Pod = client.CoreV1Api().read_namespaced_pod(name=name, namespace=namespace)

    if not pod:
        click.echo("No pod found")
        return
    
    for container in pod.status.container_statuses:
        if container_name in ["*", container.name]:
            click.echo(f"Name: {container.name} | {container.container_id.replace("containerd://", "")}")


@click.command(name="root-exec", help="Create command to execute into pod as root user")
@click.argument("pod", type=click.STRING)
@click.argument("container", type=click.STRING)
@click.option("--namespace", '-n', type=click.STRING, default="default")
def root_execute(pod: str, container: str, namespace: str = "default"):
    """Execute commands as root user in a specified pod container.
    
    This function creates a temporary node-shell pod to SSH into the Kubernetes node
    and execute commands as root user in the specified container. It automatically
    cleans up the temporary pod after execution.
    
    The process involves:
    1. Finding the node where the target pod is running
    2. Creating a temporary node-shell pod for SSH access
    3. Executing the root command in the target container
    4. Cleaning up the temporary pod
    
    Args:
        pod (str): The name of the target pod
        container (str): The name of the container within the pod
        namespace (str, optional): The namespace of the target pod. Defaults to "default"
    
    Returns:
        None: Executes commands and outputs results to stdout
    """
    config.load_config()

    pod: client.V1Pod = client.CoreV1Api().read_namespaced_pod(
        name=pod,
        namespace=namespace
    )

    if not pod:
        click.echo("No pod found")

    node_name = pod.spec.node_name

    click.echo(f"Node name: {node_name}")

    for cnt in pod.status.container_statuses:
        if container == cnt.name:
            c_id = cnt.container_id.replace("containerd://", "")
            click.echo(f"runc --root /run/containerd/runc/k8s.io/ exec -t -u 0 {c_id} bash")

            ssh_pod = ssh_into_node(node_name, pod_name=f"node-shell-{uuid4()}", namespace="kube-system")

            pod_name = ssh_pod.metadata.name

            print(f"POd started successfully with name -> {pod_name}, going to sleep")

            exec_commands(api_instance= core_v1_api.CoreV1Api(), pod_name=pod_name, namespace="kube-system")

            print("Sleep completed, killing the pod")
            

            client.CoreV1Api().delete_namespaced_pod(name=pod_name, namespace="kube-system")

            return

    click.echo("No container found with the given name")

pod.add_command(root_execute)
pod.add_command(get_container_id)