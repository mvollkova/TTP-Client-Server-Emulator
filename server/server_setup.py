from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import socket

server_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)
with open("server_private_key.pem", "wb") as f:
    f.write(server_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My_Safe_Server"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"server.com"),
])

with open("../ttp/ttp_private_key.pem", "rb") as f:
    ttp_private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("../ttp/ttp_certificate.crt", "rb") as f:
    ttp_cert = x509.load_pem_x509_certificate(f.read())

server_cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    ttp_cert.subject #TTP
).public_key(
    server_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.UTC)
).not_valid_after(
    datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)
).sign(ttp_private_key, hashes.SHA256()) # sign TTP

with open("server_certificate.crt", "wb") as f:
    f.write(server_cert.public_bytes(serialization.Encoding.PEM))

print("Certificate for SERVER created and signed by TTP")

def run_basic_server():
    print("\n--- Starting Base Server for Communication ---")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server is listening on port 12345...")
    
    conn, addr = server_socket.accept()
    print(f"Connection established with: {addr}")
    
    data = conn.recv(1024).decode()
    print(f"Log: Received message: '{data}'")
    
    conn.sendall("Hello Client! Connection is active.".encode())
    conn.close()
    print("Communication finished. Server closed.")

if __name__ == "__main__":
    run_basic_server()