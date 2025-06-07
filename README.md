### Outline Architect (Generate Outlines)

1. **Ensure you have a Research Brief** from Insight Scout and an Issue Brief.  
2. **Run the FastAPI server** if it's not already running:  
   ```bash
   uvicorn src.api:app --reload
Open the frontend page:
frontend/generate-outlines.html (via file:// URL).

Paste the Research Brief Markdown into the first textarea and enter your Issue Brief text.

Click Generate Outlines. The page will display three Markdown outlines, each beginning with # Outline Option.

Draftsmith (Create Draft from Outline)
Ensure you have a chosen Outline (Markdown) from Outline Architect.

Run the FastAPI server if it's not already running:

bash
Copy
Edit
uvicorn src.api:app --reload
Open the frontend page:
frontend/generate-draft.html (via file:// URL).

Paste one of the # Outline Option blocks into the textarea.

Click Create Draft. The page displays a full Markdown draft beginning with <!-- COVER_IMAGE_HOOK -->.

Editor-in-Chief (Polish Draft)
Ensure you have a full draft (Markdown) from Draftsmith or uploaded.

Run the FastAPI server if it's not already running:

bash
Copy
Edit
uvicorn src.api:app --reload
Open the frontend page:
frontend/generate-edit.html (via file:// URL).

Paste the entire draft Markdown into the textarea.

Click Edit Draft. The page shows the polished Markdown and a revision summary under the respective headings.

Creative Director (Suggest Visuals)
Ensure you have a polished draft excerpt from Editor-in-Chief.

Run the FastAPI server if it's not already running:

bash
Copy
Edit
uvicorn src.api:app --reload
Open the frontend page:
frontend/generate-visuals.html (via file:// URL).

Paste the first few paragraphs of your polished draft into the textarea.

Click Suggest Visuals. The page shows three lines, each containing a description and a text-to-image prompt separated by a tab.

Metrics Forecaster (Forecast Performance)
Ensure you have a metrics CSV with at least 3 past issues (columns: IssueDate, SubjectLine, OpenRate).

Run the FastAPI server if it's not already running:

bash
Copy
Edit
uvicorn src.api:app --reload
Open the frontend page:
frontend/generate-forecast.html (via file:// URL).

In the Metrics CSV Path field, enter the relative path, e.g. data/metrics/metrics_2025-06-01.csv.

In Subject Lines, enter each candidate subject line on its own line.

Click Forecast Performance. The page displays a Markdown forecast. If too little history exists, a stub forecast explains the default assumptions.

yaml
Copy
Edit

---  
**Next steps**:  
1. Replace that conflicted block in `README.md` with the above.  
2. Remove the `<<<<<<<`, `=======`, and `>>>>>>>` lines.  
3. Save, then:

```bash
git add README.md
git commit