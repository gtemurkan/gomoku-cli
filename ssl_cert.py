"""
A one-function module for generating local self-signed certificates
"""

import subprocess
import os


def generate_ssl_cert(cert_file="server.crt", key_file="server.key"):
    """
    Generates a self-signed SSL-certificate and a private key.
    """
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"Certificate {cert_file} and "
              f"private key {key_file} already exist.")
        return

    command = [
        "openssl", "req", "-new", "-x509", "-days", "365", "-nodes",
        "-out", cert_file,
        "-keyout", key_file,
        "-subj", "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Certificate created: {cert_file}")
        print(f"Private key generated: {key_file}")
    except FileNotFoundError:
        print("OpenSSL not found. Ensure OpenSSL is installed and accessed via PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating certificate: {e}")


if __name__ == "__main__":
    generate_ssl_cert()
