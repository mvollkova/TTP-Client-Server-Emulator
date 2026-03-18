# Emulating environment with Thrusted Third Party and Client-Server data exchange scenario

## Project Overview
This repository contains a basic implementation of a secure communication system as part of the SCS course. The system follows a **TTP (Trusted Third Party)** architecture to ensure identity verification using **X.509 certificates**.

## Current Progress
- [x] Repository structure created according to requirements.
- [x] **TTP Application**: Generates RSA 4096-bit keys and a self-signed Root CA certificate.
- [x] **Server Application**: Generates identity keys and obtains a TTP-signed certificate.
- [x] **Client Application**: Generates identity keys and obtains a TTP-signed certificate.
- [x] **Security**: Passwords and certificates management is initialized.
- [x] **Network Communication**: Basic TCP/IP socket connection established between Client and Server.
- [x] **Data Exchange**: Client successfully transmits Student ID to the Server.

## How to Run
1. Navigate to the `TTP` folder and run `python main.py` to generate the Root CA.
2. Navigate to the `server` folder and run `python server_setup.py` to get the Server certificate.
3. Navigate to the `client` folder and run `python client_setup.py` to get the Client certificate.

## Technologies Used
- **Language:** Python
- **Library:** `cryptography`
- **Encryption:** RSA 4096 bits
- **Certificate Format:** X.509

Note: Certificates are generated locally upon running the scripts and are excluded from the repository for security reasons.
