// ==============================
// DASHBOARD JS – FINANCEIRO
// ==============================

document.addEventListener("DOMContentLoaded", () => {

  // ----------------------------
  // AUTOFOCUS NO INPUT
  // ----------------------------
  const quickInput = document.querySelector(".hero-input input");
  if (quickInput) {
    quickInput.focus();
  }

  // ----------------------------
  // SUBMIT COM ENTER
  // ----------------------------
  const quickForm = document.querySelector(".quick-form");
  if (quickForm && quickInput) {
    quickForm.addEventListener("submit", () => {
      quickInput.blur();
    });
  }

  // ----------------------------
  // FEEDBACK VISUAL AO ENVIAR
  // ----------------------------
  if (quickForm) {
    quickForm.addEventListener("submit", () => {
      document.body.classList.add("dashboard-loading");
    });
  }

});
