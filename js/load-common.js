// static/js/load-common.js

let loadCounter = 0;
function checkIfAllLoaded() {
  if (loadCounter === 3) {
    // Aquí puedes ocultar un spinner si lo tienes
  }
}

// Todas las rutas son absolutas desde la raíz del dominio:
$.get("/head.html", data => {
  $("#common-head").html(data);
  loadCounter++; checkIfAllLoaded();
});

$("#header-container").load("/header.html", () => {
  loadCounter++; checkIfAllLoaded();
});

$("#footer-container").load("/footer.html", () => {
  loadCounter++; checkIfAllLoaded();
});