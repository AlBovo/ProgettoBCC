document.addEventListener('DOMContentLoaded', function () {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const currentMonthDisplay = document.getElementById('currentMonth');
    const calendarGrid = document.getElementById('calendarGrid');
    const details = document.getElementById('details');
    const overlay = document.getElementById('overlay');
    const eventListContainer = document.getElementById('event-list');

    let currentDate = new Date();
    let days = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];

    function getDayCell(day, dayOfWeek) {
        const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
        const cellClass = isWeekend ? 'bg-gray-300 cursor-not-allowed' : 'cell';

        return `<div class="bg-white p-4 m-4 rounded-lg shadow-md aspect-w-1 aspect-h-2 text-left p-2 border ${cellClass} hover:scale-105"
                    data-day="${day}"
                    data-day-of-week="${days[dayOfWeek]}">
                    ${day < 10 ? day + '&nbsp;' : day}&nbsp;&nbsp;&nbsp;${days[dayOfWeek]}&nbsp;&nbsp;
                    <hr class="my-4 border-t border-gray-300">
                </div>`;
    }

    function daysInPreviousMonth(currentDate) {
        const currentMonth = currentDate.getMonth();
        const currentYear = currentDate.getFullYear();
        let previousMonth = currentMonth - 1;
        let previousYear = currentYear;
      
        if (previousMonth === -1) {
          previousMonth = 11;
          previousYear--;
        }
      
        const lastDayOfPreviousMonth = new Date(previousYear, previousMonth + 1, 0);
      
        return lastDayOfPreviousMonth.getDate();
    }

    async function getEvents(selectedDate) {
        try {
            let csrftoken = document.getElementById('csrf_token');
            csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;
    
            const response = await fetch('/api/day', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    date: selectedDate,
                })
            });

            if (!response.ok) {
                throw new Error('Errore nel recupero degli eventi');
            }

            return await response.json();
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    function getHourString(hour) {
        let ihour = parseInt(hour, 10);
        let minutes = ihour % 100;
        let hours = (ihour - minutes) / 100;
        return `${hours}:${minutes < 10 ? '0' + minutes : minutes} ${ihour < 1200 ? 'AM' : 'PM'}`;
    }

    async function renderEventList(selectedDate) {
        try {
            const events = await getEvents(selectedDate);
            eventListContainer.innerHTML = ''; 

            events.forEach(event => {
                const listItem = document.createElement('div');
                listItem.className = 'bg-gray-100 p-4 my-2 rounded-md';
                listItem.innerHTML = `
                    <div class="flex justify-items-stretch shadow-sm">
                        <a href="#" aria-current="page" class="flex-none justify-self-start text-center px-4 py-3 text-sm font-medium text-blue-700 bg-white border border-gray-200 rounded-s-lg hover:bg-gray-100 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
                            Prenota
                        </a>
                        <a class="flex-1 justify-self-start text-center px-4 py-3 text-sm font-medium text-gray-900 bg-white border-t border-b border-gray-200">
                            <i class="fa-solid fa-clock"></i>&#32;${getHourString(event.start_hour)}
                        </a>
                        <a class="flex-1 justify-self-start text-center px-4 py-3 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-e-lg">
                            <i class="fa-solid fa-clock"></i>&#32;${getHourString(event.end_hour)}
                        </a>
                    </div>
                `;
                eventListContainer.appendChild(listItem);
            });
        } catch (error) {
            console.error(error);
        }
    }

    function openDetails(selectedDate) {
        renderEventList(selectedDate);
        details.classList.remove('hidden');
        overlay.classList.remove('hidden');

        setTimeout(() => {
            details.style.transition = 'transform 0.2s ease-out';
            details.style.transitionProperty = 'transform, opacity';
            details.style.transform = 'translateX(0)';
            details.style.opacity = '1';
        }, 200);
    }

    function closeDetails() {
        details.style.transition = 'transform 0.2s ease-in';
        details.style.transform = 'translateX(-100%)';
        setTimeout(() => {
            details.classList.add('hidden');
            overlay.classList.add('hidden');
        }, 200);
    }

    function renderCalendar() {
        if(new Date().getMonth() === currentDate.getMonth() && new Date().getFullYear() === currentDate.getFullYear()) {
            prevBtn.disabled = true;
            prevBtn.classList.add('cursor-not-allowed');
        } else {
            prevBtn.disabled = false;
            prevBtn.classList.remove('cursor-not-allowed');
        }

        calendarGrid.innerHTML = '';

        const currentMonth = currentDate.getMonth();
        const currentYear = currentDate.getFullYear();
        currentMonthDisplay.textContent = new Date(currentYear, currentMonth).toLocaleString('default', {
            month: 'long',
            year: 'numeric'
        });

        let firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        let startingDayOfWeek = firstDayOfMonth.getDay(); 

        if (startingDayOfWeek === 0) {
            startingDayOfWeek = 6;
        } else {
            startingDayOfWeek -= 1;
        }

        const totalDaysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        const lastDayOfPreviousMonth = daysInPreviousMonth(currentDate);

        for (let i = 0; i < startingDayOfWeek; i++) {
            calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
            ${lastDayOfPreviousMonth + i - (startingDayOfWeek-1)}&nbsp;&nbsp;&nbsp;${days[startingDayOfWeek-startingDayOfWeek+i+1]}&nbsp;&nbsp;
            <hr class="my-4 border-t border-gray-300">
            </div>`;
        }

        let dayOfWeek = firstDayOfMonth.getDay();
        for (let day = 1; day <= totalDaysInMonth; day++) {
            calendarGrid.innerHTML += getDayCell(day, dayOfWeek);
            dayOfWeek = (dayOfWeek + 1) % 7;
        }

        for (let i = 1; dayOfWeek <= 7 && dayOfWeek != 1; i++) {
            if (dayOfWeek == 7) {
                calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
                ${i}&nbsp;&nbsp;&nbsp;${days[0]}&nbsp;&nbsp;
                <hr class="my-4 border-t border-gray-300">
                </div>`;
            } else {
                calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
                ${i}&nbsp;&nbsp;&nbsp;${days[dayOfWeek]}&nbsp;&nbsp;
                <hr class="my-4 border-t border-gray-300">
                </div>`;
            }
            dayOfWeek++;
        }
    }

    prevBtn.addEventListener('click', function () {
        if(new Date().getMonth() === currentDate.getMonth() && new Date().getFullYear() === currentDate.getFullYear()) {
            return;
        }
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextBtn.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    calendarGrid.addEventListener('click', function(event) {
        if (event.target.classList.contains('cell')) {
            const day = event.target.dataset.day;
            const selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day, 12).toISOString().split('T')[0];
            openDetails(selectedDate);
        }
    });

    overlay.addEventListener('click', function () {
        closeDetails();
    });

    renderCalendar();
});
