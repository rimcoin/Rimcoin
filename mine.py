from Crypto.Hash import SHA256
import os,random,sys,subprocess
args=sys.argv
os.system("curl "+args[1]+"/get_hash -s > hashd")
hashes=int(open("hashd","r").read())
for j in range(int(hashes/131072)):
     diff/=2
while True:
    r=str(random.randint(1,(2**60)))
    Hash=SHA256.new()
    Hash.update(r)
    diff=2**240
    for j in range(int(hashes/1048576)):
        diff/=2
    if int(Hash.hexdigest(),16)<(diff):
        os.system("curl "+sys.argv[1]+"/submit*"+r+"*"+sys.argv[2])
        hashes+=1
