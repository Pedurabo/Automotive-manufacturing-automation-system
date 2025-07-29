document.addEventListener('DOMContentLoaded', function() {
  // Auto-dismiss flash messages after 4 seconds
  const flash = document.querySelector('.flash-messages');
  if (flash) {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s';
      flash.style.opacity = 0;
      setTimeout(() => flash.remove(), 500);
    }, 4000);
  }

  // Notification system
  window.showNotification = function(msg, timeout=4000) {
    let notif = document.querySelector('.notification-area');
    if (!notif) {
      notif = document.createElement('div');
      notif.className = 'notification-area';
      document.body.appendChild(notif);
    }
    notif.textContent = msg;
    notif.classList.add('active');
    setTimeout(() => {
      notif.classList.remove('active');
    }, timeout);
  }

  // Add more global JS as needed
}); 