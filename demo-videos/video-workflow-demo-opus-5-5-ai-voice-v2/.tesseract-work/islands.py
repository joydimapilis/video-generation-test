import sys
from rms import rms_profile
p=sys.argv[1]; st=float(sys.argv[2]); du=float(sys.argv[3]); thr=float(sys.argv[4]) if len(sys.argv)>4 else -45; mingap=float(sys.argv[5]) if len(sys.argv)>5 else 0.12
prof=rms_profile(p,st,du,0.01)
on=[d>thr for d in prof]
# islands with gaps >= mingap
isl=[];cur=None;gap=0
for i,v in enumerate(on):
    t=st+i*0.01
    if v:
        if cur is None: cur=[t,t]
        cur[1]=t+0.01; gap=0
    elif cur is not None:
        gap+=0.01
        if gap>=mingap: isl.append(cur);cur=None;gap=0
if cur: isl.append(cur)
prev=None
for a,b in isl:
    g=f"gap {a-prev:.2f}" if prev is not None else ""
    print(f"{a:7.2f}-{b:7.2f} ({b-a:.2f}) {g}"); prev=b
