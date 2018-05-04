# Rimcoin
# By iH8Ra1n (I may reveal my true identity later on)
# Credit license
# Do whatever you want with it. Just don't blame me for ANYTHING, and credit me.

from Crypto.Hash import SHA256
import os,random

def REAL_HASH(s):
    h=0 # hashed output
    for c in s:
        h=(31*h+ord(c))&0xFFFFFFFF # java hashing algo
    return ((h+0x80000000)&0xFFFFFFFF) - 0x80000000; # final return

def RIMCOIN_NODE(data):
    out="" # output
    c=data.split("*")[0] # command
    args=data.split("*")[1:] # arguments
    if c=="send":
        BALANCES=open("balance","r").read() # balance file
        BALANCES=eval(BALANCES) # evaluate, to read balances
        IDS=open("id","r").read() # open id file
        IDS=eval(IDS) # evaluate
        if REAL_HASH(str(int(args[3],16)))==IDS[args[0]] and (BALANCES[args[0]]-float(args[2]))>0: # if wallet has enough money, and ID is ok, send. 
            BALANCES[args[0]]-=float(args[2]) # remove
            BALANCES[args[1]]+=float(args[2]) # add
            BL_FILE=open("balance","w") # write
            BL_FILE.write(str(BALANCES)) # write
            BL_FILE.close() # close
            NODE=open("nodes","r").read() # nodes
            NODE=NODE.split("/") # split
            for node in NODE:
                try:
                    os.system("(curl "+node+"/up_bal*"+"*".join(args)+" &sleep 20; kill $$)&") # contact, to update balances
                except:
                    pass
            return "\x41"; # success
        else:
            return "\x00"; # fail
    elif c=="submit":
        Hash=SHA256.new()
        Hash.update(args[0])
        hashes=int(open('hashes','r').read())
        forbidden=eval(open('forbidden','r').read())
        reward=50
        for j in range(int(hashes/840000)):
            reward/=2
        if int(Hash.hexdigest(),16)<((2**256)-(hashes*96)) and (not args[0] in forbidden):
            NODE=open("nodes","r").read() # read
            NODE=NODE.split("/") # split
            BALANCES=open("balance","r").read() # balance file
            BALANCES=eval(BALANCES) # evaluate, to read balances
            BALANCES[args[1]]+=reward
            BL_FILE=open("balance","w") # write
            BL_FILE.write(str(BALANCES)) # write
            BL_FILE.close() # close
            forbidden.append(args[0])
            forb=open('forbidden','w')
            forb.write(str(forbidden))
            forb.close()
            for node in NODE:
                try:
                    os.system("(curl "+node+"/update_mine*"+"*".join(args)+" &sleep 20; kill $$)&") # contact, to update balances
                except:
                    pass
            hashd=open('hashes','w')
            hashd.write(str(hashes+1))
            hashd.close()
    elif c=="bal":
        try:
            BALANCES=open("balance","r").read() # read
            BALANCES=eval(BALANCES) # evaluate
            return BALANCES[args[0]]; # return
        except:
            return "\x42"; # fail
    elif c=="rq_node":
        NODE=open("nodes","r").read() # get nodes
        NODE=NODE.split("/") # split
        return str(NODE); # return list of nodes
    elif c=="add_node":
        try:
            NODE=open("nodes","r").read() # read
            NODE=NODE.split("/") # split
            NODE.append(args[0]) # add
            NODEW=open("nodes","w") # open
            NODEW.write("/".join(NODE)) # write
            NODEW.close() # close
            for node in NODE:
                try:
                    os.system("(curl "+node+"/add_node_update*"+"*".join(args)+" &sleep 20; kill $$)&") # contact all other nodes, to make this change
                except:
                    pass
            return "\x41"; # success
        except:
            return "\x42"; # fail
    elif c=="up_bal":
        try:
            BALANCES=open("balance","r").read() # open
            BALANCES=eval(BALANCES) # read
            BALANCES[args[0]]-=float(args[2]) # remove
            BALANCES[args[1]]+=float(args[2]) # add
            BL_FILE=open("balance","w") # open
            BL_FILE.write(str(BALANCES)) # write
            BL_FILE.close() # close
            return "\x41"; # success
        except:
            return "\x42"; # fail
    elif c=="add_node_update":
        NODE=open("nodes","r").read() # open, and read
        NODE=NODE.split("/") # split
        NODE.append(args[0]) # add
        NODEW=open("nodes","w") # open
        NODEW.write("/".join(NODE)) # write
        NODEW.close() # close
    elif c=="add_rc_wallet":
        BALANCES=open("balance","r").read() # get file
        BALANCES=eval(BALANCES) # evaluate
        BALANCEW=open("balance","w") # open
        BALANCES[args[0]]=0 # add new wallet
        BALANCEW.write(str(BALANCES)) # write
        BALANCEW.close() # close
    elif c=="rq_bal":
        return open("balance","r").read(); # give balance file
    elif c=="update_mine":
        forbidden=eval(open('forbidden','r').read())
        forbidden.append(args[0])
        forb=open('forbidden','w')
        forb.write(str(forbidden))
        forb.close()
        reward=50
        for j in range(int(hashes/840000)):
            reward/=2
        BALANCES=open("balance","r").read() # balance file
        BALANCES=eval(BALANCES) # evaluate, to read balances
        BALANCES[args[1]]+=reward
        BL_FILE=open("balance","w") # write
        BL_FILE.write(str(BALANCES)) # write
        BL_FILE.close() # close
    elif c=="create":
        BALANCES=open("balance","r").read() # open
        BALANCES=eval(BALANCES)
        try:
            if not args[0] in BALANCES: # they shouldn't be in there, or the wallet is being re-created! 
                BALANCES[args[0]]=0 # set balance
                BALANCEW=open("balance","w") # open for writing
                BALANCEW.write(str(BALANCES)) # write
                BALANCEW.close() # close
                NODE=open("nodes","r").read() # open
                NODE=NODE.split("/") # split
                for node in NODE:
                    try:
                        os.system("(curl --connect-timeout 20 "+node+"/add_rc_wallet*"+"*".join(args)+" &sleep 20; kill $$)&") # contact each node, informing that a new wallet has been created. 
                    except:
                           pass
                IDS=open("id","r").read() # open id file
                IDS=eval(IDS) # evaluate
                key=random.getrandbits(160) # get random bits
                IDS[args[0]]=REAL_HASH(str(key)) # get real hash
                IDSW=open("id","w") # open
                IDSW.write(str(IDS)) # write
                IDSW.close() # close
                return str(hex(key))[2:]; # return hex version of key
            else:
                return "\x43";
        except:
            return "\x42"; # fail
    return "\x40"; # no command

