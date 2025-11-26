"""
Display and presentation utilities for Jupyter notebooks.
"""
import base64
from typing import Any

import pandas as pd
from IPython.display import display, HTML


def print_html(content: Any, title: str | None = None, is_image: bool = False, is_html: bool = False):
    """
    Pretty-print inside a styled card.
    - If is_image=True and content is a string: treat as image path/URL and render <img>.
    - If content is a pandas DataFrame/Series: render as an HTML table.
    - Otherwise (strings/otros): show as code/text in <pre><code>.
    """
    try:
        from html import escape as _escape
    except ImportError:
        _escape = lambda x: x

    def image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # Render content
    if is_image and isinstance(content, str):
        b64 = image_to_base64(content)
        rendered = f'<img src="data:image/png;base64,{b64}" alt="Image" style="max-width:100%; height:auto; border-radius:8px;">'
    elif isinstance(content, pd.DataFrame):
        rendered = content.to_html(classes="pretty-table", index=False, border=0, escape=False)
    elif isinstance(content, pd.Series):
        rendered = content.to_frame().to_html(classes="pretty-table", border=0, escape=False)
    elif is_html and isinstance(content, str):
        rendered = content  # Pass through raw HTML
    elif isinstance(content, str):
        rendered = f"<pre><code>{_escape(content)}</code></pre>"
    else:
        rendered = f"<pre><code>{_escape(str(content))}</code></pre>"

    css = """
    <style>
    .pretty-card{
      font-family: ui-sans-serif, system-ui;
      border: 2px solid transparent;
      border-radius: 14px;
      padding: 14px 16px;
      margin: 10px 0;
      background: linear-gradient(#fff, #fff) padding-box,
                  linear-gradient(135deg, #3b82f6, #9333ea) border-box;
      color: #111;
      box-shadow: 0 4px 12px rgba(0,0,0,.08);
    }
    .pretty-title{
      font-weight:700;
      margin-bottom:8px;
      font-size:14px;
      color:#111;
    }
    /* 🔒 Solo afecta lo DENTRO de la tarjeta */
    .pretty-card pre,
    .pretty-card code {
      background: #f3f4f6;
      color: #111;
      padding: 8px;
      border-radius: 8px;
      display: block;
      overflow-x: auto;
      font-size: 13px;
      white-space: pre-wrap;
    }
    .pretty-card img { max-width: 100%; height: auto; border-radius: 8px; }
    .pretty-card table.pretty-table {
      border-collapse: collapse;
      width: 100%;
      font-size: 13px;
      color: #111;
    }
    .pretty-card table.pretty-table th,
    .pretty-card table.pretty-table td {
      border: 1px solid #e5e7eb;
      padding: 6px 8px;
      text-align: left;
    }
    .pretty-card table.pretty-table th { background: #f9fafb; font-weight: 600; }
    </style>
    """

    title_html = f'<div class="pretty-title">{title}</div>' if title else ""
    card = f'<div class="pretty-card">{title_html}{rendered}</div>'
    display(HTML(css + card))


def display_rubric_scores(result: dict[str, Any], title: str = "LLM Judge Evaluation"):
    """
    Display LLM judge results in a styled card with score bars.

    Args:
        result: Output from llm_judge()
        title: Title for the display card
    """
    scores = result.get("scores", {})
    explanations = result.get("explanations", {})
    overall = result.get("overall", 0)

    # Build score bars HTML
    bars_html = ""
    for dim, score in scores.items():
        pct = (score / 5) * 100  # Assuming 1-5 scale
        explanation = explanations.get(dim, "")
        bars_html += f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600; text-transform: capitalize;">{dim}</span>
                <span style="font-weight: 700;">{score}/5</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #3b82f6, #9333ea); width: {pct}%; height: 100%;"></div>
            </div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">{explanation}</div>
        </div>
        """

    # Overall score
    overall_html = f"""
    <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #e5e7eb;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; font-size: 16px;">Overall Score</span>
            <span style="font-weight: 700; font-size: 20px; color: #3b82f6;">{overall}/5</span>
        </div>
    </div>
    """

    # Check for errors
    error_html = ""
    if "error" in result:
        error_html = f'<div style="color: #dc2626; margin-top: 8px;">Error: {result["error"]}</div>'

    full_html = bars_html + overall_html + error_html
    print_html(full_html, title=title, is_html=True)


def display_test_results(results: list[dict], title: str = "Test Results"):
    """
    Display test results in a styled card with pass/fail indicators.

    Args:
        results: List of dicts with 'question', 'expected', 'actual', 'passed' keys
        title: Title for the display card
    """
    passed_count = sum(1 for r in results if r.get("passed"))
    total = len(results)

    # Build rows HTML
    rows_html = ""
    for i, r in enumerate(results, 1):
        passed = r.get("passed", False)
        icon = "✓" if passed else "✗"
        color = "#22c55e" if passed else "#ef4444"
        bg = "#f0fdf4" if passed else "#fef2f2"

        rows_html += f"""
        <div style="margin-bottom: 12px; padding: 10px; background: {bg}; border-radius: 8px; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
                <span style="font-weight: 600; color: #374151;">Q{i}: {r.get('question', '')}{'...' if len(r.get('question', '')) > 60 else ''}</span>
                <span style="font-weight: 700; color: {color}; font-size: 18px;">{icon}</span>
            </div>
            <div style="font-size: 13px; color: #6b7280;">
                <span>Expected: <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">{r.get('expected', '')}</code></span>
                <span style="margin-left: 16px;">Got: <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">{str(r.get('actual') or '')[:40]}{'...' if len(str(r.get('actual') or '')) > 40 else ''}</code></span>
            </div>
        </div>
        """

    # Summary
    pct = (passed_count / total * 100) if total > 0 else 0
    summary_color = "#22c55e" if passed_count == total else "#f59e0b" if passed_count > 0 else "#ef4444"
    summary_html = f"""
    <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #e5e7eb;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; font-size: 16px;">Total</span>
            <span style="font-weight: 700; font-size: 20px; color: {summary_color};">{passed_count}/{total} passed</span>
        </div>
    </div>
    """

    full_html = rows_html + summary_html
    print_html(full_html, title=title, is_html=True)
