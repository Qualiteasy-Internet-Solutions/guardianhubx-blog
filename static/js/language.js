document.addEventListener("DOMContentLoaded", function () {
  const languageSwitcher = document.getElementById("languageSwitcher");

  if (languageSwitcher) {
    // 1. Determina l'idioma actual
    let currentLang = "es"; // Idioma per defecte
    if (window.location.pathname.startsWith("/blog/ca")) {
      currentLang = "ca";
    }
    
    // 2. Estableix el valor correcte al selector
    languageSwitcher.value = currentLang;

    // 3. Afegeix l'event per canviar d'idioma
    languageSwitcher.addEventListener("change", function () {
      const selectedLang = this.value;

      // 4. LÒGICA PRINCIPAL: Utilitza l'objecte de traduccions de Hugo si existeix
      // Aquesta part gestiona tots els articles amb traducció directa.
      if (window.translations && window.translations[selectedLang]) {
        window.location.href = window.translations[selectedLang];
        return; 
      }

      // 5. LÒGICA DE FALLBACK: Si no hi ha traducció, redirigeix a l'índex del blog
      // Aquesta és la part que estava incorrecta i ara està corregida.
      let fallbackUrl = "/blog/"; // Per defecte a l'índex en espanyol
      if (selectedLang === "ca") {
        fallbackUrl = "/blog/ca/"; // Índex en català
      }
      window.location.href = fallbackUrl;
    });
  }
});