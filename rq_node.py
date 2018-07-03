# Rimcoin
# By iH8Ra1n (I may reveal my true identity later on)
# Credit license
# Do whatever you want with it. Just don't blame me for ANYTHING, and credit me.

from Crypto.Hash import SHA256
import os,random,time

def REAL_HASH(s):
    h=0 # hashed output
    for c in s:
        h=(31*h+ord(c))&0xFFFFFFFF # java hashing algo
    return ((h+0x80000000)&0xFFFFFFFF) - 0x80000000; # final return

diff=2**240
last=time.time()
last2=time.time()

def RIMCOIN_NODE(data,ip):
    global diff, last, last2
    out="" # output
    c=data.split("*")[0] # command
    args=data.split("*")[1:] # arguments
    if (time.time() - last) > 120:
        os.system("rm -rf forbidden; printf '[]' > forbidden")
        last=time.time()
    if (time.time() - last2) > 20:
        os.system("kill $(ps aux | grep curl)")
        last2=time.time()
    if c=="send":
        BALANCES=open("balance","r").read() # balance file
        BALANCES=eval(BALANCES) # evaluate, to read balances
        IDS=open("id","r").read() # open id file
        IDS=eval(IDS) # evaluate
        print(REAL_HASH(str(int(args[3].replace("L", ""),16)).replace("L","")))
        print(IDS[args[0]])
        if REAL_HASH(str(int(args[3].replace("L",""),16)).replace("L",""))==IDS[args[0]] and (BALANCES[args[0]]-float(args[2]))>0 and float(args[2]) > 0: # if wallet has enough money, and ID is ok, send. 
            BALANCES[args[0]]-=float(args[2]) # remove
            BALANCES[args[1]]+=float(args[2]) # add
            BL_FILE=open("balance","w") # write
            BL_FILE.write(str(BALANCES)) # write
            BL_FILE.close() # close
            NODE=open("nodes","r").read() # nodes
            NODE=NODE.split("/") # split
            for node in NODE:
                if len(node) >= 7:
                    continue
                try:
                    os.system("sh -c '(curl "+node+"/up_bal*"+"*".join(args[:-1])+" &sleep 1; kill $$)'& ") # contact, to update balances
                except:
                    pass
            return "\x41"; # success
        else:
            return "\x00"; # fail
    elif c=="get_mine":
         return str(diff);
    elif c=="new_mine":
         diff=diff/(131078/131072)
         return "\x41";
    elif c=="get_hash":
        return open('hashes','r').read();
    elif c=="submit":
        Hash=SHA256.new()
        Hash.update(args[0])
        hashes=int(open('hashes','r').read())
        forbidden=eval(open('forbidden','r').read())
        reward=50
        diff=2**240
        for j in range(int(hashes/1024)):
            diff=diff*(((2**15.77 - 1.0) / (2**15.77)))
            pass
        h=Hash.hexdigest()
        if int(h,16)<diff:
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
                if len(node) >= 7:
                    continue
                try:
                    os.system("sh -c '(curl "+node+"/update_mine*"+"*".join(args)+" &sleep 1; kill $$)'& ") # contact, to update balances
                except:
                    pass
            hashd=open('hashes','w')
            hashd.write(str(hashes+1))
            hashd.close()
            print("\x41")
            return "\x41";
        return "\x42";
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
            IPS=open("ip","r").read() # open id file
            IPS=eval(IPS) # evaluate
            if ip!=IPS[args[0]]:
                return "\x42";
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
        if not args[0] in BALANCES:
            BALANCEW=open("balance","w") # open
            BALANCES[args[0]]=0 # add new wallet
            BALANCEW.write(str(BALANCES)) # write
            BALANCEW.close() # close
            IPS=open("ip","r").read() # open id file
            IPS=eval(IPS) # evaluate
            IPS[args[0]]=ip
            IP=open('ip','w')
            IP.write(str(IPS))
            IP.close()
            return "\x41";
        else:
            return "\x42";
    elif c=="rq_bal":
        return open("balance","r").read(); # give balance file
    elif c=="update_mine":
        Hash=SHA256.new()
        Hash.update(args[0])
        hashes=int(open('hashes','r').read())
        forbidden=eval(open('forbidden','r').read())
        reward=50
        diff=2**240
        for j in range(int(hashes/1024)):
            diff=diff*(131071/131072)
        h=Hash.hexdigest()
        if int(h,16)<diff:
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
            hashd=open('hashes','w')
            hashd.write(str(hashes+1))
            hashd.close()
            print("\x41")
            return "\x41";
        return "\x42";
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
                IDS[args[0]]=REAL_HASH(str(key).replace("L","")) # get real hash
                IDSW=open("id","w") # open
                IDSW.write(str(IDS)) # write
                IDSW.close() # close
                return str(hex(key))[2:]; # return hex version of key
            else:
                return "\x43";
        except:
            return "\x42"; # fail
    elif c=="app":
        i=open('balance','r') # open users file
        i=eval(i.read()) # read said file
        bal=str(i[args[0]]); # get balance
        # final html
        return """
<html>
<head>
<meta name="apple-mobile-web-app-capable" content="yes">
<title>Wallet</title>
<style>
* {
    background-color: #ffffff;
    font-size:56px;
    border-size: 0px;
    color: #1294F6;
    border:0;
};
</style>
</head>
<body><center>
<script src='https://code.jquery.com/jquery-3.3.1.js'></script>
<h1 style="font-family:helvetica">User</h1>
<p><div id="x" style="font-family:helvetica"></div></p>
<p><strong id="y" style="font-family:helvetica">Balance</strong></p>
<p><div id="z" style="font-family:helvetica"></div></p>
<h1 style="font-family:helvetica">Function</h1>
<button onclick="
rec=prompt('Recieving Address? ');am=prompt('Amount? ');getText('/send*'+localStorage.user+'*'+rec+'*'+am+'*'+localStorage.sk);bal-=parseFloat(am);">Send</button>
<script>
bal="""+bal+""";
function getText(url){
  document.body.innerHTML+="<iframe src='"+url+"' id='abc' style='opacity:0;'></iframe>";
};
if (localStorage.ft!="n"){
    localStorage.user='"""+str(args[0])+"""';
    localStorage.sk='"""+str(args[1])+"""';
    localStorage.ft="n";
};
document.getElementById("x").innerHTML=localStorage.user;
document.getElementById("z").innerHTML=bal.toString();
setInterval(function f(){document.getElementById('z').innerHTML=bal.toString();},500);
</script>

</center></body></html>"""
    elif c=="rq_ip":
        return open('ip','r').read();
    return "\x40"; # no command
