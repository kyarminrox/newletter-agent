document.addEventListener("DOMContentLoaded", () => {
  const excerptInput = document.getElementById("excerptInput");
  const suggestBtn = document.getElementById("suggestBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  suggestBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Generating visual prompts…";
    suggestBtn.disabled = true;

    const excerpt = excerptInput.value.trim();
    if (!excerpt) {
      errorDiv.textContent = "Draft excerpt is required.";
      outputDiv.textContent = "";
      suggestBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/suggest-visuals", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ draft_excerpt: excerpt })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = data.visual_prompts;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      suggestBtn.disabled = false;
    }
  });
});
