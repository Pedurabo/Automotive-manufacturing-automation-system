document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('.login-form');
  const passwordInput = document.querySelector('input[type="password"]');
  const toggleBtn = document.createElement('button');
  toggleBtn.type = 'button';
  toggleBtn.textContent = 'Show';
  toggleBtn.className = 'toggle-password';
  toggleBtn.style.marginLeft = '8px';

  if (passwordInput) {
    passwordInput.parentNode.appendChild(toggleBtn);
    toggleBtn.addEventListener('click', function() {
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = 'Hide';
      } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = 'Show';
      }
    });
  }

  if (form) {
    form.addEventListener('submit', function(e) {
      const username = form.querySelector('input[name="username"]');
      const password = form.querySelector('input[name="password"]');
      if (!username.value.trim() || !password.value.trim()) {
        e.preventDefault();
        showFlash('Please enter both username and password.');
        return false;
      }
      const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
    });
  }

  function showFlash(msg) {
    let flash = document.querySelector('.flash-messages');
    if (!flash) {
      flash = document.createElement('div');
      flash.className = 'flash-messages';
      form.parentNode.insertBefore(flash, form.nextSibling);
    }
    flash.textContent = msg;
  }
}); 