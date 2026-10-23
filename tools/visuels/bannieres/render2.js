const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
async function s(f,w,h,out){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+__dirname+'/'+f);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:92});await p.close();}
await s('txt-fb.html',1640,624,'facebook-texte.jpg');await s('txt-li.html',2256,382,'linkedin-texte.jpg');await s('ph-fb.html',1640,624,'facebook-photo.jpg');await s('ph-li.html',2256,382,'linkedin-photo.jpg');await b.close();})();
