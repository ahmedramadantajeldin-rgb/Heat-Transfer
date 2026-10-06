// Dua toggle
(function(){
var btn=document.getElementById('duaToggle');
var content=document.getElementById('duaContent');
if(!btn||!content) return;
btn.addEventListener('click',function(){
var expanded=btn.getAttribute('aria-expanded')==='true';
btn.setAttribute('aria-expanded',expanded?'false':'true');
content.style.display=expanded?'none':'block';
});
})();

// Solution toggles
function toggleSolution(btn){
var answer=btn.nextElementSibling;
if(!answer) return;
var visible=answer.style.display==='block';
answer.style.display=visible?'none':'block';
btn.textContent=visible?'عرض الحل الكامل ▼':'إخفاء الحل ▲';
}

// Smooth scroll for TOC
document.querySelectorAll('.toc-item').forEach(function(a){
a.addEventListener('click',function(e){
e.preventDefault();
var target=document.querySelector(a.getAttribute('href'));
if(target){
target.scrollIntoView({behavior:'smooth',block:'start'});
}
});
});

// Eye protection toggle
(function(){
var KEY='eyeProtection',root=document.documentElement,btn=document.getElementById('eyeToggle');
if(!btn) return;
var st=btn.querySelector('.eye-st');
function render(on){btn.setAttribute('aria-pressed',on?'true':'false');st.textContent=on?'ON':'OFF';}
render(root.getAttribute('data-eye')==='on');
btn.addEventListener('click',function(){
var on=root.getAttribute('data-eye')!=='on';
if(on){root.setAttribute('data-eye','on');}else{root.removeAttribute('data-eye');}
render(on);
try{localStorage.setItem(KEY,on?'on':'off');}catch(e){}
});
})();
