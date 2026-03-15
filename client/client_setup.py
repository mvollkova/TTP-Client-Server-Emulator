from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
client_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

with open("client_private_key.pem", "wb") as f:
    f.write(client_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Student_User"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"my_client_app"),
])

with open("../ttp/ttp_private_key.pem", "rb") as f:
    ttp_private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("../ttp/ttp_certificate.crt", "rb") as f:
    ttp_cert = x509.load_pem_x509_certificate(f.read())

client_cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    ttp_cert.subject
).public_key(
    client_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.UTC)
).not_valid_after(
    datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)
).sign(ttp_private_key, hashes.SHA256())

with open("client_certificate.crt", "wb") as f:
    f.write(client_cert.public_bytes(serialization.Encoding.PEM))

print("Certificate for CLIENT created and signed by TTP")