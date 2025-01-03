document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const viewSelect = document.getElementById('viewSelect');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    let currentDate = new Date();
    let currentView = '3months';

    function updateCalendar() {
        calendarEl.innerHTML = '';
        calendarEl.className = 'calendar-container';
        
        if (currentView === 'year') {
            calendarEl.classList.add('year-view');
            for (let i = 0; i < 12; i++) {
                const monthDate = new Date(currentDate.getFullYear(), i, 1);
                const monthEl = createMonth(monthDate);
                calendarEl.appendChild(monthEl);
            }
        } else if (currentView === '3months') {
            calendarEl.classList.add('three-months');
            for (let i = 0; i < 3; i++) {
                const monthDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + i, 1);
                const monthEl = createMonth(monthDate);
                calendarEl.appendChild(monthEl);
            }
        } else {
            calendarEl.classList.add('single-month');
            const monthEl = createMonth(currentDate);
            calendarEl.appendChild(monthEl);
        }
    }

    function createMonth(date) {
        const monthEl = document.createElement('div');
        monthEl.className = 'month';

        const monthHeader = document.createElement('div');
        monthHeader.className = 'month-header';
        monthHeader.textContent = date.toLocaleString('default', { month: 'long', year: 'numeric' });
        monthEl.appendChild(monthHeader);

        const weekdaysEl = document.createElement('div');
        weekdaysEl.className = 'weekdays';
        ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'].forEach(day => {
            const dayEl = document.createElement('div');
            dayEl.textContent = day;
            weekdaysEl.appendChild(dayEl);
        });
        monthEl.appendChild(weekdaysEl);

        const daysEl = document.createElement('div');
        daysEl.className = 'days';

        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
        const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

        const today = new Date();
        const currentWeekStart = new Date(today);
        currentWeekStart.setDate(today.getDate() - today.getDay());
        const nextWeekStart = new Date(currentWeekStart);
        nextWeekStart.setDate(currentWeekStart.getDate() + 7);
        const nextWeekEnd = new Date(nextWeekStart);
        nextWeekEnd.setDate(nextWeekStart.getDate() + 6);

        for (let i = 0; i < firstDay; i++) {
            const dayEl = document.createElement('div');
            dayEl.className = 'day other-month';
            daysEl.appendChild(dayEl);
        }

        for (let i = 1; i <= daysInMonth; i++) {
            const dayEl = document.createElement('div');
            dayEl.className = 'day';
            dayEl.textContent = i;

            const currentDate = new Date(date.getFullYear(), date.getMonth(), i);

            if (currentDate.toDateString() === today.toDateString()) {
                dayEl.classList.add('today');
            } else if (currentDate >= currentWeekStart && currentDate < nextWeekStart) {
                dayEl.classList.add('current-week');
            } else if (currentDate >= nextWeekStart && currentDate <= nextWeekEnd) {
                dayEl.classList.add('next-week');
            }

            daysEl.appendChild(dayEl);
        }

        monthEl.appendChild(daysEl);
        return monthEl;
    }

    viewSelect.addEventListener('change', function() {
        currentView = this.value;
        updateCalendar();
    });

    prevBtn.addEventListener('click', function() {
        if (currentView === 'year') {
            currentDate.setFullYear(currentDate.getFullYear() - 1);
        } else if (currentView === '3months') {
            currentDate.setMonth(currentDate.getMonth() - 3);
        } else {
            currentDate.setMonth(currentDate.getMonth() - 1);
        }
        updateCalendar();
    });

    nextBtn.addEventListener('click', function() {
        if (currentView === 'year') {
            currentDate.setFullYear(currentDate.getFullYear() + 1);
        } else if (currentView === '3months') {
            currentDate.setMonth(currentDate.getMonth() + 3);
        } else {
            currentDate.setMonth(currentDate.getMonth() + 1);
        }
        updateCalendar();
    });

    updateCalendar();
});

