document.addEventListener("DOMContentLoaded", () => {
  const csvInput = document.getElementById("csvPath");
  const queryInput = document.getElementById("query");
  const generateBtn = document.getElementById("generateBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  generateBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Generating research brief…";
    generateBtn.disabled = true;

    const csvPath = csvInput.value.trim();
    const query = queryInput.value.trim();

    if (!csvPath || !query) {
      errorDiv.textContent = "Both CSV path and query are required.";
      outputDiv.textContent = "";
      generateBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/generate-research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ csv_path: csvPath, query: query })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = data.research_brief;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      generateBtn.disabled = false;
    }
  });
});
