document.addEventListener("DOMContentLoaded", () => {
  const csvInput = document.getElementById("csvPath");
  const subjectsInput = document.getElementById("subjects");
  const forecastBtn = document.getElementById("forecastBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  forecastBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Generating forecast…";
    forecastBtn.disabled = true;

    const csvPath = csvInput.value.trim();
    const subjectsRaw = subjectsInput.value.trim();
    const subjectLines = subjectsRaw
      .split("\n")
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    if (!csvPath || subjectLines.length === 0) {
      errorDiv.textContent = "Both CSV path and at least one subject line are required.";
      outputDiv.textContent = "";
      forecastBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/forecast-performance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ csv_path: csvPath, subject_lines: subjectLines })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = data.forecast_markdown;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      forecastBtn.disabled = false;
    }
  });
});
