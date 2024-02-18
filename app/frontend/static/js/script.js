// Dynamic DataTable Initialization
$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});

// Call setup functions based on screen size
if (window.innerWidth >= 768) {
  // Desktop
  setupDesktopSidebar();
} else {
  // Mobile
  setupMobileSidebar();
}

// Desktop Sidebar State Handling
function setupDesktopSidebar() {
  const hamBurgerDesktop = document.querySelector(".toggle-btn-desktop");
  const sidebarDesktop = document.querySelector("#sidebar");

  const isSidebarExpanded =
    localStorage.getItem("isSidebarExpanded") === "true";

  if (isSidebarExpanded) {
    sidebarDesktop.classList.add("expand");
  }

  hamBurgerDesktop.addEventListener("click", function () {
    sidebarDesktop.classList.toggle("expand");

    localStorage.setItem(
      "isSidebarExpanded",
      sidebarDesktop.classList.contains("expand")
    );
  });
}

// Mobile Sidebar State Handling
function setupMobileSidebar() {
  const toggleBtnMobile = document.querySelector(".toggle-btn-mobile");
  const sidebarMobile = document.querySelector("#sidebar");

  const isSidebarExpandedMobile =
    localStorage.getItem("isSidebarExpandedMobile") === "true";

  if (isSidebarExpandedMobile) {
    sidebarMobile.classList.add("expand");
  }

  toggleBtnMobile.addEventListener("click", function () {
    sidebarMobile.classList.toggle("expand");

    localStorage.setItem(
      "isSidebarExpandedMobile",
      sidebarMobile.classList.contains("expand")
    );

    // Update sidebar display based on expansion state
    if (sidebarMobile.classList.contains("expand")) {
      sidebarMobile.style.display = "block"; // Show sidebar when expanding
    } else {
      sidebarMobile.style.display = "none"; // Hide sidebar when collapsing
    }
  });

  // Optional: Close sidebar when clicking outside of it
  document.addEventListener("click", function (event) {
    if (
      !sidebarMobile.contains(event.target) &&
      !toggleBtnMobile.contains(event.target)
    ) {
      sidebarMobile.classList.remove("expand");
      sidebarMobile.style.display = "none"; // Hide sidebar when collapsing
    }
  });
}
