document.addEventListener("DOMContentLoaded", () => {
  const outlineInput = document.getElementById("outlineInput");
  const generateBtn = document.getElementById("generateBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  generateBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Generating draft…";
    generateBtn.disabled = true;

    const outline = outlineInput.value.trim();
    if (!outline) {
      errorDiv.textContent = "Outline Markdown is required.";
      outputDiv.textContent = "";
      generateBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/create-draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ outline_markdown: outline })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = data.draft_markdown;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      generateBtn.disabled = false;
    }
  });
});
