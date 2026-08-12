const form = document.getElementById("search-form");
const input = document.getElementById("search-input");
const resultsContainer = document.getElementById("results");

// Check if user is logged in
const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const query = input.value.trim();

    if (!query) {
        return;
    }

    resultsContainer.innerHTML = "<p>Searching...</p>";

    try {

        const response = await fetch(
            `http://localhost:8080/api/search?q=${encodeURIComponent(query)}`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        // JWT missing, invalid or expired
        if (response.status === 401 || response.status === 403) {

            localStorage.removeItem("token");

            window.location.href = "login.html";

            return;
        }

        if (!response.ok) {
            throw new Error("Search request failed");
        }

        const data = await response.json();

        displayResults(data.results);

    } catch (error) {

        console.error("SEARCH ERROR:", error);

        resultsContainer.innerHTML = `
            <p>Search failed.</p>
            <p>${error.message}</p>
        `;
    }
});


function displayResults(results) {

    resultsContainer.innerHTML = "";

    if (!results || results.length === 0) {

        resultsContainer.innerHTML =
            "<p>No results found.</p>";

        return;
    }

    results.forEach(result => {

        const resultElement = document.createElement("div");

        resultElement.classList.add("result");

        resultElement.innerHTML = `
            <h2>${escapeHTML(result.title)}</h2>

            <a
                href="${escapeAttribute(result.url)}"
                target="_blank"
                rel="noopener noreferrer"
            >
                ${escapeHTML(result.url)}
            </a>

            <p>
                ${escapeHTML(result.snippet || "No preview available.")}
            </p>
        `;

        resultsContainer.appendChild(resultElement);
    });
}


// Prevent HTML from the crawled pages from being injected
function escapeHTML(value) {

    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
}


function escapeAttribute(value) {

    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}


// Logout
const logoutBtn = document.getElementById("logout-btn");

if (logoutBtn) {

    logoutBtn.addEventListener("click", () => {

        localStorage.removeItem("token");

        window.location.href = "login.html";
    });
}