# DKIM-verify
A command line tool to verify the DKIM signature of an email with the possibility of skipping the request to the DNS server.

## Usage
```commandline
dkim-verify.py --help
```
```
usage: dkim-verify.py [-h] -e EMAIL [-v] [--txt-file TXT_FILE | --txt ... | -p PUBLIC_KEY_DATA]

Verify the DKIM signature of an email.

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        The email to verify.
  -v, --verbose         Verbose mode. Prints debugging messages about the verification process.
  --txt-file TXT_FILE   The file containing the DNS TXT record.
  --txt ...             The DNS TXT record.
  -p PUBLIC_KEY_DATA, --public-key-data PUBLIC_KEY_DATA
                        The public key.
```
## Example (using the real DKIM DNS TXT record)
```commandline
dkim-verify.py --email email.eml --verbose
```

## Examples providing a local DKIM DNS TXT record (skipping the request to the DNS server)
```commandline
dkim-verify.py --email email.eml --verbose --txt-file localhost
```
```commandline
dkim-verify.py --email email.eml --verbose --txt 'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwO91hEBFuPQOJ+1dvGxKUzDMEKD5s4KOzKRwP/XRrs46Oht+JdXPD0hkraBNAii98hA11NfGlwSFuf2kIjQh/ncQmSeeSXbAhdY73VkzV8PD4OXFq5hShgeiamzJksA2KuxT6G8yj1WH8Ytvtuyzm9jXwhqngyaZA7QOXu4vLgQIDAQAB;'
```
```commandline
dkim-verify.py --email email.eml --verbose --dkim-version DKIM1 --key-type rsa --public-key-data MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwO91hEBFuPQOJ+1dvGxKUzDMEKD5s4KOzKRwP/XRrs46Oht+JdXPD0hkraBNAii98hA11NfGlwSFuf2kIjQh/ncQmSeeSXbAhdY73VkzV8PD4OXFq5hShgeiamzJksA2KuxT6G8yj1WH8Ytvtuyzm9jXwhqngyaZA7QOXu4vLgQIDAQAB
```
```commandline
dkim-verify.py --email email.eml --verbose --public-key-data MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwO91hEBFuPQOJ+1dvGxKUzDMEKD5s4KOzKRwP/XRrs46Oht+JdXPD0hkraBNAii98hA11NfGlwSFuf2kIjQh/ncQmSeeSXbAhdY73VkzV8PD4OXFq5hShgeiamzJksA2KuxT6G8yj1WH8Ytvtuyzm9jXwhqngyaZA7QOXu4vLgQIDAQAB
```

## Requirements
- [dkimpy](https://launchpad.net/dkimpy)