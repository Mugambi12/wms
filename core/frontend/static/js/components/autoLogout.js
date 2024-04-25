let inactivityTimeout;

function resetInactivityTimer() {
  clearTimeout(inactivityTimeout);
  inactivityTimeout = setTimeout(redirectAfterInactivity, 600000); // 10 minutes in milliseconds
}

function redirectAfterInactivity() {
  window.location.href = "/";
  localStorage.clear();
}

// Add event listeners for user activity
document.addEventListener("mousemove", resetInactivityTimer);
document.addEventListener("keypress", resetInactivityTimer);
document.addEventListener("scroll", resetInactivityTimer);
