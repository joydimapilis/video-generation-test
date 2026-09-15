// Check the actual SVG pointer tip against both controls in authored scene coordinates.
const fs=require('fs'),path=require('path'),os=require('os');
const cache=path.join(os.homedir(),'.npm','_npx');
const modules=fs.readdirSync(cache).map(d=>path.join(cache,d,'node_modules','puppeteer-core')).filter(p=>fs.existsSync(path.join(p,'package.json')));
const puppeteer=require(modules[0]);
(async()=>{const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try {const p=await browser.newPage();await p.setViewport({width:1920,height:1080});
 const root=path.resolve('videos/fold');const frame=fs.readFileSync(path.join(root,'compositions/frames/02-direction.html'),'utf8').replace('<template>','').replace('</template>','');
 const qa=path.join(root,'.hyperframes/geometry-qa.html');fs.writeFileSync(qa,`<!doctype html><html><head><base href="file://${root}/"><style>html,body{margin:0;width:1920px;height:1080px}</style><script src="assets/gsap.min.js"></script></head><body>${frame}</body></html>`);
 await p.goto('file://'+qa);await p.evaluate(()=>document.fonts.ready);const rows=[];
 for(const [time,id]of[[1.7,'f2-organize'],[7.4,'f2-human']]) rows.push(await p.evaluate(({time,id})=>{window.__timelines['02-direction'].seek(time);const b=document.getElementById(id).getBoundingClientRect(),c=document.getElementById('f2-cursor').getBoundingClientRect();const tip={x:c.x+7,y:c.y+6.533};return {time,target:id,bounds:{x:b.x,y:b.y,w:b.width,h:b.height},tip,inside:tip.x>=b.x&&tip.x<=b.right&&tip.y>=b.y&&tip.y<=b.bottom};},{time,id}));
 const states=[];for(const t of [4.9,8.6,0,8.6,4.9])states.push(await p.evaluate(t=>{window.__timelines['02-direction'].seek(t);const op=id=>+getComputedStyle(document.getElementById(id)).opacity;return{time:t,formal:op('f2-formalcopy'),human:op('f2-humancopy'),ui:op('f2-ui')};},t));
 const result={clicks:rows,seek_states:states};fs.writeFileSync('artifacts/library-loop-11/cursor-targets.json',JSON.stringify(result,null,2)+'\n');console.log(result);
 if(rows.some(r=>!r.inside)||states[0].formal!==1||states[1].human!==1||states[1].formal!==0||states[2].ui!==0||JSON.stringify(states[0])!==JSON.stringify(states[4]))throw Error('Geometry/state regression');
}finally{await browser.close()}})();
