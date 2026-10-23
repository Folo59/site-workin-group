const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
async function s(f,w,h,out){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+__dirname+'/'+f);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:92});await p.close();}
await s('fb.html',1640,624,'banniere-facebook.jpg');await s('li.html',2256,382,'banniere-linkedin.jpg');await s('ig.html',1080,1080,'photo-profil-instagram.jpg');await b.close();})();
