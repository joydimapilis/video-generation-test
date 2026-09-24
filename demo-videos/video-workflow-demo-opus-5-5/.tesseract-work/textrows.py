import subprocess, sys, array
f, x0, y0, x1, y1 = sys.argv[1], *map(int, sys.argv[2:6]); inv = len(sys.argv) > 6 and sys.argv[6] == 'inv'
w, h = x1 - x0, y1 - y0
raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", f, "-vf", f"crop={w}:{h}:{x0}:{y0},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
a = array.array('B', raw)
bg = sorted(a)[len(a)//2]
thr = 60
rows = []
for y in range(h):
    r = a[y*w:(y+1)*w]
    xs = [i for i, v in enumerate(r) if abs(v - bg) > thr]
    rows.append((xs[0], xs[-1]) if len(xs) > 2 else None)
y = 0
while y < h:
    if rows[y]:
        s = y; xa, xb = rows[y]
        while y < h and rows[y]:
            xa = min(xa, rows[y][0]); xb = max(xb, rows[y][1]); y += 1
        if y - s >= 6: print(f"y {y0+s}-{y0+y} (h{y-s})  x {x0+xa}-{x0+xb}")
    y += 1
