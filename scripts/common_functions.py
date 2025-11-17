import subprocess, sys, base64, time

def run_cmd(cmd):
    """Run a command and print it."""
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd).returncode

def run_cmd_and_exit_on_error(cmd):
    """Run a command and stop if it fails."""
    code = run_cmd(cmd)
    if code != 0:
        print("Command failed:", code)
        sys.exit(code)

def check_exists(name):
    """Check if a binary exists on PATH."""
    try:
        subprocess.run([name, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

import subprocess
import time


def wait_for_pods(namespace: str,
                  max_attempts: int = 15,
                  poll_interval: int = 8,
                  wait_timeout: str = "120s") -> None:
    """
    Wait until at least one pod in the namespace is Ready.

    This uses `kubectl wait --for=condition=Ready` instead of manually
    parsing `kubectl get pods` output, so the logic is simpler and relies
    on Kubernetes' own readiness condition.

    - First, we poll until at least one pod exists in the namespace.
    - Once pods exist, we call `kubectl wait` to wait for them to become Ready.
    """

    for attempt in range(1, max_attempts + 1):
        print(f"[wait_for_pods] Checking pods in '{namespace}' (try {attempt}/{max_attempts})")

        # Step 1: Check if there are any pods at all in this namespace
        get_result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "--no-headers"],
            capture_output=True,
            text=True
        )

        output = get_result.stdout.strip()

        if not output:
            # No pods yet – ArgoCD/Helm may still be creating them
            print(f"[wait_for_pods] No pods found in namespace '{namespace}' yet. Waiting...")
            time.sleep(poll_interval)
            continue

        # At least one pod exists – show them for visibility
        print("[wait_for_pods] Current pods:")
        print(output)

        # Step 2: Use kubectl's native wait for Ready condition
        wait_cmd = [
            "kubectl", "wait",
            "--for=condition=Ready",
            "pod",
            "--all",
            "-n", namespace,
            f"--timeout={wait_timeout}",
        ]

        print(f"[wait_for_pods] Pods detected. Waiting for them to become Ready (timeout={wait_timeout})...")
        wait_result = subprocess.run(wait_cmd)

        if wait_result.returncode == 0:
            print("[wait_for_pods] ✅ Pods are Ready.")
            return

        print("[wait_for_pods] Pods not Ready yet. Retrying...")
        time.sleep(poll_interval)

    print("[wait_for_pods] ❌ Finished waiting. Pods did not become Ready in time.")
    print(f"Please check manually with: kubectl get pods -n {namespace}")
    # You can also raise an exception if you want to fail the script:
    # raise RuntimeError(f"Pods in namespace '{namespace}' did not become Ready in time.")

def get_argocd_password():
    """Retrieve ArgoCD initial admin password from secret."""
    try:
        result = subprocess.run(
            ["kubectl","-n","argocd","get","secret","argocd-initial-admin-secret",
             "-o","jsonpath={.data.password}"],
            capture_output=True, text=True
        )
        encoded = result.stdout.strip()
        return base64.b64decode(encoded).decode() if encoded else ""
    except:
        return ""
