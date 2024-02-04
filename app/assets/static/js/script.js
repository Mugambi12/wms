// const hamBurger = document.querySelector(".toggle-btn");
//
// hamBurger.addEventListener("click", function () {
//   document.querySelector("#sidebar").classList.toggle("expand");
// });

const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.querySelector("#sidebar");

// Check if the sidebar state is stored in localStorage
const isSidebarExpanded = localStorage.getItem("isSidebarExpanded") === "true";

// Set the initial state based on localStorage
if (isSidebarExpanded) {
  sidebar.classList.add("expand");
}

hamBurger.addEventListener("click", function () {
  sidebar.classList.toggle("expand");

  // Update the localStorage to reflect the current sidebar state
  localStorage.setItem(
    "isSidebarExpanded",
    sidebar.classList.contains("expand")
  );
});
