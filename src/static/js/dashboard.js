document.addEventListener('DOMContentLoaded', function () {
    async function showCategories() {
        let csrftoken = document.getElementById('csrf_token');
        csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;

        const response = await fetch("/api/categories", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
        });
        const categories = await response.json();
        
        for (let i = 0; i < categories.length; i+=2) {
            const category = categories[i];
            const categoryElement = document.createElement("div");
            categoryElement.classList.add(...["flex", "flex-col", "md:flex-row", "text-sm", "font-medium"]);
            
            categoryElement.innerHTML = `
                <div class="w-full bg-white rounded-lg my-2 flex-1 mr-4 svelte-1l8159u">
                    <div class="flex items-center ps-3 border-gray-200 svelte-1l8159u">
                        <input id="tag" type="checkbox" value="" class="w-4 h-4 bg-gray-100 border-gray-300 rounded">
                        <label for="tag" class="w-full py-3 ms-2 text-sm font-medium text-gray-800">${categories[i]}</label>
                    </div>
                </div>
            `;
            
            if (i + 1 < categories.length) {
                categoryElement.innerHTML += `
                <div class="w-full bg-white rounded-lg my-2 flex-1 ml-4 svelte-1l8159u">
                    <div class="flex items-center ps-3 border-gray-200 svelte-1l8159u">
                        <input id="tag" type="checkbox" value="" class="w-4 h-4 bg-gray-100 border-gray-300 rounded">
                        <label for="tag" class="w-full py-3 ms-2 text-sm font-medium text-gray-800">${categories[i+1]}</label>
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

    showCategories();
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

