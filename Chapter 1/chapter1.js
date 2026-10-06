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

// ===== TASK COMPLETION SYSTEM =====
(function(){
  var STORAGE_KEY = 'ch1_tasks';
  var TOTAL_TASKS = 17;
  var messages = [
    'استمر! 🔥', 'عاش! كمل كده 👏', 'أحسنت! 💪',
    'مهمة خلصت، واحدة كمان! 🚀', 'جامد جدًا! ⭐', 'Keep going! 🔥',
    'ممتاز! 🌟', 'يلا نكمل! 💥', 'برافو عليك! 🎯'
  ];

  // Load saved state
  function loadState(){
    try{
      var s = localStorage.getItem(STORAGE_KEY);
      return s ? JSON.parse(s) : {};
    } catch(e){ return {}; }
  }
  function saveState(state){
    try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e){}
  }

  // Update progress bar
  function updateProgress(state){
    var count = Object.keys(state).filter(function(k){ return state[k]; }).length;
    var fill = document.getElementById('progressFill');
    var text = document.getElementById('progressText');
    if(fill) fill.style.width = (count / TOTAL_TASKS * 100) + '%';
    if(text) text.textContent = count + ' / ' + TOTAL_TASKS + ' Tasks';
    return count;
  }

  // Mini confetti burst
  function miniConfetti(x, y){
    var canvas = document.getElementById('confettiCanvas');
    if(!canvas){
      canvas = document.createElement('canvas');
      canvas.id = 'confettiCanvas';
      document.body.appendChild(canvas);
    }
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');
    var colors = ['#1ABC9C','#2E86C1','#F0B429','#E74C3C','#9B59B6','#FF6B6B','#48C9B0'];
    var particles = [];
    for(var i = 0; i < 35; i++){
      particles.push({
        x: x, y: y,
        vx: (Math.random() - 0.5) * 12,
        vy: (Math.random() - 0.7) * 12,
        w: Math.random() * 8 + 4,
        h: Math.random() * 6 + 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 15,
        gravity: 0.3,
        life: 1
      });
    }
    var frame;
    function animate(){
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var alive = false;
      particles.forEach(function(p){
        if(p.life <= 0) return;
        alive = true;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.rotation += p.rotSpeed;
        p.life -= 0.018;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation * Math.PI / 180);
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
        ctx.restore();
      });
      if(alive) frame = requestAnimationFrame(animate);
      else ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    animate();
  }

  // Big confetti for chapter completion
  function bigConfetti(){
    var canvas = document.getElementById('confettiCanvas');
    if(!canvas){
      canvas = document.createElement('canvas');
      canvas.id = 'confettiCanvas';
      document.body.appendChild(canvas);
    }
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');
    var colors = ['#1ABC9C','#2E86C1','#F0B429','#E74C3C','#9B59B6','#FF6B6B','#48C9B0','#FFD700','#FF69B4'];
    var particles = [];
    for(var i = 0; i < 120; i++){
      particles.push({
        x: Math.random() * canvas.width,
        y: -20 - Math.random() * 200,
        vx: (Math.random() - 0.5) * 6,
        vy: Math.random() * 3 + 2,
        w: Math.random() * 10 + 5,
        h: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 10,
        gravity: 0.08,
        life: 1
      });
    }
    function animate(){
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var alive = false;
      particles.forEach(function(p){
        if(p.life <= 0) return;
        alive = true;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.rotation += p.rotSpeed;
        p.life -= 0.006;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation * Math.PI / 180);
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
        ctx.restore();
      });
      if(alive) requestAnimationFrame(animate);
      else ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    animate();
  }

  // Show motivational message
  function showMessage(btn){
    var old = btn.parentNode.querySelector('.task-msg');
    if(old) old.remove();
    var msg = document.createElement('span');
    msg.className = 'task-msg';
    msg.textContent = messages[Math.floor(Math.random() * messages.length)];
    btn.parentNode.appendChild(msg);
    setTimeout(function(){
      msg.style.animation = 'msgFade .4s ease forwards';
      setTimeout(function(){ msg.remove(); }, 400);
    }, 2000);
  }

  // Init
  var state = loadState();
  var buttons = document.querySelectorAll('.task-check');
  buttons.forEach(function(btn){
    var taskId = btn.getAttribute('data-task');
    var section = document.getElementById(taskId);
    // Restore saved state
    if(state[taskId]){
      btn.classList.add('completed');
      if(section) section.classList.add('task-done');
    }
    btn.addEventListener('click', function(){
      var isCompleted = btn.classList.contains('completed');
      if(isCompleted){
        // Uncomplete
        btn.classList.remove('completed');
        if(section) section.classList.remove('task-done');
        state[taskId] = false;
      } else {
        // Complete
        btn.classList.add('completed');
        if(section) section.classList.add('task-done');
        state[taskId] = true;
        // Confetti
        var rect = btn.getBoundingClientRect();
        miniConfetti(rect.left + rect.width/2, rect.top + rect.height/2);
        // Message
        showMessage(btn);
      }
      saveState(state);
      var count = updateProgress(state);
      // Chapter complete?
      if(count >= TOTAL_TASKS){
        var banner = document.getElementById('chapterBanner');
        if(banner) banner.style.display = 'block';
        setTimeout(bigConfetti, 300);
      } else {
        var banner = document.getElementById('chapterBanner');
        if(banner) banner.style.display = 'none';
      }
    });
  });
  updateProgress(state);
  // Check if already all complete on load
  var initialCount = Object.keys(state).filter(function(k){ return state[k]; }).length;
  if(initialCount >= TOTAL_TASKS){
    var banner = document.getElementById('chapterBanner');
    if(banner) banner.style.display = 'block';
  }
})();
