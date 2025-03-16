document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");
  const viewSelect = document.getElementById("viewSelect");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  let currentDate = new Date();
  let currentView = "3months";
  let colorSemana = [];

  function formatDate(date) {
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
  }

  function updateCalendar() {
    console.log("Actualizando calendario con colorSemana:", colorSemana);
    calendarEl.innerHTML = "";
    calendarEl.className = "calendar-container";

    if (currentView === "year") {
      calendarEl.classList.add("year-view");
      for (let i = 0; i < 12; i++) {
        const monthDate = new Date(currentDate.getFullYear(), i, 1);
        const monthEl = createMonth(monthDate);
        calendarEl.appendChild(monthEl);
      }
    } else if (currentView === "3months") {
      calendarEl.classList.add("three-months");
      for (let i = 0; i < 3; i++) {
        const monthDate = new Date(
          currentDate.getFullYear(),
          currentDate.getMonth() + i,
          1
        );
        const monthEl = createMonth(monthDate);
        calendarEl.appendChild(monthEl);
      }
    } else {
      calendarEl.classList.add("single-month");
      const monthEl = createMonth(currentDate);
      calendarEl.appendChild(monthEl);
    }
  }

  // Función para normalizar los nombres de colores
  function normalizeColor(color) {
    // Mapa de conversión de colores personalizados
    const colorMap = {
        'AZUL' : 'royalblue',
        'VERDE' : 'forestgreen',
        'ROJO' : 'firebrick',
        'AMARILLO' : 'yellow',
        'MARFIL' : 'papayawhip',
        'NARANJA' : 'orangered',
        'MORADO' : 'slateblue',
        'NEGRO' : '#212121',
        'ORO' : 'gold',
        'CAFÉ' : 'saddlebrown',
        'ROSA' : 'orchid',
        'GRIS' : 'slategray',
        'AZUL CLARO' : 'lightblue',
        'MELON' : 'mistyrose',
        'VERDE CLARO' : 'lightgreen',
        'BLANCO' : 'white',
    };

    // Si el color está en el mapa, usa ese valor
    if (colorMap[color]) {
      return colorMap[color];
    }

    // Si no está en el mapa, conviértelo a minúsculas y elimina espacios
    return color.toLowerCase().replace(/\s/g, "");
  }

  function createMonth(date) {
    const monthEl = document.createElement("div");
    monthEl.className = "month";

    const monthHeader = document.createElement("div");
    monthHeader.className = "month-header";
    monthHeader.textContent = date.toLocaleString("default", {
      month: "long",
      year: "numeric",
    });
    monthEl.appendChild(monthHeader);

    const weekdaysEl = document.createElement("div");
    weekdaysEl.className = "weekdays";
    ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"].forEach(day => {
      const dayEl = document.createElement("div");
      dayEl.textContent = day;
      weekdaysEl.appendChild(dayEl);
    });
    monthEl.appendChild(weekdaysEl);

    const daysEl = document.createElement("div");
    daysEl.className = "days";

    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    const daysInMonth = new Date(
      date.getFullYear(),
      date.getMonth() + 1,
      0
    ).getDate();

    for (let i = 0; i < firstDay; i++) {
      const dayEl = document.createElement("div");
      dayEl.className = "day other-month";
      daysEl.appendChild(dayEl);
    }

    for (let i = 1; i <= daysInMonth; i++) {
      const dayEl = document.createElement("div");
      dayEl.className = "day";
      dayEl.textContent = i;

      const currentDayDate = new Date(date.getFullYear(), date.getMonth(), i);
      const formattedDate = formatDate(currentDayDate);

      console.log("Comprobando fecha:", formattedDate);
      const dateData = colorSemana.find(item => {
        console.log("Comparando con:", item.DIA, "Color:", item.COLOR);
        return item.DIA === formattedDate;
      });

      if (dateData) {
        console.log("¡Coincidencia encontrada!", formattedDate, dateData.COLOR);
        const normalizedColor = normalizeColor(dateData.COLOR);
        console.log("Color normalizado:", normalizedColor);
        dayEl.style.backgroundColor = normalizedColor;

        // Ajusta el color del texto según el fondo
        if (["red", "blue", "darkgreen", "purple"].includes(normalizedColor)) {
          dayEl.style.color = "white";
        }
      }

      if (currentDayDate.toDateString() === new Date().toDateString()) {
        dayEl.classList.add("today");
      }

      daysEl.appendChild(dayEl);
    }

    monthEl.appendChild(daysEl);
    return monthEl;
  }

  // Event Listeners permanecen igual
  viewSelect.addEventListener("change", function () {
    currentView = this.value;
    updateCalendar();
  });

  prevBtn.addEventListener("click", function () {
    if (currentView === "year") {
      currentDate.setFullYear(currentDate.getFullYear() - 1);
    } else if (currentView === "3months") {
      currentDate.setMonth(currentDate.getMonth() - 3);
    } else {
      currentDate.setMonth(currentDate.getMonth() - 1);
    }
    updateCalendar();
  });

  nextBtn.addEventListener("click", function () {
    if (currentView === "year") {
      currentDate.setFullYear(currentDate.getFullYear() + 1);
    } else if (currentView === "3months") {
      currentDate.setMonth(currentDate.getMonth() + 3);
    } else {
      currentDate.setMonth(currentDate.getMonth() + 1);
    }
    updateCalendar();
  });

  // Modificamos el fetch para incluir más logging
  fetch("/home/", {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log("Datos recibidos del servidor:", data);
      if (data.color_semana) {
        colorSemana = data.color_semana;
        console.log("colorSemana actualizado:", colorSemana);

        // Verificar el formato de las fechas
        colorSemana.forEach(item => {
          console.log(
            "Fecha en datos:",
            item.DIA,
            "Formato esperado:",
            formatDate(new Date(item.DIA))
          );
        });
      }
      updateCalendar();
    })
    .catch(error => {
      console.error("Error al obtener los datos:", error);
      updateCalendar();
    });
});
