import paramiko

def FortigateConnection(user, passw, host):
    "Returns a paramiko client object"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(host, port=8022, username=user, password=passw)
        return client

    except:
        raise
