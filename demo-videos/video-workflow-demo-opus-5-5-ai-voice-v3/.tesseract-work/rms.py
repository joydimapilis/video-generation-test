import subprocess,sys,math,array
def rms_profile(path,start,dur,win=0.01,sr=48000):
    raw=subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-ss",str(start),"-t",str(dur),"-i",path,"-ac","1","-ar",str(sr),"-f","s16le","-"],capture_output=True).stdout
    a=array.array('h',raw); n=int(sr*win); out=[]
    for i in range(0,len(a)-n+1,n):
        s=sum(x*x for x in a[i:i+n])/n
        out.append(20*math.log10(math.sqrt(s)/32768+1e-9))
    return out
if __name__=="__main__":
    p,st,du=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); win=float(sys.argv[4]) if len(sys.argv)>4 else 0.01
    prof=rms_profile(p,st,du,win)
    for i,d in enumerate(prof):
        t=st+i*win
        bar="#"*max(0,int((d+70)/2))
        print(f"{t:7.2f} {d:6.1f} {bar}")
