import json
from pathlib import Path
r=Path(__file__).resolve().parent
p=r/'editable.json';d=json.loads(p.read_text());d['duration']=20;d['dimensions']={'width':1920,'height':1080}
def tf(x,y,s=100):return {'position':[x,y],'anchorPoint':[0,0],'scale':[s,s],'rotation':0,'opacity':100}
l=[]
def visual(i,name,start,end,x,y,s,asset,src=None):
 v={'type':'Image' if src is None else 'Video','id':i,'name':name,'blendMode':'normal','activeRange':{'start':start,'duration':end-start},'transform':tf(x,y,s),'source':{'assetId':asset,'fit':'contain'}}
 if src is not None:v.update(sourceRange={'start':src,'duration':end-start},sourceIntrinsicDuration=29766,volume=0)
 l.append(v)
visual(1,'Document introduction — source 0.0–0.7s',0,700,-610,-180,106,'screen',0)
visual(2,'Hold document title — original frame 0.7s',700,5000,-610,-180,106,'title-hold')
visual(3,'Recorded structure scroll — source 1.4–4.27s',5000,7870,-610,-180,106,'screen',1400)
visual(4,'Hold original prompts — source frame 7.0s',7870,11140,-610,-825,106,'prompts-hold')
visual(5,'Revisions and learnings — source frame 7.65s',11140,13550,-610,-305,106,'revisions-hold')
visual(6,'Document file and verification context — source 8–14.45s',13550,20000,-500,-90,82,'screen',8000)
l.append({'type':'Audio','id':50,'name':'Original narration — trimmed head and tail; +2.2 dB','activeRange':{'start':0,'duration':20000},'sourceRange':{'start':2050,'duration':20000},'sourceIntrinsicDuration':23253,'source':{'assetId':'narration'},'volume':10**(2.2/20),'captionsEnabled':False})
d['composition']['layers']=l
p.write_text(json.dumps(d,indent=2))
a=[]
a.append({'type':'createFxRectLayer','compositionId':'main','layerId':100,'name':'Caption safe area','insertIndex':0,'activeRange':{'start':0,'duration':20000},'transform':tf(0,934),'rect':{'size':[1920,146],'fillColor':[0.027,0.033,0.043,1]}})
# Phrase starts follow local transcription of the actual trimmed recording.
caps=[(230,1800,'For every finished video,'),(1800,3160,'the system creates its own'),(3160,5000,'reverse-engineering document.'),(5000,7870,'This records how the video was made,'),(7870,10180,'including the prompts, structure,'),(10180,11840,'methods used, revisions,'),(11840,13200,'and key learnings.'),(13500,15100,'The workflow also checks that'),(15100,16150,'this file exists'),(16150,17490,'before the video can be'),(17490,19200,'marked complete.')]
for i,(start,end,txt) in enumerate(caps,200):
 a.append({'type':'createFxTextLayer','compositionId':'main','layerId':i,'name':f'Caption: {txt}','insertIndex':0,'activeRange':{'start':start,'duration':end-start},'transform':tf(100,978),'sourceText':{'text':txt,'fontFamily':'Lato','fontStyle':'Regular','fontSize':46,'fillColor':[1,1,1,1],'justification':'center','boxText':True,'boxPosition':[0,0],'boxSize':[1720,80]}})
# Very short boundary ramps affect only the retained silent handles.
for prop,values in [('volume',[(0,0),(60,10**(2.2/20)),(19700,10**(2.2/20)),(19999,0)])]:
 a.append({'type':'setFxPropertyKeyframes','compositionId':'main','property':{'layerId':50,'propertyType':prop},'keyframes':[{'id':f'voice-{t}','layerTime':t,'value':{'type':'float','value':v},'easing':{'type':'linear'}} for t,v in values]})
if (r/'refinement.json').exists(): a.extend(json.loads((r/'refinement.json').read_text()))
(r/'actions.json').write_text(json.dumps(a,indent=2))
(r/'captions.json').write_text(json.dumps(caps,indent=2))
def time(ms):
 h,rem=divmod(ms,3600000);m,rem=divmod(rem,60000);s,milli=divmod(rem,1000);return f'{h:02}:{m:02}:{s:02},{milli:03}'
(r.parent/'Captions.srt').write_text('\n\n'.join(f'{i}\n{time(s)} --> {time(e)}\n{t}' for i,(s,e,t) in enumerate(caps,1))+'\n')
