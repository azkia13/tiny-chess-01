import json,os,sys,urllib.request,urllib.error
sys.setrecursionlimit(10000)
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
LIM=150000
INF=1000000
MATE=100000
SQ=[r*16+f for r in range(8) for f in range(8)]
VAL=[0,100,320,330,500,900,0]
PH=[0,0,1,1,2,4,0]
PS=["SSSSSSSS\x85\x85\x85\x85\x85\x85\x85\x85]]gqqg]]XX]ll]XXSSSggSSSXNISSINXX]]??]]XSSSSSSSS","!+5555+!+?SSSS?+5S]bb]S55XbggbX55SbggbS55X]bb]X5+?SXXS?+!+5555+!","?IIIIII?ISSSSSSIISX]]XSIIXX]]XXIIS]]]]SII]]]]]]IIXSSSSXI?IIIIII?","SSSSSSSSX]]]]]]XNSSSSSSNNSSSSSSNNSSSSSSNNSSSSSSNNSSSSSSNSSSXXSSS","?IINNII?ISSSSSSIISXXXXSINSXXXXSNSSXXXXSNIXXXXXSIISXSSSSI?IINNII?","5++!!++55++!!++55++!!++55++!!++5?55++55?I??????IggSSSSgggq]SS]qg","!+5??5+!5?ISSI?55IgqqgI55Iq{{qI55Iq{{qI55IgqqgI555SSSS55!555555!"]
KN=[-33,-31,-18,-14,14,18,31,33]
KG=[-17,-16,-15,-1,1,15,16,17]
BI=[-17,-15,15,17]
RO=[-16,-1,1,16]
CK=[15]*128
CK[0]=13;CK[7]=14;CK[4]=12;CK[112]=7;CK[119]=11;CK[116]=3
def _mk(t):
    w=[0]*128;bb=[0]*128;s=PS[t]
    for r in range(8):
        for f in range(8):
            w[r*16+f]=ord(s[(7-r)*8+f])-83
            bb[r*16+f]=ord(s[r*8+f])-83
    return w,bb
PW=[[0]*128];PB=[[0]*128]
for _i in range(7):
    _w,_b=_mk(_i);PW.append(_w);PB.append(_b)
b=[0]*128;side=0;cast=0;ep=-1;ks=[4,116]
def parse(fen):
    global side,cast,ep
    p=fen.split()
    for i in range(128): b[i]=0
    mp={'p':1,'n':2,'b':3,'r':4,'q':5,'k':6}
    for ri,row in enumerate(p[0].split('/')):
        r=7-ri;f=0
        for c in row:
            if c.isdigit(): f+=int(c)
            else:
                v=mp[c.lower()]+(0 if c.isupper() else 8)
                b[r*16+f]=v
                if v==6: ks[0]=r*16+f
                if v==14: ks[1]=r*16+f
                f+=1
    side=0 if p[1]=='w' else 1
    cast=0
    if len(p)>2:
        if 'K' in p[2]: cast|=1
        if 'Q' in p[2]: cast|=2
        if 'k' in p[2]: cast|=4
        if 'q' in p[2]: cast|=8
    ep=-1
    if len(p)>3 and p[3]!='-': ep=(ord(p[3][1])-49)*16+(ord(p[3][0])-97)
def atk(sq,byw):
    if byw:
        for d in (-15,-17):
            s=sq+d
            if 0<=s<128 and not s&0x88 and b[s]==1: return 1
    else:
        for d in (15,17):
            s=sq+d
            if 0<=s<128 and not s&0x88 and b[s]==9: return 1
    for d in KN:
        s=sq+d
        if 0<=s<128 and not s&0x88 and b[s]==(2 if byw else 10): return 1
    for d in KG:
        s=sq+d
        if 0<=s<128 and not s&0x88 and b[s]==(6 if byw else 14): return 1
    for d in BI:
        s=sq+d
        while 0<=s<128 and not s&0x88:
            p=b[s]
            if p:
                if p==(3 if byw else 11) or p==(5 if byw else 13): return 1
                break
            s+=d
    for d in RO:
        s=sq+d
        while 0<=s<128 and not s&0x88:
            p=b[s]
            if p:
                if p==(4 if byw else 12) or p==(5 if byw else 13): return 1
                break
            s+=d
    return 0
def gen(caponly):
    ms=[];us=side;them=1-us
    for sq in SQ:
        p=b[sq]
        if not p or (p>>3)!=us: continue
        t=p&7
        if t==1:
            d=16 if us==0 else -16
            one=sq+d
            if not one&0x88 and not b[one]:
                pr=(one>>4)==(7 if us==0 else 0)
                if not caponly: ms.append(sq|(one<<7)|((5<<14) if pr else 0))
                if not pr and (sq>>4)==(1 if us==0 else 6):
                    two=sq+2*d
                    if not b[two] and not caponly: ms.append(sq|(two<<7))
            for dd in (d-1,d+1):
                s2=sq+dd
                if s2&0x88: continue
                q=b[s2]
                if q and (q>>3)==them:
                    pr=(s2>>4)==(7 if us==0 else 0)
                    ms.append(sq|(s2<<7)|((5<<14) if pr else 0))
                elif s2==ep: ms.append(sq|(s2<<7))
        elif t==2:
            for d in KN:
                s2=sq+d
                if s2&0x88: continue
                q=b[s2]
                if not q:
                    if not caponly: ms.append(sq|(s2<<7))
                elif (q>>3)==them: ms.append(sq|(s2<<7))
        elif t==6:
            for d in KG:
                s2=sq+d
                if s2&0x88: continue
                q=b[s2]
                if not q:
                    if not caponly: ms.append(sq|(s2<<7))
                elif (q>>3)==them: ms.append(sq|(s2<<7))
            if not caponly:
                if us==0 and sq==4:
                    if cast&1 and not b[5] and not b[6] and b[7]==4 and not atk(4,0) and not atk(5,0) and not atk(6,0): ms.append(4|(6<<7))
                    if cast&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not atk(4,0) and not atk(3,0) and not atk(2,0): ms.append(4|(2<<7))
                if us==1 and sq==116:
                    if cast&4 and not b[117] and not b[118] and b[119]==12 and not atk(116,1) and not atk(117,1) and not atk(118,1): ms.append(116|(118<<7))
                    if cast&8 and not b[115] and not b[114] and not b[113] and b[112]==12 and not atk(116,1) and not atk(115,1) and not atk(114,1): ms.append(116|(114<<7))
        else:
            ds=BI if t==3 else RO if t==4 else BI+RO
            for d in ds:
                s2=sq+d
                while not s2&0x88:
                    q=b[s2]
                    if not q:
                        if not caponly: ms.append(sq|(s2<<7))
                    else:
                        if (q>>3)==them: ms.append(sq|(s2<<7))
                        break
                    s2+=d
    return ms
def make(m):
    global side,cast,ep
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7
    p=b[f];cap=b[t];csq=-1
    if (p&7)==1 and t==ep and not cap:
        csq=t+(-16 if side==0 else 16);cap=b[csq];b[csq]=0
    u=(m,cap,csq,cast,ep,ks[side])
    b[t]=p;b[f]=0
    if pr: b[t]=pr|(side<<3)
    if (p&7)==6:
        ks[side]=t
        if t-f==2: b[t-1]=b[t+1];b[t+1]=0
        elif f-t==2: b[t+1]=b[t-2];b[t-2]=0
    cast&=CK[f]&CK[t]
    ep=-1
    if (p&7)==1 and abs(t-f)==32: ep=(f+t)//2
    side^=1
    return u
def unmake(u):
    global side,cast,ep
    m,cap,csq,oc,oe,ok=u
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7
    side^=1
    p=b[t]
    if pr: p=1|(side<<3)
    b[f]=p;b[t]=0
    if cap:
        if csq>=0: b[csq]=cap
        else: b[t]=cap
    if (p&7)==6:
        ks[side]=ok
        if t-f==2: b[t+1]=b[t-1];b[t-1]=0
        elif f-t==2: b[t-2]=b[t+1];b[t+1]=0
    cast=oc;ep=oe
def legal(caponly=0):
    out=[]
    for m in gen(caponly):
        u=make(m)
        if not atk(ks[side^1],side==0): out.append(m)
        unmake(u)
    return out
def ev():
    s=0;ph=0;ked=0;wb=0;bb=0
    for sq in SQ:
        p=b[sq]
        if not p: continue
        t=p&7
        if p<8:
            s+=VAL[t]+PW[t][sq]
            if t==3: wb+=1
            if t==6: ked+=PW[7][sq]-PW[6][sq]
            ph+=PH[t]
        else:
            s-=VAL[t]+PB[t][sq]
            if t==3: bb+=1
            if t==6: ked-=PB[7][sq]-PB[6][sq]
            ph+=PH[t]
    if wb>1: s+=30
    if bb>1: s-=30
    if ph>24: ph=24
    s+=ked*(24-ph)//24
    sh=0
    for d in KG:
        q=ks[0]+d
        if 0<=q<128 and not q&0x88 and b[q]==1: sh+=1
        q=ks[1]+d
        if 0<=q<128 and not q&0x88 and b[q]==9: sh-=1
    s+=sh*12*ph//24
    return s if side==0 else -s
class TO(Exception): pass
N=0;TT={}
KL=[[0,0] for _ in range(128)]
def ordm(m,ply):
    t=(m>>7)&127;q=b[t]
    if q: return 1000000+VAL[q&7]*10-VAL[b[m&127]&7]
    if m==KL[ply][0] or m==KL[ply][1]: return 900000
    return 0
def srch(d,al,be,ply):
    global N,side,ep
    N+=1
    if N>LIM: raise TO
    key=None;e=None
    if d>0:
        key=bytes(b)+bytes((side,cast,ep+1))
        e=TT.get(key)
        if e and e[0]>=d:
            if e[1]==0: return e[2]
            if e[1]==1 and e[2]>=be: return e[2]
            if e[1]==2 and e[2]<=al: return e[2]
    chk=atk(ks[side],side==1)
    if d<=0: return qs(al,be,ply,chk)
    if chk: d+=1
    if d>=3 and not chk and be<99000:
        npm=0
        for sq in SQ:
            p=b[sq]
            if p and (p>>3)==side and 1<(p&7)<6: npm=1;break
        if npm:
            oe=ep;ep=-1;side^=1
            s=-srch(d-3,-be,-be+1,ply+1)
            side^=1;ep=oe
            if s>=be: return be
    ms=legal(0)
    if not ms: return -MATE+ply if chk else 0
    if e and e[3] in ms:
        ms.remove(e[3]);ms.insert(0,e[3])
    else: ms.sort(key=lambda m: ordm(m,ply),reverse=True)
    a0=al;best=-INF;bm=ms[0];fl=2
    for m in ms:
        u=make(m)
        s=-srch(d-1,-be,-al,ply+1)
        unmake(u)
        if s>best: best=s;bm=m
        if s>al: al=s
        if al>=be:
            if not u[1]:
                if m!=KL[ply][0]: KL[ply][1]=KL[ply][0];KL[ply][0]=m
            fl=1
            break
    if best>=be: fl=1
    elif best<=a0: fl=2
    else: fl=0
    TT[key]=(d,fl,best,bm)
    return best
def qs(al,be,ply,chk):
    global N
    N+=1
    if N>LIM: raise TO
    if chk:
        ms=legal(0)
        if not ms: return -MATE+ply
    else:
        st=ev()
        if st>=be: return be
        if st>al: al=st
        ms=legal(1)
        if not ms: return al
    ms.sort(key=lambda m: ordm(m,ply),reverse=True)
    for m in ms:
        u=make(m)
        s=-qs(-be,-al,ply+1,atk(ks[side],side==1))
        unmake(u)
        if s>=be: return be
        if s>al: al=s
    return al
def sqn(s): return "abcdefgh"[s&7]+str((s>>4)+1)
def uci(m):
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7
    return sqn(f)+sqn(t)+("q" if pr==5 else "")
def root(moves,seen=None):
    global N,side,cast,ep
    ms=legal(0)
    st=set(moves)
    cand=[m for m in ms if uci(m) in st]
    if not cand: return None
    if len(cand)==1: return cand[0]
    N=0;TT.clear()
    for i in range(128): KL[i][0]=0;KL[i][1]=0
    b0=list(b);s0=side;c0=cast;e0=ep;k0=list(ks)
    best=cand[0];sc={}
    for d in range(1,10):
        try:
            al=-INF;lb=cand[0];ls=-INF;sc={}
            for m in cand:
                u=make(m)
                s=-srch(d-1,-INF,-al,1)
                unmake(u)
                sc[m]=s
                if s>ls: ls=s;lb=m
                if s>al: al=s
            best=lb
            cand.remove(best);cand.insert(0,best)
        except TO:
            break
    # restore the root position: a TO abort leaves moves made mid-search
    b[:]=b0;side=s0;cast=c0;ep=e0;ks[:]=k0
    if seen:
        bb=best;bs=sc.get(best,-INF)
        for m in cand:
            s=sc.get(m)
            if s is None: continue
            u=make(m)
            k=bytes(b)+bytes((side,cast,ep+1))
            unmake(u)
            c=seen.get(k,0)
            if c>=2: s=min(s,0)
            elif c>=1: s-=20
            if s>bs: bs=s;bb=m
        best=bb
    return best
def seenkeys(moves):
    parse("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    d={}
    for mv in moves:
        f=(ord(mv[0])-97)+(ord(mv[1])-49)*16
        t=(ord(mv[2])-97)+(ord(mv[3])-49)*16
        pr=5 if len(mv)==5 and mv[4]=='q' else 0
        fm=None
        for m in legal(0):
            if (m&127)==f and ((m>>7)&127)==t and ((m>>14)&7)==pr: fm=m;break
        if fm is None: break
        make(fm)
        k=bytes(b)+bytes((side,cast,ep+1))
        d[k]=d.get(k,0)+1
    return d
def post(path,body):
    req=urllib.request.Request(U+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")
# === env loop ===
while True:
    g=post("/game",{})
    if g["status"]=="done": break
    while g["status"]=="your_move":
        sn=seenkeys(g.get("moves") or [])
        parse(g["fen"])
        m=root(g["legal_moves"],sn)
        mv=uci(m) if m is not None else g["legal_moves"][0]
        g=post("/move",{"game":g["game"],"move":mv})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
