
################################################### Python Import ##################################

from kubernetes import client, config

################################################### Project Import #################################

################################################### Main Declaration ###############################


def ssh_volume() -> client.V1Volume:
    """
    Create a projected volume for Kubernetes API access.
    
    This volume provides the necessary credentials and configuration files
    that a pod needs to authenticate with the Kubernetes API server.
    
    Returns:
        client.V1Volume: A projected volume containing:
            - Service account token for authentication
            - CA certificate for secure communication
            - Namespace information via downward API
    """
    return client.V1Volume(
        name="kube-api-access-msslb",  # Volume name for mounting
        projected=client.V1ProjectedVolumeSource(
            default_mode=420,  # Octal permissions (644 in decimal)
            sources=[
                # Source 1: Service account token for API authentication
                client.V1VolumeProjection(
                    service_account_token=client.V1ServiceAccountTokenProjection(
                        expiration_seconds=3607,  # Token expiration time
                        path="token"  # Path where token will be mounted
                    )
                ),
                # Source 2: CA certificate for secure API communication
                client.V1VolumeProjection(
                    config_map=client.V1ConfigMapProjection(
                        name="kube-root-ca.crt",  # ConfigMap containing CA certificate
                        items=[
                            client.V1KeyToPath(
                                key="ca.crt",  # Key in the ConfigMap
                                path="ca.crt"  # Path where CA cert will be mounted
                            )
                        ]
                    )
                ),
                # Source 3: Downward API to get current namespace
                client.V1VolumeProjection(
                    downward_api=client.V1DownwardAPIProjection(
                        items=[
                            client.V1DownwardAPIVolumeFile(
                                path="namespace",  # Path where namespace will be written
                                field_ref=client.V1ObjectFieldSelector(
                                    api_version="v1",
                                    field_path="metadata.namespace"  # Reference to pod's namespace
                                )
                            )
                        ]
                    )
                )
            ]
        )
    )


def ssh_container() -> client.V1Container:
    """
    Create a privileged container for SSH access to a Kubernetes node.
    
    This container uses nsenter to enter the host's namespaces, effectively
    giving it access to the host system while running inside a pod.
    
    Returns:
        client.V1Container: A privileged container configured for node access
    """
    return client.V1Container(
        name="shell",  # Container name
        image="docker.io/alpine:3.19",  # Lightweight Alpine Linux image
        # The nsenter command allows a user to execute a program within the namespaces of another process.
        command=["nsenter"],
        args=[
            '-t', '1',      # Target process ID (1 = init process)
            '-m',            # Mount namespace
            '-u',            # User namespace
            '-i',            # IPC namespace
            '-n',            # Network namespace
            "sleep",         # Command to execute
            '14000'          # Sleep for ~4 hours to keep container running
        ],
        # Mount the API access volume for authentication
        volume_mounts=[client.V1VolumeMount(
            name="kube-api-access-msslb",
            read_only=True,  # Read-only mount for security
            mount_path="/var/run/secrets/kubernetes.io/serviceaccount"  # Standard mount path
        )],
        # Privileged context allows access to host namespaces
        security_context=client.V1SecurityContext(
            privileged=True  # Required for nsenter to work properly
        )
    )


def ssh_into_node(node_name: str, pod_name: str, namespace: str = "kube-system") -> client.V1Pod:
    """
    Create a pod that provides SSH access to a specific Kubernetes node.
    
    This function creates a privileged pod that runs on the specified node
    and uses nsenter to access the host system's namespaces, effectively
    providing SSH-like access to the node.
    
    Args:
        node_name (str): The name of the target node where the pod will be scheduled
        pod_name (str): The name to assign to the created pod
        namespace (str, optional): The namespace where the pod will be created. 
                                 Defaults to "kube-system".
    
    Returns:
        client.V1Pod: The created pod object that provides node access
        
    Note:
        The pod runs with privileged security context and has access to host
        namespaces (network, PID, IPC) to enable full node access.
    """
    return client.CoreV1Api().create_namespaced_pod(
        namespace=namespace,
        body=client.V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=client.V1ObjectMeta(
                name=pod_name,
                namespace=namespace
            ),
            spec=client.V1PodSpec(
                # Mount the API access volume for authentication
                volumes=[
                    ssh_volume()
                ],
                # Use the privileged SSH container
                containers=[
                    ssh_container()
                ],
                # Immediate termination when pod is deleted
                termination_grace_period_seconds=0,
                # Schedule pod on specific node
                node_name=node_name,
                # Access host network, PID, and IPC namespaces
                host_network=True,  # Use host's network stack
                host_pid=True,      # Access host's process tree
                host_ipc=True,      # Access host's IPC namespaces
                # Allow pod to run on any node regardless of taints
                tolerations=[
                    client.V1Toleration(
                        operator="Exists"  # Tolerate all taints
                    ),
                ],
                # Pod scheduling and priority settings
                preemption_policy="PreemptLowerPriority",  # Can preempt lower priority pods
                priority=2000001000,  # High priority to ensure scheduling
                enable_service_links=True,  # Enable service environment variables
                priority_class_name="system-node-critical"  # Use system critical priority class
            )
        )
    )