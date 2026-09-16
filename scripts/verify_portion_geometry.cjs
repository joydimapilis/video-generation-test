// Check the exact on-screen product actions, totals and deterministic replay.
const fs=require('fs'),path=require('path'),os=require('os');
const cache=path.join(os.homedir(),'.npm','_npx');
const mods=fs.readdirSync(cache).map(d=>path.join(cache,d,'node_modules','puppeteer-core')).filter(p=>fs.existsSync(path.join(p,'package.json')));
const puppeteer=require(mods[0]);
(async()=>{const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});try{
const p=await browser.newPage();await p.setViewport({width:1920,height:1080});const root=path.resolve('videos/portion');
let html=fs.readFileSync(path.join(root,'index.html'),'utf8').replace('<script src="assets/gsap.min.js"></script>','<script src="assets/gsap.min.js"></script><script>window.__timelines={};</script>');
html=html.replace('<head>','<head><base href="file://'+root+'/">');fs.mkdirSync(path.join(root,'.hyperframes'),{recursive:true});
const file=path.join(root,'.hyperframes/geometry-qa.html');fs.writeFileSync(file,html);await p.goto('file://'+file);await p.evaluate(()=>document.fonts.ready);
const clicks=[];for(const [t,target] of [[6.55,'#manual .cell:nth-child(5)'],[8.02,'#manual .cell:nth-child(6)'],[9.3,'#manual .cell:nth-child(8)'],[14.05,'#build-btn'],[22.98,'#send-btn']])clicks.push(await p.evaluate(({t,target})=>{window.__timelines.main.seek(t);const b=document.querySelector(target).getBoundingClientRect(),c=document.getElementById('cursor').getBoundingClientRect();const point={x:c.x+6.25,y:c.y+5.83};return{t,target,point,bounds:{x:b.x,y:b.y,w:b.width,h:b.height},inside:point.x>b.x&&point.x<b.right&&point.y>b.y&&point.y<b.bottom};},{t,target}));
const capture=async(t)=>p.evaluate(t=>{window.__timelines.main.seek(t);const ids=['typed-5','typed-3','typed-2','manual','app-chrome','empty-state','build-btn','progress','result','send-btn','cursor-pulse'];const values=Object.fromEntries(ids.map(id=>[id,+getComputedStyle(document.getElementById(id)).opacity]));return{t,values,orders:[0,1,2].map(i=>{const r=document.getElementById('order-'+i).getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}})};},t);
const baseline=[];for(const t of [0,5.4,8.4,12,15.5,17.5,20,23.9])baseline.push(await capture(t));
const replay=[];for(const t of [23.9,8.4,0,20,5.4,17.5,12,15.5])replay.push(await capture(t));
if(clicks.some(x=>!x.inside))throw Error('Cursor misses click target: '+JSON.stringify(clicks));
for(const r of replay){const b=baseline.find(b=>b.t===r.t);if(JSON.stringify(r)!==JSON.stringify(b))throw Error('Seek state is not repeatable at '+r.t)}
if(baseline[0].values['cursor-pulse']!==0||baseline[3].values.result!==0||baseline[5].values.result!==1||baseline[7].values['send-btn']!==0)throw Error('Unexpected UI state');
const orders=JSON.parse(fs.readFileSync(path.join(root,'orders.json')));const totals={chicken:orders.reduce((s,o)=>s+o.chicken,0),tofu:orders.reduce((s,o)=>s+o.tofu,0)};
if(totals.chicken!==13||totals.tofu!==11||orders.find(x=>x.name==='Book Club').note!=='Sauce on the side')throw Error('Bad totals or lost packing note');
fs.writeFileSync('artifacts/library-loop-15/geometry.json',JSON.stringify({clicks,totals,bowls:24,packing_note_preserved:true,baseline,replay,passed:true},null,2));console.log('Five cursor targets, 24-bowl arithmetic, packing note and reverse seeking passed.');
}finally{await browser.close()}})();
