const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
async function s(f,w,h,out){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+__dirname+'/'+f);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:90});await p.close();}
await s('og.html',1200,630,'out-og.jpg');for(let i=1;i<=5;i++)await s('ig'+i+'.html',1080,1350,'out-ig'+i+'.jpg');await b.close();})();
