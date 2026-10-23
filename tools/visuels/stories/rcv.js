const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const f of ['cover-qui','cover-postuler','cover-offres','cover-permis','cover-installation','cover-confiance','cover-canada']){await p.goto('file://'+__dirname+'/'+f+'.html');await p.waitForTimeout(200);await p.screenshot({path:'out-'+f+'.jpg',type:'jpeg',quality:92});}
await b.close()})();
