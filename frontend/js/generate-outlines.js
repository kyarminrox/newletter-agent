document.addEventListener("DOMContentLoaded", () => {
  const researchInput = document.getElementById("researchInput");
  const issueInput = document.getElementById("issueInput");
  const generateBtn = document.getElementById("generateBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  generateBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Generating outlines…";
    generateBtn.disabled = true;

    const research = researchInput.value.trim();
    const issue = issueInput.value.trim();

    if (!research || !issue) {
      errorDiv.textContent = "Both Research Brief and Issue Brief are required.";
      outputDiv.textContent = "";
      generateBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/generate-outlines", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ research_brief: research, issue_brief: issue })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = data.outlines_markdown;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      generateBtn.disabled = false;
    }
  });
});
