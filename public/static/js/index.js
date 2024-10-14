document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("upload-btn");
    const uploadDialog = document.getElementById("upload-dialog");
    const fileInput = document.getElementById("file-input");
    const selectBtn = document.getElementById("select-btn");
    const uploadArea = document.getElementById("upload-area");
    const queryForm = document.getElementById("query-form");
    const queryTextarea = document.getElementById("query-textarea");
    const resultsList = document.getElementById("results-list");

    let selectedFile = null;

    // Show file upload dialog
    uploadBtn.addEventListener("click", () => {
        uploadDialog.classList.toggle("hidden");
    });

    // Handle file selection from input
    fileInput.addEventListener("change", (event) => {
        selectedFile = event.target.files[0];
        uploadDialog.classList.add("hidden");
    });

    // Trigger file input click when 'Select' button is clicked
    selectBtn.addEventListener("click", () => {
        fileInput.click();
    });

    // Handle drag and drop for file upload
    uploadArea.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    uploadArea.addEventListener("drop", (event) => {
        event.preventDefault();
        selectedFile = event.dataTransfer.files[0];
        uploadDialog.classList.add("hidden");
    });

    // Handle query submission
    queryForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const query = queryTextarea.value;
        const response = await fetch("/api/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        displayResults(data.results);
    });

    // Function to display results
    function displayResults(results) {
        resultsList.innerHTML = ""; // Clear previous results
        results.forEach((result) => {
            const listItem = document.createElement("li");

            if (result.type === "text") {
                listItem.textContent = result.content;
            } else if (result.type === "image") {
                const img = document.createElement("img");
                img.src = result.url;
                img.alt = result.name;
                const downloadLink = document.createElement("a");
                downloadLink.href = result.url;
                downloadLink.textContent = "Download Image";
                downloadLink.download = result.name;
                listItem.appendChild(img);
                listItem.appendChild(downloadLink);
            } else if (result.type === "audio") {
                const audio = document.createElement("audio");
                audio.controls = true;
                const source = document.createElement("source");
                source.src = result.url;
                source.type = "audio/mpeg";
                audio.appendChild(source);
                const downloadLink = document.createElement("a");
                downloadLink.href = result.url;
                downloadLink.textContent = "Download Audio";
                downloadLink.download = result.name;
                listItem.appendChild(audio);
                listItem.appendChild(downloadLink);
            } else if (result.type === "video") {
                const video = document.createElement("video");
                video.controls = true;
                video.width = 320;
                video.height = 240;
                const source = document.createElement("source");
                source.src = result.url;
                source.type = "video/mp4";
                video.appendChild(source);
                const downloadLink = document.createElement("a");
                downloadLink.href = result.url;
                downloadLink.textContent = "Download Video";
                downloadLink.download = result.name;
                listItem.appendChild(video);
                listItem.appendChild(downloadLink);
            }

            resultsList.appendChild(listItem);
        });
    }
});
