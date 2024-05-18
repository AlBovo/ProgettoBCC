const month = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
const currentDate = new Date();
const calendarDate = new Date();

function getDaysData(year, month) {
    const last = new Date(year, month+1, 0);
    const first = new Date(year, month, 1);
    return [last.getDate(), first.getDay()];
}

function resetMonth() {
    for (let i = 0; i < 5; i++) {
        const week = document.getElementById(`week${i}`);
        week.innerHTML = "";
    }
}

async function updateMonth(year, month) {
    const date = new Date();
    const data = getDaysData(year, month);
    
    let csrftoken = document.getElementById('csrf_token');
    csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;
    let monthValues = await fetch("/api/month", {
        method: "POST",
        headers: {
            'Content-type':'application/json', 
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            year: year,
            month: month + 1
        })
    });
    monthValues = await monthValues.json();

    for (let i = 0, day = 1; i < 7 * 5; i++) {
        const dayDiv = document.createElement("div");
        const innerDay = document.createElement("div");
        let textDay = document.createElement("p");
        const week = document.getElementById(`week${Math.floor(i / 7)}`)
        const td = document.createElement("td");

        innerDay.classList.add("px-2", "py-2", "cursor-pointer", "flex", "w-full", "justify-center", "text-gray-600");
        textDay.classList.add("text-base", "font-medium", "text-gray-500");
        textDay.addEventListener("click", function() {
            selectedDay(day, month+1, year);
        });

        if(day === 1 && i < data[1] - 1) {
            textDay.innerText = "";
        }
        else if (day > data[0]) {
            textDay.innerText = "";
        }
        else {
            if (day === date.getDate() && year === currentDate.getFullYear() && month === currentDate.getMonth()) {
                textDay = document.createElement("a");
                textDay.setAttribute('role', 'link');
                textDay.setAttribute('tabindex', '0');
                textDay.classList.add(...[
                    "focus:outline-none", "focus:ring-2", "focus:ring-offset-2", "focus:ring-teal-600", 
                    "focus:bg-teal-400", "text-base", "w-8", "h-8", "flex", "items-center", "justify-center", 
                    "font-medium", "text-white", "bg-teal-600", "rounded-full", "hover:bg-teal-400"
                ]);

                dayDiv.classList.add("w-full", "h-full");

                innerDay.classList.remove("px-2", "py-2", "flex", "text-gray-600");
                innerDay.classList.add("flex", "items-center", "rounded-full");                                                
            }
            else if(monthValues[day] === 0 || (day < date.getDate() && year == currentDate.getFullYear() && month == currentDate.getMonth())) {
                innerDay.classList.add("opacity-50", "cursor-not-allowed");
                innerDay.setAttribute('disabled', 'true');
            }
            textDay.innerText = `${day}`;
            day++;
        }

        innerDay.appendChild(textDay);
        dayDiv.appendChild(innerDay);
        td.appendChild(dayDiv);
        week.appendChild(td);
    }
}

async function selectedDay(day, month, year) {
    let csrftoken = document.getElementById('csrf_token');
    csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;

    let response = await fetch("/api/daydata", {
        method: "POST",
        headers: {
            'Content-type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            day: day,
            month: month,
            year: year
        })
    });
    response = await response.json();
}

function nextMonth() {
    resetMonth();
    calendarDate.setMonth(calendarDate.getMonth() + 1);

    const date = document.getElementById("calendar");    
    date.innerText = `${month[calendarDate.getMonth()]} ${calendarDate.getFullYear()}`;

    updateMonth(calendarDate.getFullYear(), calendarDate.getMonth());
}

function previousMonth() {
    if (currentDate.getMonth() === calendarDate.getMonth() && currentDate.getFullYear() === calendarDate.getFullYear()) {
        return;
    }
    resetMonth();
    calendarDate.setMonth(calendarDate.getMonth() - 1);

    const date = document.getElementById("calendar");    
    date.innerText = `${month[calendarDate.getMonth()]} ${calendarDate.getFullYear()}`;

    updateMonth(calendarDate.getFullYear(), calendarDate.getMonth());
}

document.addEventListener('DOMContentLoaded', function () {
    async function showCategories() {
        let csrftoken = document.getElementById('csrf_token');
        csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;

        const response = await fetch("/api/categories", {
            method: "GET",
            headers: {
                'X-CSRFToken': csrftoken
            },
        });
        const categories = await response.json();
        
        for (let i = 0; i < categories.length; i+=2) {
            const categoryElement = document.createElement("div");
            categoryElement.classList.add(...["flex", "flex-col", "md:flex-row", "text-sm", "font-medium"]);
            
            categoryElement.innerHTML = `
                <div class="w-full bg-white rounded-lg my-2 flex-1 mr-4 svelte-1l8159u">
                    <div class="flex items-center ps-3 border-gray-200 svelte-1l8159u">
                        <input id="${categories[i].replace(" ", "").toLowerCase()}" type="checkbox" value="" class="w-4 h-4 bg-gray-100 border-gray-300 rounded">
                        <label for="${categories[i].replace(" ", "").toLowerCase()}" class="w-full py-3 ms-2 text-sm font-medium text-gray-800">${categories[i]}</label>
                    </div>
                </div>
            `;
            
            if (i + 1 < categories.length) {
                categoryElement.innerHTML += `
                <div class="w-full bg-white rounded-lg my-2 flex-1 ml-4 svelte-1l8159u">
                    <div class="flex items-center ps-3 border-gray-200 svelte-1l8159u">
                        <input id="${categories[i+1].replace(" ", "").toLowerCase()}" type="checkbox" value="" class="w-4 h-4 bg-gray-100 border-gray-300 rounded">
                        <label for="${categories[i+1].replace(" ", "").toLowerCase()}" class="w-full py-3 ms-2 text-sm font-medium text-gray-800">${categories[i+1]}</label>
                    </div>
                </div>
                `;
            }
            else {
                categoryElement.innerHTML += `
                <div class="w-full rounded-lg flex-1 my-2 ml-4 svelte-1l8159u ">
                    <div class="flex items-center ps-3 border-gray-200 svelte-1l8159u">
                    </div>
                </div>
                `;
            }
            document.getElementById("categories").appendChild(categoryElement);
        }
    }

    // set calendar to current month
    function updateDate() {
        const date = document.getElementById("calendar");
        const d = new Date();
        
        date.innerText = `${month[d.getMonth()]} ${d.getFullYear()}`;
        updateMonth(d.getFullYear(), d.getMonth());
    }

    showCategories();
    updateDate();
});

function nextPage() {
    let page = document.getElementById("current").value - '0';

    switch (page) {
        case 0:
            document.getElementById("categories").classList.add("hidden");
            document.getElementById("date").classList.remove("hidden");
            document.getElementById("previous").classList.remove("invisible");
            break;
        
        case 1:
            document.getElementById("date").classList.add("hidden");
            document.getElementById("operator").classList.remove("hidden");
            document.getElementById("skip").classList.remove("invisible");
            break;

        case 2:
            document.getElementById("operator").classList.add("hidden");
            document.getElementById("confirm").classList.remove("hidden");
            document.getElementById("next").classList.add("invisible");
            document.getElementById("skip").classList.add("invisible");
            break;
        
        default:
            break;
    }
    page += 1;

    const line = document.getElementById(`line-${page}`);
    const icon = document.getElementById(`icon-${page}0`);
    const svg = document.getElementById(`icon-${page}1`);
    const text = document.getElementById(`text-${page}`);

    line.classList.remove("border-gray-300");
    line.classList.add("border-teal-600");

    icon.classList.remove("text-gray-500");
    icon.classList.add("text-white");

    svg.classList.remove("border-gray-300");
    svg.classList.add(...["bg-teal-600", "border-teal-600"]);

    text.classList.remove("text-gray-500");
    text.classList.add("text-teal-600");
    
    document.getElementById("current").setAttribute('value', `${page}`);
}

function previousPage() {
    let page = document.getElementById("current").value - '0';

    switch (page) {
        case 1:
            document.getElementById("date").classList.add("hidden");
            document.getElementById("categories").classList.remove("hidden");
            document.getElementById("previous").classList.add("invisible");
            break;
        
        case 2:
            document.getElementById("operator").classList.add("hidden");
            document.getElementById("date").classList.remove("hidden");
            document.getElementById("skip").classList.add("invisible");
            break;

        case 3:
            document.getElementById("confirm").classList.add("hidden");
            document.getElementById("operator").classList.remove("hidden");
            document.getElementById("next").classList.remove("invisible");
            document.getElementById("skip").classList.remove("invisible");
            break;
        
        default:
            break;
    }

    const line = document.getElementById(`line-${page}`);
    const icon = document.getElementById(`icon-${page}0`);
    const svg = document.getElementById(`icon-${page}1`);
    const text = document.getElementById(`text-${page}`);

    line.classList.remove("border-teal-600");
    line.classList.add("border-gray-300");

    icon.classList.remove("text-white");
    icon.classList.add("text-gray-500");

    svg.classList.remove(...["bg-teal-600", "border-teal-600"]);
    svg.classList.add("border-gray-300");

    text.classList.remove("text-teal-600");
    text.classList.add("text-gray-500");

    document.getElementById("current").setAttribute('value', `${page-1}`);
}

document.getElementById("previousMonth").addEventListener("click", previousMonth);
document.getElementById("nextMonth").addEventListener("click", nextMonth);
document.getElementById("previous").addEventListener("click", previousPage);
document.getElementById("next").addEventListener("click", nextPage);
document.getElementById("skip").addEventListener("click", nextPage);