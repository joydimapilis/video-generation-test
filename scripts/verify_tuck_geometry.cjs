// Check the actual SVG pointer tip against both controls in authored scene coordinates.
const fs=require('fs'),path=require('path'),os=require('os');
const cache=path.join(os.homedir(),'.npm','_npx');
const modules=fs.readdirSync(cache).map(d=>path.join(cache,d,'node_modules','puppeteer-core')).filter(p=>fs.existsSync(path.join(p,'package.json')));
const puppeteer=require(modules[0]);
(async()=>{const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try {const p=await browser.newPage();await p.setViewport({width:1920,height:1080});
 const root=path.resolve('videos/tuck');const frame=fs.readFileSync(path.join(root,'compositions/frames/02-report.html'),'utf8').replace('<template>','').replace('</template>','');
 const qa=path.join(root,'.hyperframes/geometry-qa.html');fs.writeFileSync(qa,`<!doctype html><html><head><base href="file://${root}/"><style>html,body{margin:0;width:1920px;height:1080px}</style><script src="assets/gsap.min.js"></script></head><body>${frame}</body></html>`);
 await p.goto('file://'+qa);await p.evaluate(()=>document.fonts.ready);const rows=[];
 for(const [time,id]of[[2.2,'t2-extract'],[9.2,'t2-create']]) rows.push(await p.evaluate(({time,id})=>{window.__timelines['02-report'].seek(time);const b=document.getElementById(id).getBoundingClientRect(),c=document.getElementById('t2-cursor').getBoundingClientRect();const tip={x:c.x+6.75,y:c.y+6.3};return {time,target:id,bounds:{x:b.x,y:b.y,w:b.width,h:b.height},tip,inside:tip.x>=b.x&&tip.x<=b.right&&tip.y>=b.y&&tip.y<=b.bottom};},{time,id}));
 const states=[];for(const t of [1,5,11.8,0,11.8,5])states.push(await p.evaluate(t=>{window.__timelines['02-report'].seek(t);const op=id=>+getComputedStyle(document.getElementById(id)).opacity;return{time:t,row:op('t2-row2'),report:op('t2-report'),ui:op('t2-ui')};},t));
 const result={clicks:rows,seek_states:states,example_total_cents:640+2400+14800};fs.writeFileSync('artifacts/library-loop-12/cursor-targets.json',JSON.stringify(result,null,2)+'\n');console.log(result);
 if(rows.some(r=>!r.inside)||states[0].row!==0||states[1].row!==1||states[2].report!==1||states[3].ui!==0||JSON.stringify(states[1])!==JSON.stringify(states[5]))throw Error('Geometry/state regression');

}finally{await browser.close()}})();
