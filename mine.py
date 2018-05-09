from Crypto.Hash import SHA256
import os,random,sys,subprocess
args=sys.argv
diff=float(subprocess.check_output(("curl "+args[1]+"/get_mine -s").split(" ")))
os.system("curl "+args[1]+"/new_mine -s")
while True:
    r=str(hex(random.randint(1,(2**32)))[2:])
    Hash=SHA256.new()
    Hash.update(r)
    if int(Hash.hexdigest(),16)<(diff):
        os.system("curl "+sys.argv[1]+"/submit*"+r+"*"+sys.argv[2])
