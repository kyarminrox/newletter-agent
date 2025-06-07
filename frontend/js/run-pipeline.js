document.addEventListener("DOMContentLoaded", () => {
  const metricsInput = document.getElementById("metrics");
  const queryInput = document.getElementById("query");
  const issueInput = document.getElementById("issue");
  const coverInput = document.getElementById("cover");
  const titleInput = document.getElementById("title");
  const slugInput = document.getElementById("slug");
  const tagsInput = document.getElementById("tags");
  const publishInput = document.getElementById("publish");
  const runBtn = document.getElementById("runBtn");
  const outputDiv = document.getElementById("output");
  const errorDiv = document.getElementById("error");

  runBtn.addEventListener("click", async () => {
    errorDiv.textContent = "";
    outputDiv.textContent = "Running pipeline…";
    runBtn.disabled = true;

    const metrics = metricsInput.value.trim();
    const query = queryInput.value.trim();
    const issue = issueInput.value.trim();
    const cover = coverInput.value.trim();
    const title = titleInput.value.trim();
    const slug = slugInput.value.trim();
    const tags = tagsInput.value
      .split(",")
      .map((t) => t.trim())
      .filter((t) => t.length > 0);
    const publish = publishInput.value.trim();

    if (!metrics || !query || !issue || !cover || !title || !slug || tags.length === 0 || !publish) {
      errorDiv.textContent = "All fields are required, including tags.";
      outputDiv.textContent = "";
      runBtn.disabled = false;
      return;
    }

    try {
      const resp = await fetch("/api/run-pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          metrics_csv: metrics,
          research_query: query,
          issue_brief: issue,
          cover_image: cover,
          title: title,
          slug: slug,
          tags: tags,
          publish_date: publish
        })
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      outputDiv.textContent = `Pipeline complete. ZIP at: ${data.package_zip_path}`;
    } catch (err) {
      errorDiv.textContent = `Request failed: ${err.message}`;
      outputDiv.textContent = "";
    } finally {
      runBtn.disabled = false;
    }
  });
});
