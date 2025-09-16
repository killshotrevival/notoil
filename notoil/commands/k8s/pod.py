################################################### Python Import ##################################

import subprocess
from time import sleep
from uuid import uuid4

import click

from kubernetes import client, config

################################################### Project Import #################################

from notoil.utils.generate import generate_random_string

from .ssh import ssh_into_node

################################################### Main Declaration ###############################

def root_execute_in_container(cnt: client.V1ContainerStatus, node_name: str, shell: str = "bash"):
    """Execute commands as root user in a specified pod container.
    
    This function creates a temporary node-shell pod to SSH into the Kubernetes node
    and execute commands as root user in the specified container. It automatically
    cleans up the temporary pod after execution.
    Args:
        cnt (client.V1ContainerStatus): The container status object
        node_name (str): The name of the node where the container is running
        shell (str, optional): The shell to use for the command. Defaults to "bash"

    Returns:
        None: Executes commands and outputs results to stdout
    """
    c_id = cnt.container_id.replace("containerd://", "")

    command = f"runc --root /run/containerd/runc/k8s.io/ exec -t -u 0 {c_id} {shell}"
    click.echo(f"{command}")

    ssh_pod = ssh_into_node(node_name, pod_name=f"node-shell-{uuid4()}", namespace="kube-system")

    pod_name = ssh_pod.metadata.name

    print(f"POd started successfully with name -> {pod_name}, sleeping for some time so that ssh pod can stabalize")
    sleep(2)

    subprocess.call(["kubectl", "exec", "-it", pod_name, "-n", "kube-system", "--", "bash", "-c", command])

    print("Root execute completed, killing the pod")

    client.CoreV1Api().delete_namespaced_pod(name=pod_name, namespace="kube-system", propagation_policy="Foreground",)



@click.command(name="re", help="Create command to execute into pod as root user")
@click.argument("pod", type=click.STRING)
@click.option("--container", '-c', type=click.STRING, default="first-container", \
              help="Name of the container to execute the command in, if not provided, the command will be executed in the first container")
@click.option("--namespace", '-n', type=click.STRING, default="default", help="Namespace of the pod")
@click.option("--shell", "-s", type=click.STRING, default="bash", help="Shell to use for the command")
def root_execute(pod: str, container: str, namespace: str = "default", shell: str = "bash"):
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
        container (str): The name of the container within the pod, if not provided, the command will be executed in the first container
        namespace (str, optional): The namespace of the target pod. Defaults to "default"
        shell (str, optional): The shell to use for the command. Defaults to "bash"
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
        return

    node_name = pod.spec.node_name

    click.echo(f"Node name: {node_name}")

    if container == "first-container":
        root_execute_in_container(pod.status.container_statuses[0], node_name, shell)
        return

    for cnt in pod.status.container_statuses:
        if container == cnt.name:
            root_execute_in_container(cnt, node_name, shell)
            return

    click.echo("No container found with the given name")


@click.command(name="cnp", help="Create a network pod")
@click.option("--namespace", "-n", type=click.STRING, default="default")
def create_network_pod(namespace: str = "default"):
    """
    Create a network pod

    Args:
        namespace (str, optional): The namespace where the pod will be created. Defaults to "default"

    Returns:
        None: Creates a network pod
    """
    config.load_config()

    pod = client.CoreV1Api().create_namespaced_pod(
        namespace=namespace,
        body=client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(
            name=f"network-{generate_random_string(5)}",
            namespace=namespace,
            labels={
                "network-pod": "true"
            }
        ),
        spec=client.V1PodSpec(
            containers=[client.V1Container(
                name="network",
                image="jonlabelle/network-tools",
                command=["sleep", "infinity"]
            )]
        ),
    )
    )

    click.echo(f"Network pod created successfully in namespace {namespace}. Use the below command to connect to the pod")
    click.echo(f"kubectl exec -it {pod.metadata.name} -n {namespace} -- bash")


@click.command(name="lnp", help="List all network pods in a namespace")
@click.option("--namespace", "-n", type=click.STRING, default="default")
def list_network_pod(namespace: str = "default"):
    """
    List all network pods in a namespace
    """
    config.load_config()
    pods = client.CoreV1Api().list_namespaced_pod(namespace=namespace, label_selector="network-pod=true")

    for pod in pods.items:
        click.echo(f"Pod name: {pod.metadata.name} | Pod namespace: {pod.metadata.namespace} | Pod status: {pod.status.phase}")


@click.command(name="dnp", help="Delete a network pod")
@click.option("--name", "-i", type=click.STRING, default="*")
@click.option("--namespace", "-n", type=click.STRING, default="default")
def delete_network_pod(name: str, namespace: str = "default"):
    """
    Delete a network pod

    Args:
        name (str): The name of the pod to delete
        namespace (str, optional): The namespace of the pod. Defaults to "default"

    Returns:
        None: Deletes a network pod
    """
    config.load_config()
    pods = client.CoreV1Api().list_namespaced_pod(namespace=namespace, label_selector="network-pod=true")

    for pod in pods.items:
        if name in ("*", pod.metadata.name):
            click.echo(f"Deleting pod {pod.metadata.name} in namespace {namespace}")
            client.CoreV1Api().delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, propagation_policy="Foreground",)


@click.command(name="mp", help="Match a pod by name (substring) in a namespace")
@click.argument("name", type=click.STRING)
@click.option("--interactive", "-i", is_flag=True, default=False, help="Whether to interactively connect to the pod")
@click.option("--namespace", "-n", type=click.STRING, default="default", help="Namespace of the pod")
@click.option("--shell", "-s", type=click.STRING, default="bash", help="Shell to use for the command")
def match_pod(name: str, namespace: str = "default", interactive: bool = False, shell: str = "bash"):
    """
    Match a pod by name (substring) in a namespace

    Args:
        name (str): The name of the pod to match
        namespace (str, optional): The namespace of the pod. Defaults to "default"
        interactive (bool, optional): Whether to interactively connect to the pod. Defaults to False
        shell (str, optional): The shell to use for the command. Defaults to "bash"

    Returns:
        None: Matches a pod by name (substring) in a namespace
    """
    config.load_config()
    pods = client.CoreV1Api().list_namespaced_pod(namespace=namespace)

    for pod in pods.items:
        if name in pod.metadata.name:
            if interactive:
                action = click.prompt(f"Do you want to connect to {pod.metadata.name} in namespace {namespace} startedAt: {pod.status.start_time} ? (y/n)")
                if action == "y":
                    subprocess.call(["kubectl", "exec", "-it", pod.metadata.name, "-n", namespace, "--", shell])
                    break
            click.echo(f"Pod found: {pod.metadata.name} in namespace {namespace} startedAt: {pod.status.start_time}")
