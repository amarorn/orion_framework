document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");

  const setGlow = (card, x, y) => {
    const rect = card.getBoundingClientRect();
    const relX = ((x - rect.left) / rect.width - 0.5) * 60;
    const relY = ((y - rect.top) / rect.height - 0.5) * 60;
    card.style.setProperty("--glow-x", `${relX}px`);
    card.style.setProperty("--glow-y", `${relY}px`);
  };

  cards.forEach((card) => {
    card.addEventListener("mousemove", (event) => {
      window.requestAnimationFrame(() => setGlow(card, event.clientX, event.clientY));
    });

    card.addEventListener("mouseleave", () => {
      card.style.setProperty("--glow-x", "0px");
      card.style.setProperty("--glow-y", "0px");
    });
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal");
        }
      });
    },
    { threshold: 0.2 }
  );

  const revealables = document.querySelectorAll(".card, .section h2, .section p, .hero-content");
  revealables.forEach((el) => {
    el.classList.add("pre-reveal");
    observer.observe(el);
  });

  const languageButtons = document.querySelectorAll("[data-switch-lang]");
  const langBlocks = document.querySelectorAll(".lang-block");
  const langInlines = document.querySelectorAll(".lang-inline");

  const applyLanguage = (lang) => {
    langBlocks.forEach((el) => {
      el.classList.toggle("is-active", el.dataset.lang === lang);
    });
    langInlines.forEach((el) => {
      el.classList.toggle("is-active", el.dataset.lang === lang);
    });
    languageButtons.forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.switchLang === lang);
    });
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("data-lang", lang);
  };

  const supportedLanguages = ["en", "pt", "es"];
  const storedLang = localStorage.getItem("orion-doc-lang");
  const initialLang = supportedLanguages.includes(storedLang) ? storedLang : "en";
  applyLanguage(initialLang);

  languageButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetLang = btn.dataset.switchLang;
      if (!supportedLanguages.includes(targetLang)) {
        return;
      }
      localStorage.setItem("orion-doc-lang", targetLang);
      applyLanguage(targetLang);
    });
  });

  const currentYear = new Date().getFullYear();
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = currentYear;
  });
});
