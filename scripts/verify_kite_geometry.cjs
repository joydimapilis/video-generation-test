const fs=require('fs'),path=require('path');
const {chromium}=require('../.context/browser-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({headless:true,channel:'chrome'});
 try{
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.addInitScript(()=>{window.__timelines={};});
  await p.goto('file://'+path.resolve('videos/kite/index.html'));
  await p.evaluate(()=>document.fonts.ready);
  const result=await p.evaluate(()=>{
   const errors=[],states=[];
   const seek=t=>{
    window.__timelines['kite-film'].seek(t,false);
    document.querySelectorAll('.clip').forEach(el=>{
     const s=+el.dataset.start,e=s+(+el.dataset.duration);
     el.style.visibility=t>=s&&t<e?'visible':'hidden';
    });
   };
   const opacity=el=>{let v=1;while(el&&el!==document){const s=getComputedStyle(el);if(s.visibility==='hidden'||s.display==='none')return 0;v*=+s.opacity;el=el.parentElement;}return v;};
   for(let f=0;f<1260;f++){
    const t=f/30;seek(t);
    for(const el of document.querySelectorAll('[data-essential],.caption')){
     if(opacity(el)<.05||!el.textContent.trim()&&el.tagName!=='image')continue;
     const r=el.getBoundingClientRect();
     if(r.left<107||r.right>973||r.top<689||r.bottom>1231)errors.push({frame:f,time:t,text:el.textContent||'logo',bounds:{x:r.x,y:r.y,w:r.width,h:r.height}});
    }
   }
   for(const t of [9.8,35.2,1,35.2,9.8]){
    seek(t);states.push({t,request:document.querySelector('#request-first').textContent+' '+document.querySelector('#request-last').textContent,decision:document.querySelector('#approval-draft').textContent});
   }
   return {frames_checked:1260,crop_safe_rectangle:[108,690,864,540],errors,states};
  });
  fs.writeFileSync('artifacts/kite/video-geometry.json',JSON.stringify(result,null,2));
  console.log(JSON.stringify({frames:result.frames_checked,errors:result.errors.length,examples:result.errors.slice(0,4),states:result.states}));
  if(result.errors.length)process.exitCode=1;
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
