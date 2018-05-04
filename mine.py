from Crypto.Hash import SHA256
import os,random,sys
args=sys.argv
Hash=SHA256.new()
hashes=int(open('hashes','r').read())
while True:
    r=str(random.randint(1,(2**30)))
    Hash.update(args[0])
    if int(Hash.hexdigest(),16)<((2**256)-(hashes*96)):
        os.system("curl "+sys.argv[1]+"/submit*"+r+"*"+sys.argv[2])
        hashes+=1