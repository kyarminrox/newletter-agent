import argparse
import os
from pathlib import Path

from src.agents.data_collector import ingest_metrics, ingest_content
from src.agents.insight_scout import InsightScout
from src.agents.outline_architect import OutlineArchitect
from src.agents.draftsmith import Draftsmith
from src.agents.editor_in_chief import EditorInChief
from src.agents.creative_director import CreativeDirector
from src.agents.metrics_forecaster import MetricsForecaster
from src.agents.formatter import Formatter
from src.agents.performance_analyst import PerformanceAnalyst


def parse_subject_lines(outline: str) -> list[str]:
    """Extract subject lines from the first outline option."""
    import re

    # Get first outline block
    start = outline.find("# Outline Option 1")
    if start == -1:
        block = outline
    else:
        end = outline.find("# Outline Option 2", start)
        block = outline[start:end if end != -1 else len(outline)]

    subject_lines = []
    if "## Subject Line Candidates" in block:
        section = block.split("## Subject Line Candidates", 1)[1]
        for line in section.splitlines():
            line = line.strip()
            if line.startswith("-"):
                subject = line.lstrip("-").strip().strip('"')
                if subject:
                    subject_lines.append(subject)
            elif subject_lines:
                # stop when leaving list
                if not line.startswith("-"):
                    break
    return subject_lines


def run_pipeline(
    *,
    metrics_csv: str,
    research_query: str,
    issue_brief: str,
    cover_image: str,
    title: str,
    slug: str,
    tags: list[str],
    publish_date: str,
) -> str:
    """Run the full pipeline and return the created ZIP path."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    ingest_metrics(metrics_csv)
    try:
        ingest_content("data/content")
    except Exception:
        pass

    scout = InsightScout()
    research_md = scout.fetch_research_brief(metrics_csv, research_query)
    (output_dir / "research.md").write_text(research_md, encoding="utf-8")

    architect = OutlineArchitect()
    outlines_md = architect.generate_outlines(research_md, issue_brief)
    (output_dir / "outlines.md").write_text(outlines_md, encoding="utf-8")

    subject_lines = parse_subject_lines(outlines_md)
    first_outline = outlines_md.split("# Outline Option 1", 1)[-1]
    if "# Outline Option 2" in first_outline:
        first_outline = first_outline.split("# Outline Option 2", 1)[0]
    if not first_outline.startswith("# Outline Option 1"):
        first_outline = "# Outline Option 1" + first_outline

    smith = Draftsmith()
    draft_md = smith.create_draft(first_outline)
    (output_dir / "draft.md").write_text(draft_md, encoding="utf-8")

    editor = EditorInChief()
    polished_md, summary_md = editor.edit_draft(draft_md)
    polished_path = output_dir / "polished.md"
    polished_path.write_text(polished_md, encoding="utf-8")
    (output_dir / "revision_summary.md").write_text(summary_md, encoding="utf-8")

    director = CreativeDirector()
    visuals_txt = director.suggest_visuals(polished_md[:500])
    (output_dir / "visuals.txt").write_text(visuals_txt, encoding="utf-8")

    forecaster = MetricsForecaster()
    forecast_md = forecaster.forecast(metrics_csv, subject_lines)
    (output_dir / "forecast.md").write_text(forecast_md, encoding="utf-8")

    fmt = Formatter()
    zip_path = fmt.package_for_substack(
        draft_path=str(polished_path),
        cover_image_path=cover_image,
        title=title,
        slug=slug,
        tags=tags,
        publish_date=publish_date,
    )

    analyst = PerformanceAnalyst()
    analysis_md = analyst.analyze(forecast_md, metrics_csv)
    (output_dir / "analysis.md").write_text(analysis_md, encoding="utf-8")

    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Run newsletter pipeline")
    parser.add_argument("--metrics-csv", required=True, help="Path to metrics CSV")
    parser.add_argument("--research-query", required=True, help="Research query")
    parser.add_argument("--issue-brief", required=True, help="Issue brief text")
    parser.add_argument("--cover-image", required=True, help="Cover image path")
    parser.add_argument("--title", required=True, help="Newsletter title")
    parser.add_argument("--slug", required=True, help="URL slug")
    parser.add_argument("--tags", required=True, help="Comma-separated tags")
    parser.add_argument("--publish-date", required=True, help="Publish date ISO8601")
    args = parser.parse_args()

    zip_path = run_pipeline(
        metrics_csv=args.metrics_csv,
        research_query=args.research_query,
        issue_brief=args.issue_brief,
        cover_image=args.cover_image,
        title=args.title,
        slug=args.slug,
        tags=[t.strip() for t in args.tags.split(',') if t.strip()],
        publish_date=args.publish_date,
    )

    print(f"Pipeline complete. Package created at: {zip_path}")


if __name__ == "__main__":
    main()