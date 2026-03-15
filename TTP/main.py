import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

def generate_ttp_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    with open("ttp_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"GUT_TTP_Office"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"Root_CA"),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(private_key, hashes.SHA256())

    # 4. Сохраняем сертификат в файл
    with open("ttp_certificate.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("--- success ---")
    print("files are created: ttp_private_key.pem and ttp_certificate.crt")

if __name__ == "__main__":
    generate_ttp_keys()