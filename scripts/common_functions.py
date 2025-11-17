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

def wait_for_pods(namespace):
    """Simple wait loop for any Ready+Running pod in a namespace."""
    for attempt in range(1, 16):
        print(f"Checking pods in {namespace} (try {attempt}/15)")

        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "--no-headers"],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if output:
            print(output)
            for line in output.splitlines():
                parts = line.split()
                if len(parts) < 3:
                    continue

                ready = parts[1]  # e.g. 1/1
                status = parts[2] # e.g. Running

                if status == "Running" and ready.count("/") == 1:
                    r, t = ready.split("/")
                    if r == t:
                        print("Pod is Ready and Running.")
                        return
        else:
            print(f"No pods found in {namespace}.")

        time.sleep(8)

    print("Finished waiting for pods. Check manually if required.")

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
