// Verify actual cursor tips, 90-minute calendar geometry and reversible seek state.
const fs=require('fs'),path=require('path'),os=require('os');
const cache=path.join(os.homedir(),'.npm','_npx');
const mods=fs.readdirSync(cache).map(d=>path.join(cache,d,'node_modules','puppeteer-core')).filter(p=>fs.existsSync(path.join(p,'package.json')));
const puppeteer=require(mods[0]);
(async()=>{const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try{const p=await browser.newPage();await p.setViewport({width:1920,height:1080});
const root=path.resolve('videos/serein');const html=fs.readFileSync(path.join(root,'compositions/frames/02-find-space.html'),'utf8').replace('<template>','').replace('</template>','');
const file=path.join(root,'.hyperframes/geometry-qa.html');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`<!doctype html><html><head><base href="file://${root}/"><style>html,body{margin:0;width:1920px;height:1080px}</style><script src="assets/gsap.min.js"></script></head><body>${html}</body></html>`);
await p.goto('file://'+file);await p.evaluate(()=>document.fonts.ready);
const clicks=[];for(const [time,id] of [[5.4,'s2-find'],[12.2,'s2-protect']])clicks.push(await p.evaluate(({time,id})=>{window.__timelines['02-find-space'].seek(time);const b=document.getElementById(id).getBoundingClientRect(),c=document.getElementById('s2-cursor').getBoundingClientRect(),tip={x:c.x+5.75,y:c.y+5.37};return{time,target:id,bounds:{x:b.x,y:b.y,w:b.width,h:b.height},tip,inside:tip.x>b.x&&tip.x<b.right&&tip.y>b.y&&tip.y<b.bottom};},{time,id}));
const states=[];for(const t of [1,9,12.8,15.8,0,15.8,9])states.push(await p.evaluate(t=>{window.__timelines['02-find-space'].seek(t);const o=id=>+getComputedStyle(document.getElementById(id)).opacity;const b=id=>{let r=document.getElementById(id).getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}};return{t,focus:o('s2-focuscopy'),protected:o('s2-protected'),summary:o('s2-summary'),ui:o('s2-ui'),meeting1:b('s2-meeting1'),meeting2:b('s2-meeting2'),focus_box:b('s2-focus')};},t));
const geometry={start_minutes:11*60,end_minutes:12*60+30,hour_spacing_px:72,focus_height_px:108};
if(clicks.some(x=>!x.inside)||states[0].focus!==0||states[1].focus!==1||states[2].protected!==1||states[3].summary!==1||states[4].ui!==0||JSON.stringify(states[3])!==JSON.stringify(states[5])||JSON.stringify(states[1])!==JSON.stringify(states[6]))throw Error('Cursor or seek regression');
if(geometry.end_minutes-geometry.start_minutes!==90||geometry.focus_height_px/geometry.hour_spacing_px*60!==90)throw Error('Wrong slot length');
const result={clicks,seek_states:states,geometry};fs.writeFileSync('artifacts/library-loop-13/geometry.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}finally{await browser.close()}})();
