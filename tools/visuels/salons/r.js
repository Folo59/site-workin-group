const { chromium } = require('playwright');const L=require('./list.json');
(async()=>{const b=await chromium.launch();for(const [n,[w,h]] of Object.entries(L)){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+__dirname+'/'+n+'.html');await p.waitForTimeout(300);await p.screenshot({path:'out-'+n+'.jpg',type:'jpeg',quality:90});await p.close();}await b.close()})();
