document.addEventListener("DOMContentLoaded", () => {
  const actividades = Object.keys(ponderaciones);

  actividades.forEach(act => {
    const radios = document.getElementsByName(act);
    const puntajeInput = document.querySelector(`input[name="${act}_puntaje"]`);

    radios.forEach(radio => {
      radio.addEventListener("change", () => {
        if (radio.value === "si" && radio.checked) {
          puntajeInput.disabled = false;
          puntajeInput.value = "";
        } else if (radio.value === "no" && radio.checked) {
          puntajeInput.disabled = true;
          puntajeInput.value = "0";
        }
      });
    });

    if (puntajeInput) {
      puntajeInput.disabled = true;
      puntajeInput.value = "";
    }
  });
});

async function enviarEvaluacion() {
  const actividades = Object.keys(ponderaciones);
  const datos = {};

  for (const act of actividades) {
    const si = document.querySelector(`input[name="${act}"]:checked`);
    const retroalimentacion = document.querySelector(`input[name="${act}_feedback"]`).value.trim();
    const puntos = document.querySelector(`input[name="${act}_puntaje"]`).value.trim();

    datos[act] = {
      cumplido: si && si.value === "si",
      retroalimentacion: retroalimentacion,
      puntos: puntos || "0"
    };
  }

  try {
    const resp = await fetch("/evaluate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(datos),
    });

    const result = await resp.json();
    const container = document.getElementById("resultado");
    const puntos = result.totalPuntos;
    const minimo = 70;
    const maximo = 100;

    let html = `
    <div class="result-container ${puntos >= minimo ? 'pass' : 'fail'}">
      <span class="icon ${puntos >= minimo ? 'pass' : 'fail'}">
        ${puntos >= minimo ? '✔️' : '❌'}
      </span>
      <div class="result-text">
        <span>${puntos >= minimo ? '¡Proyecto aprobado!' : 'Proyecto no aprobado.'}</span>
        <span class="score">${puntos} / ${maximo}</span>
      </div>
    </div>
  `;

    const actividadesOrdenadas = Object.entries(result.detalles)
      .sort(([, a], [, b]) => {
        const numA = parseInt(a.actividad.match(/^(\d+)\./)?.[1] || "0");
        const numB = parseInt(b.actividad.match(/^(\d+)\./)?.[1] || "0");
        return numA - numB;
      });

    html += `<h3>Detalle de actividades:</h3>`;

    actividadesOrdenadas.forEach(([clave, detalle]) => {
      const cumplido = datos[clave].cumplido ? "Sí" : "No";
      const puntosAct = parseInt(datos[clave].puntos) || 0;
      const retro = detalle.retroalimentacion.trim();

      html += `
    <div class="feedback-item">
      <strong>${detalle.actividad}</strong>

      <div class="info-bloque">
        <div class="info-linea">
          <span class="icon-cumplio">${cumplido === "Sí" ? '✔️' : '❌'}</span>
          <span class="cumplio-texto">Cumplió: ${cumplido}</span>
        </div>
        <div class="info-linea">
          <span class="puntaje-label">Puntaje:</span> 
          <span class="puntaje-valor">${puntosAct}</span>
        </div>
      </div>

      ${retro ? `
      <div class="retro-bloque">
        <span class="retro-label">Comentarios:</span>
        <p class="retro-texto">${retro}</p>
      </div>
      ` : ''}
    </div>
  `;
    });

    container.innerHTML = html;
    container.scrollIntoView({behavior: "smooth"});
  } catch (error) {
    alert("Error al evaluar: " + error.message);
  }
}
