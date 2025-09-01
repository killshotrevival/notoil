from kubernetes.stream import stream

def exec_commands(api_instance, pod_name: str, namespace: str = "default"):
    """
    Execute an interactive shell session in a Kubernetes pod.
    
    This function establishes a streaming connection to a pod and provides an interactive
    shell experience. It continuously monitors the pod's stdout and stderr streams,
    displays output to the user, and forwards user input to the pod.
    
    Args:
        api_instance: Kubernetes API instance for pod operations
        pod_name (str): Name of the target pod
        namespace (str, optional): Kubernetes namespace containing the pod. Defaults to "default"
    
    Example:
        >>> api_instance = get_kubernetes_api()
        >>> exec_commands(api_instance, "my-pod", "my-namespace")
        Entering interactive shell. Type 'exit' to quit.
        $ ls -la
        total 0
        drwxr-xr-x 1 root root 0 Jan 1 00:00 .
        ...    
    """
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command=['/bin/sh'],
                  stderr=True, stdin=True,
                  stdout=True, tty=True,
                  _preload_content=False)

    print("Entering interactive shell. Type 'exit' to quit.")

    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            print(resp.read_stdout(), end='')
        if resp.peek_stderr():
            print(resp.read_stderr(), end='')

        try:
            command = input()
            if command.lower() == "exit":
                break
            else:
                resp.write_stdin(command + "\n")
        except EOFError:
            break

    resp.close()