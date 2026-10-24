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

function init(){theme();bar();reveal();count();nav();budget()}
document.readyState==='loading'?addEventListener('DOMContentLoaded',init):init();
})();
