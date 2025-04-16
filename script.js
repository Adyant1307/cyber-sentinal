
async function fetchLiveThreats() {
    const res = await fetch("/api/live");
    const data = await res.json();
    const tbody = document.querySelector("#live-table tbody");
    tbody.innerHTML = "";

    data.forEach(entry => {
        const postClass = entry.status === "Threat" ? "post-threat" : "post-safe";
        const statusClass = entry.status === "Threat" ? "status-threat" : "status-safe";
        tbody.innerHTML += `
            <tr>
                <td class="${postClass}">${entry.post}</td>
                <td class="${statusClass}">${entry.status}</td>
            </tr>
        `;
    });
}


async function fetchDarkwebRaw() {
    const res = await fetch("/api/darkweb/raw");
    const data = await res.json();
    const ul = document.querySelector("#darkweb-raw");
    ul.innerHTML = "";
    data.forEach(post => {
        ul.innerHTML += `<li>${post}</li>`;
    });
}


async function fetchDarkwebThreats() {
    const res = await fetch("/api/darkweb");
    const data = await res.json();
    const tbody = document.querySelector("#darkweb-table tbody");
    tbody.innerHTML = "";

    data.forEach(entry => {
        const postClass = entry.status === "Threat" ? "post-threat" : "post-safe";
        const statusClass = entry.status === "Threat" ? "status-threat" : "status-safe";
        tbody.innerHTML += `
            <tr>
                <td class="${postClass}">${entry.post}</td>
                <td class="${statusClass}">${entry.status}</td>
                <td>${entry.threat_level}</td>
                <td>${entry.time}</td>
            </tr>
        `;
    });
}


function refreshAll() {
    fetchLiveThreats();
    fetchDarkwebRaw();
    fetchDarkwebThreats();
}

refreshAll();
setInterval(refreshAll, 30000);
