/* Xưởng Vibe — tầng review. Animation vừa đủ, không trình diễn.
   Tôn trọng prefers-reduced-motion ở mọi hiệu ứng. */
(function(){'use strict';
var K='vibe-doc-theme',R=matchMedia('(prefers-reduced-motion: reduce)').matches;
function get(){try{return localStorage.getItem(K)}catch(e){return null}}
function set(v){try{localStorage.setItem(K,v)}catch(e){}}
var s=get(); if(s)document.documentElement.setAttribute('data-theme',s);

function theme(){var b=document.getElementById('t');if(!b)return;
  function lab(){var l=document.documentElement.getAttribute('data-theme')==='light';
    b.textContent=l?'tối':'sáng';b.setAttribute('aria-label',l?'Nền tối':'Nền sáng')}
  lab();b.onclick=function(){var l=document.documentElement.getAttribute('data-theme')==='light';
    var n=l?'dark':'light';document.documentElement.setAttribute('data-theme',n);set(n);lab()}}

function bar(){var e=document.getElementById('bar');if(!e)return;var q=false;
  function u(){var h=document.documentElement.scrollHeight-innerHeight;
    e.style.width=Math.min(100,Math.max(0,h>0?scrollY/h*100:0))+'%';q=false}
  addEventListener('scroll',function(){if(!q){q=true;requestAnimationFrame(u)}},{passive:true});u()}

function reveal(){var n=document.querySelectorAll('.r');
  if(R||!('IntersectionObserver'in window)){n.forEach(function(e){e.classList.add('on')});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;
    var d=e.target.getAttribute('data-d');e.target.style.transitionDelay=(d?+d:0)+'ms';
    e.target.classList.add('on');io.unobserve(e.target)})},
    {rootMargin:'0px 0px -7% 0px',threshold:.05});
  n.forEach(function(e){io.observe(e)})}

function count(){var n=document.querySelectorAll('[data-to]');if(!n.length)return;
  function f(v,d){return v.toLocaleString('vi-VN',{minimumFractionDigits:d,maximumFractionDigits:d})}
  function go(e){var to=parseFloat(e.getAttribute('data-to')),
    d=(e.getAttribute('data-to').split('.')[1]||'').length,
    sf=e.getAttribute('data-sfx')||'',pf=e.getAttribute('data-pfx')||'';
    if(R){e.textContent=pf+f(to,d)+sf;return}
    var t0=null;function st(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/780);
      e.textContent=pf+f(to*(1-Math.pow(1-k,3)),d)+sf;
      if(k<1)requestAnimationFrame(st);else e.textContent=pf+f(to,d)+sf}
    requestAnimationFrame(st)}
  if(!('IntersectionObserver'in window)){n.forEach(go);return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){go(e.target);io.unobserve(e.target)}})},{threshold:.5});
  n.forEach(function(e){io.observe(e)})}

function nav(){var h=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('nav a[href]').forEach(function(a){
    if(a.getAttribute('href')===h)a.setAttribute('aria-current','page')})}

/* Đếm chữ thật và IN RA — ngân sách là thứ nhìn thấy được, không phải lời hứa. */
function budget(){var m=document.querySelector('.meta .words');if(!m)return;
  var c=document.querySelector('main'); if(!c)return;
  var t=c.innerText.replace(/\s+/g,' ').trim();
  var w=t?t.split(' ').length:0;
  m.textContent=w+' từ · ~'+Math.max(1,Math.round(w/180))+' phút';
  if(w>520)m.classList.add('hot')}

function lang(){var navIn=document.querySelector('nav .in');if(!navIn)return;
  var q=new URLSearchParams(location.search),ql=q.get('lang'),st='';
  try{st=localStorage.getItem('wms-lang')||''}catch(_){}
  var cur=(ql==='en'||ql==='vi')?ql:(st==='en'||st==='vi'?st:'vi');
  var grp=document.createElement('div');grp.className='doc-lang';grp.setAttribute('role','group');
  grp.setAttribute('aria-label','Language / Ngôn ngữ');
  var bVi=document.createElement('button');bVi.type='button';bVi.textContent='VI';bVi.setAttribute('data-doc-lang','vi');
  var bEn=document.createElement('button');bEn.type='button';bEn.textContent='EN';bEn.setAttribute('data-doc-lang','en');
  grp.appendChild(bVi);grp.appendChild(bEn);
  var tBtn=document.getElementById('t');
  if(tBtn&&tBtn.parentNode===navIn)navIn.insertBefore(grp,tBtn);else navIn.appendChild(grp);
  var mainEl=document.querySelector('main'),footEl=document.querySelector('footer');
  var origTitle=document.title,origMain=mainEl?mainEl.innerHTML:'',origFoot=footEl?footEl.innerHTML:'';
  var navLinks=Array.from(navIn.querySelectorAll('a')).map(function(a){return{el:a,vi:a.textContent}});
  var NAV_EN={'Tổng quan S0':'Overview S0','S0 Khảo cứu':'S0 Research','Trắc nghiệm AI':'AI Quiz',
    'Tổng quan DuysLab':'DuysLab Overview','S1 Spec':'S1 Spec','S2 Design':'S2 Design',
    'S3 Build':'S3 Build','S4 QA':'S4 QA','S5 Launch':'S5 Launch','S6 Iterate':'S6 Iterate',
    'Prototype':'Prototype','Mở Prototype':'Open Prototype','Studio':'Studio','Sơ đồ Agent':'Agent Workflows'};
  function syncThemeText(){var b=document.getElementById('t');if(!b)return;var v=b.textContent.trim();
    if(cur==='en'){if(v==='sáng')b.textContent='light';else if(v==='tối')b.textContent='dark'}
    else{if(v==='light')b.textContent='sáng';else if(v==='dark')b.textContent='tối'}}
  if(tBtn)tBtn.addEventListener('click',function(){setTimeout(syncThemeText,0)});
  function updateWords(l){var m=document.querySelector('.meta .words');if(!m||!mainEl)return;
    var w=(mainEl.innerText||'').trim().split(/\s+/).filter(Boolean).length;
    m.textContent=l==='en'?(w+' words · ~'+Math.max(1,Math.round(w/180))+' min'):(w+' từ · ~'+Math.max(1,Math.round(w/180))+' phút')}
  function apply(l){cur=l==='en'?'en':'vi';document.documentElement.lang=cur;
    try{localStorage.setItem('wms-lang',cur)}catch(_){}
    try{var u=new URL(location.href);u.searchParams.set('lang',cur);history.replaceState(null,'',u.toString())}catch(_){}
    bVi.setAttribute('aria-pressed',String(cur==='vi'));bEn.setAttribute('aria-pressed',String(cur==='en'));
    navLinks.forEach(function(item){var tx=item.vi.trim();
      item.el.textContent=cur==='en'?(NAV_EN[tx]||tx):item.vi;
      var h=item.el.getAttribute('href');
      if(h&&h.endsWith('.html')){try{var nu=new URL(h,location.href);nu.searchParams.set('lang',cur);
        item.el.setAttribute('href',h.split('?')[0]+nu.search)}catch(_){}}});
    var enPack=window.VIBE_DOC_EN;
    if(enPack){if(cur==='en'){if(enPack.title)document.title=enPack.title;
      if(mainEl&&enPack.main)mainEl.innerHTML=enPack.main;
      if(footEl&&enPack.footer)footEl.innerHTML=enPack.footer}
      else{document.title=origTitle;if(mainEl)mainEl.innerHTML=origMain;if(footEl)footEl.innerHTML=origFoot}}
    if(mainEl)mainEl.querySelectorAll('.r').forEach(function(el){el.classList.add('v')});
    try{count()}catch(_){}
    updateWords(cur);syncThemeText()}
  bVi.onclick=function(){apply('vi')};bEn.onclick=function(){apply('en')};
  if(cur==='en'||window.VIBE_DOC_EN)apply(cur);else{bVi.setAttribute('aria-pressed','true');bEn.setAttribute('aria-pressed','false')}}
function init(){theme();bar();reveal();count();nav();budget();lang()}
document.readyState==='loading'?addEventListener('DOMContentLoaded',init):init();
})();
