document.addEventListener("DOMContentLoaded", () => {
  const draftInput = document.getElementById("draftInput");
  const editBtn = document.getElementById("editBtn");
  const polishedDiv = document.getElementById("polished");
  const summaryDiv = document.getElementById("summary");
  const errorDiv = document.getElementById("error");

  editBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    polishedDiv.textContent = "Editing draft…";
    summaryDiv.textContent = "";
    editBtn.disabled = true;

    const draft = draftInput.value.trim();
    if (!draft) {
      errorDiv.textContent = "Draft Markdown is required.";
      polishedDiv.textContent = "";
      summaryDiv.textContent = "";
      editBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/edit-draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ draft_markdown: draft })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      polishedDiv.textContent = data.polished_markdown;
      summaryDiv.textContent = data.revision_summary;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      polishedDiv.textContent = "";
      summaryDiv.textContent = "";
    } finally {
      editBtn.disabled = false;
    }
  });
});
