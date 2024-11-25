function searchPapers() {
    const courseCode = document.getElementById("courseCode").value.trim();

    if (!courseCode) {
        alert("Please enter a course code.");
        return;
    }

    // Send course code to the backend
    fetch("/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ course_code: courseCode })
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error("Error fetching question papers:", error));
}

function displayResults(data) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    if (data.error) {
        resultsContainer.textContent = data.error;
    } else {
        data.forEach(link => {
            const anchor = document.createElement("a");
            anchor.href = link;
            anchor.target = "_blank";
            anchor.textContent = `Download: ${link}`;
            resultsContainer.appendChild(anchor);
        });
    }
}
