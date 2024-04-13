document.addEventListener('DOMContentLoaded', function () {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const currentMonthDisplay = document.getElementById('currentMonth');
    const calendarGrid = document.getElementById('calendarGrid');
    const details = document.getElementById('details');
    const detailsContent = document.getElementById('detailsContent');
    const overlay = document.getElementById('overlay');

    let currentDate = new Date();

    let days = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];

    function get_day_cell(day, day_of_week) {
        // Funzione Jinja per determinare se è un weekend
        const isWeekend = day_of_week == 0 || day_of_week == 6; // Sabato o Domenica

        //TODO: isHoliday

        // Se è un weekend o una festività italiana, aggiungi le classi corrette
        const cellClass = isWeekend ? 'bg-gray-300 cursor-not-allowed' : 'cell';

        return `<div class="bg-white p-4 m-4 rounded-lg shadow-md aspect-w-1 aspect-h-2 text-left p-2 border ${cellClass} hover:scale-105"
                    data-day="${day}"
                    data-day-of-week="${days[day_of_week]}">
                    ${day < 10 ? day + '&nbsp;' : day}&nbsp;&nbsp;&nbsp;${days[day_of_week]}&nbsp;&nbsp;
                    <!-- Horizontal line -->
                    <hr class="my-4 border-t border-gray-300">
                </div>`;
    }


    function openDetails(day, dayOfWeek) {
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
        // Clear previous content
        calendarGrid.innerHTML = '';

        // Get the current month and year
        const currentMonth = currentDate.getMonth();
        const currentYear = currentDate.getFullYear();

        // Set the current month in the header
        currentMonthDisplay.textContent = new Date(currentYear, currentMonth).toLocaleString('default', {
            month: 'long',
            year: 'numeric'
        });

        // Get the first day of the month
        let firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        let startingDayOfWeek = firstDayOfMonth.getDay(); // Sunday is 0, Monday is 1

        // If the starting day is Sunday (0), adjust it to Monday (6)
        if (startingDayOfWeek === 0) {
            startingDayOfWeek = 6;
        } else {
            startingDayOfWeek -= 1;
        }

        // Get the total number of days in the month
        const totalDaysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        // Get the current date
        const tempDate = new Date();
        // Set the date to the first day of the current month
        tempDate.setDate(1);
        // Subtract one day to move to the last day of the previous month
        tempDate.setDate(0);
        // Get the number of the last day of the previous month
        const lastDayOfPreviousMonth = tempDate.getDate();

        for (let i = 0; i < startingDayOfWeek; i++) {
            calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
            ${lastDayOfPreviousMonth + i - startingDayOfWeek}&nbsp;&nbsp;&nbsp;${days[startingDayOfWeek-startingDayOfWeek+i+1]}&nbsp;&nbsp;
            <!-- Horizontal line -->
            <hr class="my-4 border-t border-gray-300">
            </div>`
        }

        let dayOfWeek = firstDayOfMonth.getDay();
        for (let day = 1; day <= totalDaysInMonth; day++) {
            calendarGrid.innerHTML += get_day_cell(day, dayOfWeek);
            dayOfWeek = (dayOfWeek + 1) % 7;
        }

        for (let i = 1; dayOfWeek <= 7 && dayOfWeek != 1; i++) {
            if (dayOfWeek == 7) {
                calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
                ${i}&nbsp;&nbsp;&nbsp;${days[0]}&nbsp;&nbsp;
                <!-- Horizontal line -->
                <hr class="my-4 border-t border-gray-300">
                </div>`;
            } else {
                calendarGrid.innerHTML += `<div class="opacity-70 p-4 m-4 rounded-lg aspect-w-1 aspect-h-2 text-left p-2 border">
                ${i}&nbsp;&nbsp;&nbsp;${days[dayOfWeek]}&nbsp;&nbsp;
                <!-- Horizontal line -->
                <hr class="my-4 border-t border-gray-300">
                </div>`;
            }
            dayOfWeek++;
        }
    }

    renderCalendar();

    // Event listener for previous month button
    prevBtn.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    // Event listener for next month button
    nextBtn.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    // Event delegation for cell clicks
    calendarGrid.addEventListener('click', function(event) {
        if (event.target.classList.contains('cell')) {
            const day = event.target.dataset.day;
            const dayOfWeek = event.target.dataset.dayOfWeek;
            openDetails(day, dayOfWeek);
        }
    });

    // Event listener to close details
    overlay.addEventListener('click', function () {
        closeDetails();
    });
});