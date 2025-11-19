/**
 * BlogSpot - Main JavaScript File
 * Handles navigation, sticky header, mobile menu, form validation, and active link highlighting
 */

(function () {
  "use strict";

  // Helper Functions
  const $ = (selector, context = document) => context.querySelector(selector);
  const $$ = (selector, context = document) => Array.from(context.querySelectorAll(selector));
  const on = (element, event, handler) => {
    if (element) {
      element.addEventListener(event, handler);
    }
  };

  // Initialize when DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    // Get elements
    const header = $(".header-area");
    const navbar = $(".navbar");
    const navToggle = "[data-nav-toggle]";
    const toggleBtn = $(navToggle);

    // =============================
    // 1. Sticky Header on Scroll
    // =============================
    const handleScroll = () => {
      if (!header) return;
      
      if (window.scrollY > 50) {
        header.classList.add("sticky-header");
      } else {
        header.classList.remove("sticky-header");
      }
    };

    // Initial check
    handleScroll();
    
    // Listen to scroll events
    on(window, "scroll", handleScroll);

    // =============================
    // 2. Mobile Menu Toggle
    // =============================
    if (toggleBtn && navbar) {
      on(toggleBtn, "click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        
        navbar.classList.toggle("open");
        
        // Change icon
        if (navbar.classList.contains("open")) {
          toggleBtn.innerHTML = '<i class="fas fa-times"></i>';
          toggleBtn.setAttribute("aria-label", "Menyunu bağla");
        } else {
          toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
          toggleBtn.setAttribute("aria-label", "Menyunu aç");
        }
      });
    }

    // =============================
    // 3. Close Menu on Link Click (Mobile)
    // =============================
    if (navbar) {
      const navLinks = $$(".navbar .nav a");
      navLinks.forEach((link) => {
        on(link, "click", () => {
          if (navbar.classList.contains("open")) {
            navbar.classList.remove("open");
            if (toggleBtn) {
              toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
              toggleBtn.setAttribute("aria-label", "Menyunu aç");
            }
          }
        });
      });
    }

    // =============================
    // 4. Close Menu on ESC Key
    // =============================
    on(document, "keydown", (e) => {
      if (e.key === "Escape" && navbar && navbar.classList.contains("open")) {
        navbar.classList.remove("open");
        if (toggleBtn) {
          toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
          toggleBtn.setAttribute("aria-label", "Menyunu aç");
        }
      }
    });

    // =============================
    // 5. Close Menu on Click Outside
    // =============================
    on(document, "click", (e) => {
      if (navbar && navbar.classList.contains("open")) {
        if (!navbar.contains(e.target) && !toggleBtn.contains(e.target)) {
          navbar.classList.remove("open");
          if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            toggleBtn.setAttribute("aria-label", "Menyunu aç");
          }
        }
      }
    });

    // =============================
    // 6. Active Link Highlighting (Moved to section 18)
    // =============================

    // =============================
    // 8. Smooth Scroll for Anchor Links
    // =============================
    const anchorLinks = $$('a[href^="#"]');
    anchorLinks.forEach((link) => {
      on(link, "click", (e) => {
        const href = link.getAttribute("href");
        
        if (href !== "#" && href.length > 1) {
          const target = $(href);
          
          if (target) {
            e.preventDefault();
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
              top: offsetPosition,
              behavior: "smooth"
            });
          }
        }
      });
    });

    // =============================
    // 9. Image Lazy Loading (Optional Enhancement)
    // =============================
    const images = $$("img[data-src]");
    if (images.length > 0 && "IntersectionObserver" in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute("data-src");
            observer.unobserve(img);
          }
        });
      });

      images.forEach((img) => imageObserver.observe(img));
    }

    // =============================
    // 10. Search Functionality
    // =============================
    const searchToggle = $(".search-toggle");
    const searchBox = $(".search-box");
    const searchInput = $("#search-input");
    const searchClose = $(".search-close");
    const searchResultsModal = $("#search-results");
    const searchResultsList = $("#search-results-list");
    const searchResultsClose = $(".search-results-close");

    // Toggle search box
    if (searchToggle && searchBox) {
      on(searchToggle, "click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        searchBox.classList.toggle("active");
        if (searchBox.classList.contains("active")) {
          searchInput.focus();
        }
      });
    }

    // Close search box
    if (searchClose && searchBox) {
      on(searchClose, "click", () => {
        searchBox.classList.remove("active");
        if (searchInput) {
          searchInput.value = "";
        }
      });
    }

    // Close search box on outside click
    on(document, "click", (e) => {
      if (searchBox && !searchBox.contains(e.target) && !searchToggle.contains(e.target)) {
        searchBox.classList.remove("active");
      }
    });

    // Search functionality
    if (searchInput) {
      let searchTimeout;
      on(searchInput, "input", (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim().toLowerCase();

        if (query.length > 2) {
          searchTimeout = setTimeout(() => {
            performSearch(query);
          }, 300);
        } else {
          if (searchResultsModal) {
            searchResultsModal.classList.remove("active");
          }
        }
      });

      on(searchInput, "keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          const query = searchInput.value.trim().toLowerCase();
          if (query.length > 2) {
            performSearch(query);
          }
        }
        if (e.key === "Escape") {
          if (searchResultsModal) {
            searchResultsModal.classList.remove("active");
          }
          if (searchBox) {
            searchBox.classList.remove("active");
          }
        }
      });
    }

    // Perform search
    function performSearch(query) {
      const posts = $$(".card[data-category], article[data-category]");
      const results = [];

      posts.forEach((post) => {
        const title = post.querySelector(".card-title, h3");
        const text = post.querySelector(".card-text, p");
        const category = post.getAttribute("data-category") || "";
        const tags = post.getAttribute("data-tags") || "";

        const searchableText = `
          ${title ? title.textContent : ""}
          ${text ? text.textContent : ""}
          ${category}
          ${tags}
        `.toLowerCase();

        if (searchableText.includes(query)) {
          results.push({
            element: post,
            title: title ? title.textContent : "Post",
            text: text ? text.textContent : "",
            link: post.querySelector("a")?.href || "#"
          });
        }
      });

      displaySearchResults(results, query);
    }

    // Display search results
    function displaySearchResults(results, query) {
      if (!searchResultsModal || !searchResultsList) return;

      searchResultsList.innerHTML = "";

      if (results.length === 0) {
        searchResultsList.innerHTML = `
          <div class="search-result-item">
            <p>Heç bir nəticə tapılmadı. "${query}" üçün axtarış edin.</p>
          </div>
        `;
      } else {
        results.forEach((result) => {
          const item = document.createElement("div");
          item.className = "search-result-item";
          item.innerHTML = `
            <h4><a href="${result.link}">${result.title}</a></h4>
            <p>${result.text.substring(0, 150)}...</p>
          `;
          searchResultsList.appendChild(item);
        });
      }

      searchResultsModal.classList.add("active");
    }

    // Close search results modal
    if (searchResultsClose) {
      on(searchResultsClose, "click", () => {
        if (searchResultsModal) {
          searchResultsModal.classList.remove("active");
        }
      });
    }

    on(document, "click", (e) => {
      if (searchResultsModal && e.target === searchResultsModal) {
        searchResultsModal.classList.remove("active");
      }
    });

    // =============================
    // 11. Dark Mode Toggle
    // =============================
    const darkModeToggle = $(".dark-mode-toggle");
    const isDarkMode = localStorage.getItem("darkMode") === "true";

    // Apply dark mode on load
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
      if (darkModeToggle) {
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
      }
    }

    // Toggle dark mode
    if (darkModeToggle) {
      on(darkModeToggle, "click", () => {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        
        localStorage.setItem("darkMode", isDark);
        darkModeToggle.innerHTML = isDark 
          ? '<i class="fas fa-sun"></i>' 
          : '<i class="fas fa-moon"></i>';
      });
    }

    // =============================
    // 12. Category Filtering
    // =============================
    const categoryLinks = $$(".category-list a[data-filter]");
    const postsGrid = $("#posts-grid");

    categoryLinks.forEach((link) => {
      on(link, "click", (e) => {
        e.preventDefault();
        const filter = link.getAttribute("data-filter");

        // Remove active class from all links
        categoryLinks.forEach((l) => l.classList.remove("active"));
        // Add active class to clicked link
        link.classList.add("active");

        // Filter posts
        if (postsGrid) {
          const posts = $$(".card[data-category]", postsGrid);
          posts.forEach((post) => {
            if (filter === "all" || post.getAttribute("data-category") === filter) {
              post.style.display = "block";
            } else {
              post.style.display = "none";
            }
          });
        }
      });
    });

    // =============================
    // 13. Back to Top Button
    // =============================
    const backToTopBtn = $(".back-to-top");

    if (backToTopBtn) {
      on(window, "scroll", () => {
        if (window.scrollY > 300) {
          backToTopBtn.classList.add("show");
        } else {
          backToTopBtn.classList.remove("show");
        }
      });

      on(backToTopBtn, "click", () => {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });
      });
    }

    // =============================
    // 14. Social Share Buttons
    // =============================
    const shareButtons = $$(".share-btn");

    shareButtons.forEach((btn) => {
      on(btn, "click", (e) => {
        e.preventDefault();
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        const text = encodeURIComponent(
          document.querySelector("meta[name='description']")?.content || ""
        );

        if (btn.classList.contains("facebook")) {
          window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, "_blank");
        } else if (btn.classList.contains("twitter")) {
          window.open(`https://twitter.com/intent/tweet?url=${url}&text=${title}`, "_blank");
        } else if (btn.classList.contains("linkedin")) {
          window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, "_blank");
        } else if (btn.classList.contains("whatsapp")) {
          window.open(`https://wa.me/?text=${title}%20${url}`, "_blank");
        } else if (btn.classList.contains("copy-link")) {
          navigator.clipboard.writeText(window.location.href).then(() => {
            alert("Link kopyalandı!");
          }).catch(() => {
            // Fallback for older browsers
            const textarea = document.createElement("textarea");
            textarea.value = window.location.href;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand("copy");
            document.body.removeChild(textarea);
            alert("Link kopyalandı!");
          });
        }
      });
    });

    // =============================
    // 15. Newsletter Form
    // =============================
    const newsletterForm = $(".newsletter-form");
    if (newsletterForm) {
      on(newsletterForm, "submit", (e) => {
        e.preventDefault();
        const emailInput = newsletterForm.querySelector("input[type='email']");
        const email = emailInput?.value.trim();

        if (email) {
          // Demo: Save to localStorage
          const subscribers = JSON.parse(localStorage.getItem("newsletterSubscribers") || "[]");
          if (!subscribers.includes(email)) {
            subscribers.push(email);
            localStorage.setItem("newsletterSubscribers", JSON.stringify(subscribers));
          }
          alert("Abunəliyiniz təsdiqləndi! Təşəkkürlər!");
          newsletterForm.reset();
        }
      });
    }

    // =============================
    // 16. Reading Time Calculation
    // =============================
    function calculateReadingTime() {
      const postContent = $(".post-content");
      if (postContent) {
        const text = postContent.textContent || postContent.innerText;
        const words = text.trim().split(/\s+/).length;
        const readingTime = Math.ceil(words / 200); // Average reading speed: 200 words per minute
        
        const readingTimeElements = $$(".card-reading-time, .post-reading-time");
        readingTimeElements.forEach((el) => {
          if (el.textContent.includes("dəq") || el.textContent.includes("dəqiqə")) {
            el.innerHTML = `<i class="fas fa-clock"></i> ${readingTime} dəqiqəlik oxu`;
          }
        });
      }
    }

    calculateReadingTime();

    // =============================
    // 17. Pagination
    // =============================
    const paginationBtns = $$(".pagination-btn");
    paginationBtns.forEach((btn) => {
      on(btn, "click", (e) => {
        e.preventDefault();
        paginationBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        // In a real application, you would load new posts here
      });
    });

    // =============================
    // 18. Active Link Highlighting (Updated for About page)
    // =============================
    try {
      const currentPath = window.location.pathname.split("/").pop() || "index.html";
      const pageMap = {
        "index.html": "index.html",
        "": "index.html",
        "blog.html": "blog.html",
        "post-detail.html": "post-detail.html",
        "contact.html": "contact.html",
        "about.html": "about.html",
      };

      const currentPage = pageMap[currentPath] || "index.html";
      const navLinks = $$('.navbar .nav a[href]');

      navLinks.forEach((link) => {
        const href = link.getAttribute("href");
        
        // Remove existing active class
        link.classList.remove("active");
        
        // Add active class if matches current page
        if (href === currentPage) {
          link.classList.add("active");
        }
      });
    } catch (error) {
      console.error("Error setting active link:", error);
    }

    // =============================
    // 19. Card Stats (Like/View)
    // =============================
    const cardStats = $$(".card-stats span");
    cardStats.forEach((stat) => {
      on(stat, "click", () => {
        const icon = stat.querySelector("i");
        if (icon && icon.classList.contains("fa-heart")) {
          const currentCount = parseInt(stat.textContent.trim()) || 0;
          stat.innerHTML = `<i class="fas fa-heart"></i> ${currentCount + 1}`;
          stat.style.color = "#e74c3c";
        }
      });
    });

    // =============================
    // 20. Console Log (Development)
    // =============================
    console.log("BlogSpot website loaded successfully with all features!");
  });
})();
