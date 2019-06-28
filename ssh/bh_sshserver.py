import socket
import paramiko
import threading
import sys

 


host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server(paramiko.ServerInterface):
    def _init(self):
        self.event = threading.Event()
        
    def check_channel_request(self,kind,chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if(username=='root') and (password=='password'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
server = sys.argv[1]
ssh_port = int(sys.argv[2])
    
try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((server,ssh_port))
    sock.listen(100)
    print '[+] Listen on connection ...'
    client,addr = sock.accept()
except Exception,e:
    print '[-] Listen failed :' + str(e)
    sys.exit(1)
print '[+] Get a connection'


try:
    bhsession = paramiko.Transport(client)
    bhsession.set_gss_host(socket.getfqdn(""))
    
    try:
        bhsession.load_server_moduli
    except:
        print "Failed to load moduli"
        raise
    bhsession.add_server_key(host_key)
    server = Server()
    try:
        bhsession.start_server(server=server)
    except paramiko.ssh_exception,x:
        print '[-] SSH negotiation failed.'
    chan = bhsession.accept(20)
    print '[+] Authenticated'
    print chan.recv(1024)
    chan.send('Welcame to bh_ssh')
    while True:
        try:
            command = raw_input("Enter command:").strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhsession.close()
                raise exception('exit')
        except KeyboardInterrupt:
            bhsession.close()
except Exception as e:
    print '[-] Caught exception:' + str(e.__class__) + ':' + str(e)
    try:
        bhsession.close()
    except:
        pass
    exit(1)