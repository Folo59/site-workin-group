// node frames.js states.json outdir  → rend chaque état en PNG 1080x1920 (ou 1080x1350 si state.h)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
 const states=JSON.parse(fs.readFileSync(process.argv[2]));const out=process.argv[3];
 const b=await chromium.launch();
 const pages={};
 async function page(h){ if(!pages[h]){const pg=await b.newPage({viewport:{width:1080,height:h}});
   await pg.goto('file://'+path.join(__dirname,'tpl.html'));
   await pg.addStyleTag({content:`html,body{height:${h}px!important}`});
   await pg.evaluate(()=>document.fonts.ready); pages[h]=pg;} return pages[h]; }
 for(let i=0;i<states.length;i++){
   const s=states[i]; const pg=await page(s.h||1920);
   await pg.evaluate(d=>render(d),s); await pg.evaluate(()=>document.fonts.ready);
   await pg.screenshot({path:path.join(out,s.file||`s${String(i).padStart(4,'0')}.png`),type:s.file&&s.file.endsWith('.jpg')?'jpeg':'png',quality:s.file&&s.file.endsWith('.jpg')?92:undefined});
 }
 await b.close();
})();
