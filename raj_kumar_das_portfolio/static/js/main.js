/* ==========================================================================
   Raj Kumar Das Portfolio - Main JavaScript Interactivity
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // --- 1. NAVBAR SCROLL EFFECT & ACTIVE LINK UPDATE ---
  const navbar = document.querySelector('.navbar-custom');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('shadow-lg');
    } else {
      navbar.classList.remove('shadow-lg');
    }

    let currentSection = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  });

  // Collapse mobile navbar on link click
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.querySelector('.navbar-collapse');
  if (navbarCollapse && navbarToggler) {
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (navbarCollapse.classList.contains('show')) {
          navbarToggler.click();
        }
      });
    });
  }

  // --- 2. PROJECT CATEGORY FILTERING ---
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-item');

  if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filterValue = btn.getAttribute('data-filter');

        projectCards.forEach(card => {
          const category = card.getAttribute('data-category');
          const techList = card.getAttribute('data-tech') || '';

          if (filterValue === 'all') {
            card.style.display = 'block';
          } else if (filterValue === 'Web' && category === 'Web') {
            card.style.display = 'block';
          } else if (filterValue === 'AI/ML' && category === 'AI/ML') {
            card.style.display = 'block';
          } else if (filterValue === 'Python' && techList.includes('Python')) {
            card.style.display = 'block';
          } else if (filterValue === 'Other' && category !== 'Web' && category !== 'AI/ML') {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // --- 3. CONTACT FORM SUBMISSION VIA AJAX ---
  const contactForm = document.getElementById('contactForm');
  const formFeedback = document.getElementById('formFeedback');
  const submitBtn = document.getElementById('submitBtn');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Clear previous alerts
      formFeedback.innerHTML = '';
      formFeedback.className = 'mt-3';

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const subject = document.getElementById('subject').value.trim();
      const message = document.getElementById('message').value.trim();
      const honeypot = document.getElementById('website_url') ? document.getElementById('website_url').value : '';

      // Client-side validation
      if (!name || !email || !subject || !message) {
        showFeedback('Please fill in all required fields.', 'danger');
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        showFeedback('Please provide a valid email address.', 'danger');
        return;
      }

      // UI Loading State
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Sending...';

      try {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('subject', subject);
        formData.append('message', message);
        formData.append('website_url', honeypot);

        const response = await fetch('/api/contact', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
          showFeedback(data.message, 'success');
          contactForm.reset();
        } else {
          showFeedback(data.message || 'Failed to send message. Please try again.', 'danger');
        }
      } catch (error) {
        console.error('Error submitting form:', error);
        showFeedback('A network error occurred. Please check your connection and try again.', 'danger');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    });
  }

  function showFeedback(msg, type) {
    if (!formFeedback) return;
    formFeedback.innerHTML = `
      <div class="alert alert-${type} alert-dismissible fade show border-0 shadow-sm" role="alert">
        <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
        ${msg}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
  }

  // --- 4. CODER MOTION ANIMATED BACKGROUND CANVAS ---
  const canvas = document.getElementById('coderBgCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const codeSnippets = ['01', '10', '</>', '{ }', 'def()', 'import', 'AI/ML', 'const', 'Flask', 'Python', '==>', 'SQL', 'C++', 'SIH'];
    const particles = [];
    const numParticles = 45;

    for (let i = 0; i < numParticles; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.8 - 0.2,
        text: codeSnippets[Math.floor(Math.random() * codeSnippets.length)],
        size: Math.floor(Math.random() * 8) + 12,
        alpha: Math.random() * 0.45 + 0.25
      });
    }

    function animateCoderBg() {
      ctx.clearRect(0, 0, width, height);

      // Draw faint cyber grid lines
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.05)';
      ctx.lineWidth = 1;
      const gridSize = 65;
      for (let x = 0; x < width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Draw code particles and connection links
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < -30) p.x = width + 30;
        if (p.x > width + 30) p.x = -30;
        if (p.y < -30) p.y = height + 30;
        if (p.y > height + 30) p.y = -30;

        // Render code snippet
        ctx.font = `${p.size}px "Fira Code", monospace`;
        ctx.fillStyle = `rgba(6, 182, 212, ${p.alpha})`;
        ctx.fillText(p.text, p.x, p.y);

        // Draw connections between close nodes
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            ctx.strokeStyle = `rgba(99, 102, 241, ${0.2 * (1 - dist / 130)})`;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(animateCoderBg);
    }

    animateCoderBg();
  }

});
