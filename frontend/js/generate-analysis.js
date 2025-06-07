document.addEventListener("DOMContentLoaded", () => {
  const forecastInput = document.getElementById("forecastInput");
  const actualsPath = document.getElementById("actualsPath");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  analyzeBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Analyzing…";
    analyzeBtn.disabled = true;

    const forecast = forecastInput.value.trim();
    const actuals = actualsPath.value.trim();
    if (!forecast || !actuals) {
      errorDiv.textContent = "Both forecast and actuals CSV path are required.";
      outputDiv.textContent = "";
      analyzeBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/analyze-performance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ forecast_markdown: forecast, actuals_csv_path: actuals })
      });
      if (!resp.ok) {
        const err = await resp.text();
        throw new Error(`Error ${resp.status}: ${err}`);
      }
      const data = await resp.json();
      outputDiv.textContent = data.analysis_markdown;
    } catch (e) {
      errorDiv.textContent = `Request failed: ${e.message}`;
      outputDiv.textContent = "";
    } finally {
      analyzeBtn.disabled = false;
    }
  });
});
