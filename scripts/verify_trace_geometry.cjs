// Use the Puppeteer shipped with a locally cached HyperFrames CLI.
const fs=require('fs'),path=require('path'),os=require('os');
const cache=path.join(os.homedir(),'.npm','_npx');
const packages=fs.readdirSync(cache).map(d=>path.join(cache,d,'node_modules','puppeteer-core')).filter(p=>fs.existsSync(path.join(p,'package.json')));
if(!packages.length)throw new Error('Run npx hyperframes check once to install the browser tools.');
const puppeteer=require(packages[0]);
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
 try{
 const p=await browser.newPage();await p.setViewport({width:1920,height:1080});await p.goto('file://'+process.cwd()+'/hyperframes/trace/index.html');await p.evaluate(()=>document.fonts.ready);
 const rows=[];
 for(const [time,id]of[[10.5,'record-button'],[12.45,'place-order'],[23.2,'share-button']]){
 rows.push(await p.evaluate(({time,id})=>{
 window.__timelines.trace.seek(time);
 const b=document.getElementById(id).getBoundingClientRect(),c=document.getElementById('demo-cursor').getBoundingClientRect();
 const tip={x:c.x+5.5,y:c.y+5.1};return{time,target:id,bounds:{x:b.x,y:b.y,w:b.width,h:b.height},tip,inside:tip.x>=b.x&&tip.x<=b.right&&tip.y>=b.y&&tip.y<=b.bottom};
 },{time,id}));
 }
 fs.writeFileSync('artifacts/library-loop-10/cursor-targets.json',JSON.stringify(rows,null,2)+'\n');console.log(rows);
 if(rows.some(r=>!r.inside))process.exitCode=1;
 }finally{await browser.close()}
})();
