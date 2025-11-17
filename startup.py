import platform
from scripts import linux_setup, windows_setup

def main():
    os_name = platform.system()
    print("Detected OS:", os_name)

    if os_name in ("Linux", "Darwin"):  # Darwin = macOS
        print("Using Linux/macOS setup...")
        linux_setup.main()
    elif os_name == "Windows":
        print("Using Windows setup...")
        windows_setup.main()
    else:
        print("Unsupported OS:", os_name)
        print("This script supports Linux, macOS, and Windows only.")

if __name__ == "__main__":
    main()
