// Define the mobile/desktop breakpoint

const MOBILE_BREAKPOINT = 768;

function handleResize() {
  const screenWidth = window.innerWidth;

  if (
    (screenWidth >= MOBILE_BREAKPOINT &&
      window.prevWidth < MOBILE_BREAKPOINT) ||
    (screenWidth < MOBILE_BREAKPOINT && window.prevWidth >= MOBILE_BREAKPOINT)
  ) {
    location.reload();
  }

  window.prevWidth = screenWidth;
}

handleResize();

window.addEventListener("resize", handleResize);
