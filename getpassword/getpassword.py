from collections import defaultdict
PWFILE = 'passwords.txt'


def get_password(host, user):
    #Load passworks
    with open(PWFILE) as F:
        P = defaultdict(dict)
        for Line in F.readlines():
            F = Line.split(':')
            P[F[0]][F[1]] = F[2].strip()

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
