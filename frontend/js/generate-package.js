// frontend/js/generate-package.js
document.addEventListener("DOMContentLoaded", () => {
  const draftInput = document.getElementById("draftPath");
  const coverInput = document.getElementById("coverPath");
  const titleInput = document.getElementById("titleInput");
  const slugInput = document.getElementById("slugInput");
  const tagsInput = document.getElementById("tagsInput");
  const publishDateInput = document.getElementById("publishDateInput");
  const packageBtn = document.getElementById("packageBtn");
  const zipPathDiv = document.getElementById("zipPath");
  const errorDiv = document.getElementById("error");

  packageBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    zipPathDiv.textContent = "Packaging…";
    packageBtn.disabled = true;

    const draftPath = draftInput.value.trim();
    const coverPath = coverInput.value.trim();
    const title = titleInput.value.trim();
    const slug = slugInput.value.trim();
    const tags = tagsInput.value.split(",").map(t => t.trim()).filter(t => t.length > 0);
    const publishDate = publishDateInput.value.trim();

    if (!draftPath || !coverPath || !title || !slug || tags.length === 0 || !publishDate) {
      errorDiv.textContent = "All fields are required, including at least one tag.";
      zipPathDiv.textContent = "";
      packageBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/package-for-substack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          draft_path: draftPath,
          cover_image_path: coverPath,
          title: title,
          slug: slug,
          tags: tags,
          publish_date: publishDate
        })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      const zipPath = data.package_zip_path;
      zipPathDiv.innerHTML = `<a href="${zipPath}" class="download-link" download>Download Package ZIP</a>`;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      zipPathDiv.textContent = "";
    } finally {
      packageBtn.disabled = false;
    }
  });
});
