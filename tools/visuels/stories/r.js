const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const f of ['qui-1','qui-2','qui-3','qui-4','post-1','post-2','post-3','post-4','cover-qui','cover-postuler','cover-offres','cover-permis','cover-installation','cover-confiance']){await p.goto('file://'+__dirname+'/'+f+'.html');await p.waitForTimeout(250);await p.screenshot({path:'out-'+f+'.jpg',type:'jpeg',quality:90});}
await b.close()})();
