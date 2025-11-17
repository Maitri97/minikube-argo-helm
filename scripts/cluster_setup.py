from .common_functions import (
    run_cmd,
    run_cmd_and_exit_on_error,
    wait_for_pods,
    get_argocd_password,
)
from . import port_forwarder


def start_minikube_cluster():
    """
    Start Minikube using the docker driver.
    Reuse an existing cluster if it's already running.
    """
    print("\n=== Starting Minikube ===")

    status_code = run_cmd(["minikube", "status"])
    if status_code != 0:
        print("Minikube is not running. Starting a new cluster with docker driver...")
        run_cmd_and_exit_on_error(["minikube", "start", "--driver=docker"])
    else:
        print("Minikube is already running. Reusing existing cluster.")

    run_cmd_and_exit_on_error(["kubectl", "config", "use-context", "minikube"])
    print("Kubectl context set to Minikube.")


def install_argocd():
    """
    Install ArgoCD in the 'argocd' namespace and wait for the server deployment.
    """
    print("\n=== Installing ArgoCD ===")

    # Create namespace (ignore error if it already exists)
    run_cmd(["kubectl", "create", "namespace", "argocd"])

    # Apply the official ArgoCD install manifest
    run_cmd_and_exit_on_error([
        "kubectl", "apply", "-n", "argocd",
        "-f", "https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
    ])

    print("Waiting for ArgoCD server deployment to be ready...")
    run_cmd_and_exit_on_error([
        "kubectl", "rollout", "status",
        "deployment/argocd-server",
        "-n", "argocd",
        "--timeout=300s",
    ])

    print("ArgoCD installed successfully.")


def deploy_application():
    """
    Create the demo-app namespace, apply the ArgoCD Application manifest,
    and wait until at least one pod in demo-app is Ready and Running.
    """
    print("\n=== Deploying Application via ArgoCD ===")

    # Create namespace for demo app (ignore error if it exists)
    run_cmd(["kubectl", "create", "namespace", "demo-app"])

    # Apply the ArgoCD Application definition
    run_cmd_and_exit_on_error([
        "kubectl", "apply", "-n", "argocd", "-f", "argocd-application.yaml"
    ])

    # Wait for pods in demo-app namespace
    print("Waiting for demo-app pods to become Ready...")
    wait_for_pods("demo-app")


def print_access_and_port_forward_info():
    """
    Print ArgoCD login details, then start background port-forwards
    and show how to stop them + security note.
    """
    print("\n=== Access Information ===")

    password = get_argocd_password()
    print("\nArgoCD Login:")
    print("  Username: admin")
    print(f"  Password: {password if password else '(unable to retrieve)'}")

    # Start background port-forwards and display stop instructions
    port_forwarder.start_port_forwards()


def main_cluster_flow():
    """
    Main sequence:
      1. Start or reuse Minikube
      2. Install ArgoCD
      3. Deploy the demo app via ArgoCD
      4. Start background port-forwards and show how to stop them
    """
    start_minikube_cluster()
    install_argocd()
    deploy_application()
    print_access_and_port_forward_info()
