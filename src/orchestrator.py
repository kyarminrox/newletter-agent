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

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Step a) ingest data
    ingest_metrics(args.metrics_csv)
    try:
        ingest_content("data/content")
    except Exception:
        pass

    # Step b) research brief
    scout = InsightScout()
    research_md = scout.fetch_research_brief(args.metrics_csv, args.research_query)
    research_path = output_dir / "research.md"
    research_path.write_text(research_md, encoding="utf-8")

    # Step c) outlines
    architect = OutlineArchitect()
    outlines_md = architect.generate_outlines(research_md, args.issue_brief)
    outlines_path = output_dir / "outlines.md"
    outlines_path.write_text(outlines_md, encoding="utf-8")

    # parse first outline
    subject_lines = parse_subject_lines(outlines_md)
    first_outline = outlines_md.split("# Outline Option 1", 1)[-1]
    if "# Outline Option 2" in first_outline:
        first_outline = first_outline.split("# Outline Option 2", 1)[0]
    first_outline = "# Outline Option 1" + first_outline if not first_outline.startswith("# Outline Option 1") else first_outline

    # Step d) draft
    smith = Draftsmith()
    draft_md = smith.create_draft(first_outline)
    draft_path = output_dir / "draft.md"
    draft_path.write_text(draft_md, encoding="utf-8")

    # Step e) edit draft
    editor = EditorInChief()
    polished_md, summary_md = editor.edit_draft(draft_md)
    polished_path = output_dir / "polished.md"
    polished_path.write_text(polished_md, encoding="utf-8")
    summary_path = output_dir / "revision_summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")

    # Step f) visuals
    director = CreativeDirector()
    excerpt = polished_md[:500]
    visuals_txt = director.suggest_visuals(excerpt)
    visuals_path = output_dir / "visuals.txt"
    visuals_path.write_text(visuals_txt, encoding="utf-8")

    # Step g) forecast
    forecaster = MetricsForecaster()
    forecast_md = forecaster.forecast(args.metrics_csv, subject_lines)
    forecast_path = output_dir / "forecast.md"
    forecast_path.write_text(forecast_md, encoding="utf-8")

    # Step h) package for substack
    fmt = Formatter()
    zip_path = fmt.package_for_substack(
        draft_path=str(polished_path),
        cover_image_path=args.cover_image,
        title=args.title,
        slug=args.slug,
        tags=[t.strip() for t in args.tags.split(',') if t.strip()],
        publish_date=args.publish_date,
    )

    # Step i) performance analysis
    analyst = PerformanceAnalyst()
    analysis_md = analyst.analyze(forecast_md, args.metrics_csv)
    analysis_path = output_dir / "analysis.md"
    analysis_path.write_text(analysis_md, encoding="utf-8")

    print(f"Pipeline complete. Package created at: {zip_path}")


if __name__ == "__main__":
    main()
