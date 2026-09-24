import json,sys
for fn in sys.argv[1:]:
    d=json.load(open(fn))
    print("==",fn)
    line=[]
    for s in d["transcription"]:
        t=s["text"].strip()
        if not t: continue
        a=s["offsets"]["from"]/1000; b=s["offsets"]["to"]/1000
        line.append(f"{t}[{a:.2f}-{b:.2f}]")
    print(" ".join(line))
