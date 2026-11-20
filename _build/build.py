"""Ricostruisce l'app pubblica 3PP (GitHub Pages) dall'HTML dell'artifact.
uso (dalla radice del repository):  python3 _build/build.py live.html
Le immagini sono in assets/<blob_id>.<ext>. Se manca un asset, esce con codice 2
ed elenca gli id: scaricali con read_asset (artifact de209ef8-5118-4fa1-b86b-4a3cd3e4f4d2)
e salvali in assets/<id>.<ext>, poi rilancia.
"""
import sys, os, re, shutil, json, hashlib
src = sys.argv[1]
HERE0 = os.path.dirname(os.path.abspath(__file__))
out = os.path.dirname(HERE0)
base = 'https://points3productionssrls.github.io/'
HERE = os.path.dirname(os.path.abspath(__file__))
h = open(src).read()

# assets already in the repo: assets/<id>.<ext>
AD = os.path.join(out, 'assets'); os.makedirs(AD, exist_ok=True)
have = {os.path.splitext(f)[0]: f for f in os.listdir(AD)}
used = set(re.findall(r'/_blob/([0-9a-f]{32})', h))
missing = sorted(u for u in used if u not in have)
if missing:
    print('MISSING_ASSETS ' + ' '.join(missing)); sys.exit(2)
for bid in used:
    h = h.replace('/_blob/' + bid, 'assets/' + have[bid])
for f in list(have.values()):
    if os.path.splitext(f)[0] not in used: os.remove(os.path.join(AD, f))

# head tags
head = f'''<script>window.__3PP_STANDALONE=true</script>
<meta name="description" content="3 Points Productions · casa di produzione cinematografica italo-americana in Sicilia. Listino, preventivi, progetti, laboratori nelle scuole e contatti.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="3PP">
<meta property="og:type" content="website">
<meta property="og:title" content="3 Points Productions">
<meta property="og:description" content="Film production · Sicilia. Listino 2026, preventivo in pochi tocchi, progetti e contatti.">
<meta property="og:image" content="{base}og.jpg">
<meta property="og:url" content="{base}">
<meta name="twitter:card" content="summary_large_image">
'''
assert h.count('<meta charset="utf-8">') == 1
h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + head, 1)

# install prompt + service worker (public build only)
inst = r'''<script>
/* contatore anonimo aperture app 3PP (nessun cookie, nessun dato personale) */
(function(){try{
 if(sessionStorage.getItem('3pp_seen'))return;sessionStorage.setItem('3pp_seen','1');
 const d=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome'}).format(new Date()).replace(/-/g,'');
 const B='https://abacus.jasoncameron.dev/hit/3pp-srls-app/';
 [B+'totale',B+'g-'+d].forEach(u=>fetch(u,{mode:'cors',keepalive:true}).catch(()=>{}));
}catch(e){}})();
</script>
<style>
.x-inst{position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:60;display:flex;align-items:center;gap:12px;padding:12px 14px;background:#111;border:1px solid #ffffff2a;border-radius:16px;box-shadow:0 10px 40px #000a;font:500 13px var(--fb,'Work Sans',sans-serif);color:#fff}
.x-inst img{width:36px;height:36px;border-radius:9px}.x-inst b{display:block;font-size:13px}.x-inst span{color:#aaa;font-size:12px}
.x-inst .go{margin-left:auto;background:#fff;color:#000;border:0;border-radius:999px;padding:8px 14px;font:600 11px var(--fh,'Work Sans',sans-serif);letter-spacing:.12em;text-transform:uppercase}
.x-inst .cl{background:none;border:0;color:#888;font-size:20px;padding:0 2px}
@media(min-width:900px){.x-inst{left:auto;right:24px;bottom:24px;width:380px}}
</style>
<script>
(function(){
 if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
 const lg=()=>{try{return JSON.parse(localStorage.getItem('3pp_lang'))||'it'}catch(e){return 'it'}};
 const T=(a,b)=>lg()=='en'?b:a;
 const standalone=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone;
 if(standalone)return;
 let dismissed=false;try{dismissed=+localStorage.getItem('3pp_inst_x')>Date.now()}catch(e){}
 if(dismissed)return;
 const ios=/iphone|ipad|ipod/i.test(navigator.userAgent)&&!window.MSStream;
 let evt=null;
 function show(){if(document.querySelector('.x-inst'))return;const d=document.createElement('div');d.className='x-inst';
  d.innerHTML=`<img src="icons/icon-192.png" alt=""><div><b>${T('Installa l\'app 3PP','Install the 3PP app')}</b><span>${T('Gratis, sulla schermata Home','Free, on your Home screen')}</span></div><button class="go">${T('Installa','Install')}</button><button class="cl" aria-label="Chiudi">×</button>`;
  d.querySelector('.cl').onclick=()=>{d.remove();try{localStorage.setItem('3pp_inst_x',Date.now()+7*864e5)}catch(e){}};
  d.querySelector('.go').onclick=async()=>{if(evt){evt.prompt();try{await evt.userChoice}catch(e){}d.remove();evt=null}else{d.remove();help()}};
  document.body.appendChild(d)}
 function help(){const s=document.createElement('div');s.className='x-sheet';s.id='x-sh';s.onclick=e=>{if(e.target===s)s.remove()};
  s.innerHTML=`<div><button class="x-x" onclick="this.closest('.x-sheet').remove()">×</button><div class="x-eye">${T('Installa l\'app','Install the app')}</div><h3 class="x-h2" style="font-size:28px">3 Points Productions</h3>`+
  (ios?`<p class="x-p">1. ${T('Tocca il pulsante <b>Condividi</b> in basso nella barra di Safari','Tap the <b>Share</b> button at the bottom of Safari')} (□↑)<br>2. ${T('Scorri e scegli <b>«Aggiungi alla schermata Home»</b>','Scroll and choose <b>«Add to Home Screen»</b>')}<br>3. ${T('Tocca <b>Aggiungi</b>','Tap <b>Add</b>')}</p>`
      :`<p class="x-p">1. ${T('Apri il menu del browser','Open the browser menu')} (⋮)<br>2. ${T('Scegli <b>«Installa app»</b> o <b>«Aggiungi a schermata Home»</b>','Choose <b>«Install app»</b> or <b>«Add to Home screen»</b>')}</p>`)+
  `<p class="x-mu">${T('L\'icona 3PP comparirà sulla Home e l\'app si aprirà a schermo intero.','The 3PP icon will appear on your Home screen and the app will open full screen.')}</p></div>`;
  (document.getElementById('x')||document.body).appendChild(s)}
 window.x3install=()=>{if(evt){evt.prompt()}else help()};
 window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();evt=e;setTimeout(show,4000)});
 if(ios)setTimeout(show,6000);
})();
</script>
'''
assert h.rstrip().endswith('</html>')
i = h.rfind('</body>')
h = h[:i] + inst + h[i:]

# the "install" card in Contatti opens the install help in the public build
h = h.replace("""<div class="x-card" style="margin-top:12px;display:flex;gap:14px;align-items:center">${mk()}""",
              """<div class="x-card" style="margin-top:12px;display:flex;gap:14px;align-items:center;cursor:pointer" onclick="window.x3install&&x3install()">${mk()}""", 1)

open(os.path.join(out, 'index.html'), 'w').write(h)

# manifest, sw, icons
shutil.copytree(os.path.join(HERE, 'icons'), os.path.join(out, 'icons'), dirs_exist_ok=True)
man = {"name": "3 Points Productions", "short_name": "3PP", "description": "Listino, preventivi, progetti, scuole e contatti di 3 Points Productions.",
       "lang": "it", "start_url": "./#home", "scope": "./", "display": "standalone", "orientation": "portrait",
       "background_color": "#000000", "theme_color": "#000000", "categories": ["entertainment", "business", "photo"],
       "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                 {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                 {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
json.dump(man, open(os.path.join(out, 'manifest.webmanifest'), 'w'), ensure_ascii=False, indent=1)
ver = hashlib.sha1(h.encode()).hexdigest()[:10]
sw = """const C='3pp-%s';const A=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||r.headers.get('range'))return;const u=new URL(r.url);
 if(u.origin===location.origin){if(/\\.mp4$/.test(u.pathname))return;
  if(/\\/assets\\//.test(u.pathname)){e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res})));return}
  e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r).then(m=>m||caches.match('./index.html'))))}
 else if(/fonts\\.(googleapis|gstatic)\\.com/.test(u.host)){e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res})))}});
""" % ver
open(os.path.join(out, 'sw.js'), 'w').write(sw)
shutil.copyfile(os.path.join(HERE, 'og.jpg'), os.path.join(out, 'og.jpg'))
open(os.path.join(out, '.nojekyll'), 'w').write('')
open(os.path.join(out, '404.html'), 'w').write('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./"><title>3 Points Productions</title>')
print('built', out, 'assets', len(used), 'version', ver)
