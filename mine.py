from Crypto.Hash import SHA256
import os,random,sys
args=sys.argv
Hash=SHA256.new()
hashes=int(open('hashes','r').read())
while True:
    r=str(random.randint(1,(2**30)))
    Hash.update(args[0])
    diff=2**250
    for j in range(int(hashes/840000)):
        diff/=2
    if int(Hash.hexdigest(),16)<(diff):
        os.system("curl "+sys.argv[1]+"/submit*"+r+"*"+sys.argv[2])
        hashes+=1