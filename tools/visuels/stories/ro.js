const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const f of ['offre-0','offre-1','offre-2','offre-3','offre-4','offre-5']){await p.goto('file://'+__dirname+'/'+f+'.html');await p.waitForTimeout(250);await p.screenshot({path:'out-'+f+'.jpg',type:'jpeg',quality:90});}
await b.close()})();
