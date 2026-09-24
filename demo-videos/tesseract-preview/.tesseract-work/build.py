import json
from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'editable.json'
d=json.loads(p.read_text()); d['dimensions']={'width':1920,'height':1080}; d['composition']['name']='Reykjavik setup preview'
p.write_text(json.dumps(d,indent=2))
a=[]
def transform(x,y): return {'anchorPoint':[0,0],'position':[x,y],'scale':[100,100],'rotation':0,'opacity':100}
def rect(i,name,x,y,w,h,color):
 a.append({'type':'createFxRectLayer','compositionId':'main','layerId':i,'name':name,'insertIndex':0,'activeRange':{'start':0,'duration':3000},'transform':transform(x,y),'rect':{'size':[w,h],'fillColor':color}})
def text(i,name,x,y,size,color):
 a.append({'type':'createFxTextLayer','compositionId':'main','layerId':i,'name':name,'insertIndex':0,'activeRange':{'start':0,'duration':3000},'transform':transform(x,y),'sourceText':{'text':name,'fontFamily':'Abel','fontStyle':'Regular','fontSize':size,'fillColor':color,'justification':'left','boxText':True,'boxPosition':[0,0],'boxSize':[1300,180]}})
def keys(i,prop,values):
 a.append({'type':'setFxPropertyKeyframes','compositionId':'main','property':{'layerId':i,'propertyType':prop},'keyframes':[{'id':f'{i}-{prop}-{t}','layerTime':t,'value':{'type':'float','value':v},'easing':{'type':'cubicBezier','x1':0.2,'y1':0,'x2':0.2,'y2':1}} for t,v in values]})
rect(1,'Ink background',0,0,1920,1080,[0.035,0.055,0.09,1])
rect(2,'Motion rail',160,720,1600,3,[0.2,0.3,0.38,1])
rect(3,'Moving mint marker',160,699,44,44,[0.4,1,0.8,1])
text(4,'TESSERACT',160,320,160,[0.95,0.97,1,1])
text(5,'Editable motion. Local rendering.',166,530,54,[0.65,0.77,0.84,1])
text(6,'REYKJAVIK  /  WORKSPACE PREVIEW',164,190,32,[0.4,1,0.8,1])
keys(3,'positionX',[(0,160),(1500,1716),(2300,1716),(2967,160)])
keys(4,'positionY',[(0,365),(600,320),(2400,320),(2967,300)])
keys(4,'opacity',[(0,0),(500,100),(2400,100),(2967,0)])
keys(5,'opacity',[(0,0),(250,0),(750,100),(2400,100),(2967,0)])
(root/'actions.json').write_text(json.dumps(a,indent=2))
