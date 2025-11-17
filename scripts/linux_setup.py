import shutil
from .common_functions import run_cmd_and_exit_on_error
from .cluster_setup import main_cluster_flow

def ensure_docker_running():
    print("Checking if Docker is installed...")
    if shutil.which("docker") is None:
        print("Docker is not installed. Please install Docker Desktop manually:")
        print("  https://www.docker.com/products/docker-desktop/")
        exit(1)

def install_kubectl():
    print("Installing kubectl...")
    run_cmd_and_exit_on_error([
        "curl", "-LO",
        "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
    ])
    run_cmd_and_exit_on_error(["chmod", "+x", "kubectl"])
    run_cmd_and_exit_on_error(["sudo", "mv", "kubectl", "/usr/local/bin/"])

def install_minikube():
    print("Installing Minikube...")
    run_cmd_and_exit_on_error([
        "curl", "-LO",
        "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    ])
    run_cmd_and_exit_on_error(["chmod", "+x", "minikube-linux-amd64"])
    run_cmd_and_exit_on_error(["sudo", "mv", "minikube-linux-amd64", "/usr/local/bin/minikube"])

def install_helm():
    print("Installing Helm...")
    run_cmd_and_exit_on_error([
        "curl", "-fsSL",
        "https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3",
        "-o", "get_helm.sh"
    ])
    run_cmd_and_exit_on_error(["chmod", "700", "get_helm.sh"])
    run_cmd_and_exit_on_error(["./get_helm.sh"])

def main():
    ensure_docker_running()

    if shutil.which("kubectl") is None:
        install_kubectl()
    if shutil.which("minikube") is None:
        install_minikube()
    if shutil.which("helm") is None:
        install_helm()

    main_cluster_flow()
