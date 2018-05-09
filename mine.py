from Crypto.Hash import SHA256
import os,random,sys,subprocess
args=sys.argv
hashes=1
diff=2**240
for j in range(int(hashes/1024)):
    diff=diff*(131071/131072)
while True:
    r=str(hex(random.randint(1,(2**32)))[2:])
    Hash=SHA256.new()
    Hash.update(r)
    if int(Hash.hexdigest(),16)<(diff):
        print("w00t")
        sys.stdout.flush()
        os.system("curl "+sys.argv[1]+"/submit*"+r+"*"+sys.argv[2])
        hashes+=1
