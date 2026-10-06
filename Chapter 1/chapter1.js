// Dua Toggle
(function(){
  var btn = document.getElementById('duaToggle');
  var content = document.getElementById('duaContent');
  if(!btn || !content) return;
  btn.addEventListener('click', function(){
    var expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    content.style.display = expanded ? 'none' : 'block';
  });
})();

// TOC Smooth Scroll
document.querySelectorAll('.toc-item').forEach(function(link){
  link.addEventListener('click', function(e){
    e.preventDefault();
    var target = document.querySelector(this.getAttribute('href'));
    if(target){
      target.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });
});

// Solution Toggle for Q-sections
function toggleSolution(btn){
  var solution = btn.nextElementSibling;
  if(!solution) return;
  var isVisible = solution.style.display === 'block';
  solution.style.display = isVisible ? 'none' : 'block';
  var arrow = btn.querySelector('.q-arrow');
  if(arrow) arrow.style.transform = isVisible ? '' : 'rotate(180deg)';
  btn.innerHTML = isVisible ? 'عرض الحل الكامل <span class="q-arrow">▼</span>' : 'إخفاء الحل <span class="q-arrow" style="transform:rotate(180deg)">▼</span>';
}

// Eye Protection Toggle
(function(){
  var KEY='eyeProtection', root=document.documentElement, btn=document.getElementById('eyeToggle');
  if(!btn) return;
  var st=btn.querySelector('.eye-st');
  function render(on){ btn.setAttribute('aria-pressed', on?'true':'false'); st.textContent = on?'ON':'OFF'; }
  render(root.getAttribute('data-eye')==='on');
  btn.addEventListener('click', function(){
    var on = root.getAttribute('data-eye') !== 'on';
    if(on){ root.setAttribute('data-eye','on'); } else { root.removeAttribute('data-eye'); }
    render(on);
    try{ localStorage.setItem(KEY, on?'on':'off'); }catch(e){}
  });
})();
