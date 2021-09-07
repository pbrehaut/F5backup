import os
import io
import pyAesCrypt
from collections import defaultdict

PATH = r'C:\Users\pbrehaut3\PycharmProjects\F5backup\getpassword'
PWFILE = os.path.join(PATH, 'passwords.txt')
ENCPWFILE = os.path.join(PATH, 'passwords.txt.aes')
MASTERKEY = 'TESTKEY123$%^'
bufferSize = 64 * 1024

# Load passwords from encrypted file on import
if os.path.exists(ENCPWFILE):
    with open(ENCPWFILE, 'rb') as fCiph:

        fDec = io.BytesIO()

        # get ciphertext length
        ctlen = len(fCiph.read())

        # go back to the start of the ciphertext stream
        fCiph.seek(0)

        # decrypt stream
        pyAesCrypt.decryptStream(fCiph, fDec, MASTERKEY, bufferSize, ctlen)

        # print decrypted data
        X = str(fDec.getvalue().decode('utf-8'))

    P = defaultdict(dict)
    for Line in X.splitlines():
        F = Line.split(':')
        P[F[0]][F[1]] = F[2].strip()


def get_password(host, user):
     # Check if there is a specific host in the password structure
    if host in P:
        if user in P[host]:
            return P[host][user]
        if user in P['all']:
            # If no user matching in password dict use default for that user
            return P['all'][user]
    # If there is no specific host in the password file use the defaults - key 'ALL'
    if user in P['all']:
        return P['all'][user]

if __name__=='__main__':
    print(get_password('device1','root'))
    if os.path.exists(PWFILE):
        x = input('Found new clear text input file, create new encrypted file [y/n]?')
        if 'y' in x.lower():
            pyAesCrypt.encryptFile(PWFILE, ENCPWFILE, MASTERKEY, bufferSize)
            print('Created new encrypted password file:', ENCPWFILE)
            x = input('Remove clear text input file [y/n]?')
            if 'y' in x.lower():
                os.remove(PWFILE)