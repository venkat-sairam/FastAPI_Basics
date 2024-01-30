// script.js
document.addEventListener("DOMContentLoaded", function () {
  // Function to show/hide tab content
  function showTab(tabId) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll(".tab-content");
    tabContents.forEach((content) => {
      content.classList.remove("active");
    });

    // Show the selected tab content
    const selectedTab = document.getElementById(tabId);
    selectedTab.classList.add("active");
  }

  // Add click event listeners to navbar links
  const navbarLinks = document.querySelectorAll(".nav-link");
  navbarLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const targetId = link.getAttribute("href").substring(1);
      showTab(targetId);
    });
  });
});
