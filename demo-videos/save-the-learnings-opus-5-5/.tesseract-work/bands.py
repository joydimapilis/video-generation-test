import subprocess,sys
W,H=3164,1930
X0,X1=640,2300
def bands(t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i','../Assets/Screen-Recording.mov','-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    rows=[]
    for y in range(H):
        r=raw[y*W+X0:y*W+X1]
        xs=[i for i,v in enumerate(r) if v>140]
        rows.append((len(xs), (min(xs)+X0, max(xs)+X0) if xs else None))
    out=[];y=0
    while y<H:
        if rows[y][0]>3:
            y0=y; xmin=9999;xmax=0;tot=0
            while y<H and rows[y][0]>3:
                xmin=min(xmin,rows[y][1][0]); xmax=max(xmax,rows[y][1][1]); tot+=rows[y][0]; y+=1
            out.append((y0,y,xmin,xmax,tot))
        else: y+=1
    return out
for t in sys.argv[1:]:
    print('== t',t)
    for y0,y1,a,b,tot in bands(float(t)):
        if y1-y0>=26 and (b-a)<700: print(f"  y {y0}-{y1} h{y1-y0} x {a}-{b} dens {tot/(y1-y0)/(b-a+1):.3f}")
