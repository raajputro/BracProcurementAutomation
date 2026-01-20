from __future__ import annotations

import os
import time
import shutil
# import datetime
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

import pytest
import pyautogui
import webbrowser
from pytest_html import extras

from playwright.sync_api import (
    Playwright,
    sync_playwright,
    Browser,
    BrowserContext,
    Page,
    Locator,
)

import pathlib

try:
    import yaml
except ImportError:
    yaml = None

# =========================
# Config
# =========================
headless_flag = False  # set True in CI
slow_mo_speed = 1700  # reduce in CI

ARTIFACTS_DIR = Path("artifacts")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"

screen_width, screen_height = pyautogui.size()
print(f"Artifacts path: {ARTIFACTS_DIR}")
print(f"Running on screen size: {screen_width}x{screen_height}")


# =========================
# Auto-highlighter settings
# =========================
def _env_truthy(val: str | None) -> bool:
    if val is None:
        return True
    return val.strip().lower() not in {"0", "false", "off", "no"}


HIGHLIGHT_ENABLED = _env_truthy(os.getenv("HIGHLIGHT_ELEMENTS", "1"))
try:
    HIGHLIGHT_DURATION_MS = int(os.getenv("HIGHLIGHT_MS", "800"))
except ValueError:
    HIGHLIGHT_DURATION_MS = 800

ACTION_COLORS = {
    "click": "red",
    "dblclick": "red",
    "press": "red",
    "fill": "green",
    "type": "green",
    "select_option": "green",
    "focus": "green",
    "hover": "blue",
    "check": "purple",
    "uncheck": "purple",
}

# =========================
# Globals
# =========================
global_browser: Optional[Browser] = None
global_context: Optional[BrowserContext] = None
global_pages: list[Page] = []  # last page is the most recent
test_failures: list[dict] = []

# === BRAC_Digital_Marketplace_METRICS SUMMARY & CHART (NEW) =========================
# Collect overall metrics for top summary + donut chart
BRAC_Digital_Marketplace_METRICS = {
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "durations": [],  # seconds
}


# ========================================================

# === Read pytest_html_report.yml so confest is reusable ==============
def load_report_config():
    """
    Read pytest_html_report.yml (if present) and return:
    - title
    - test_environment
    - primary_color
    Fallback to sensible defaults if the file or PyYAML is missing.
    """
    default_title = "Playwright Tests"
    default_env = "local"
    default_color = "#2E7D32"

    cfg_path = Path("pytest_html_report.yml")
    if yaml is None or not cfg_path.exists():
        return default_title, default_env, default_color

    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        return default_title, default_env, default_color

    report_cfg = cfg.get("report", {})
    theme_cfg = cfg.get("theme", {})

    title = report_cfg.get("title", default_title)
    env = report_cfg.get("test_environment", default_env)
    color = theme_cfg.get("primary_color", default_color)

    return title, env, color


REPORT_TITLE, REPORT_ENV, PRIMARY_COLOR = load_report_config()


# ======================================================================


# =========================
# Utilities
# =========================
def safe_file_operation(file_path: Path, operation, max_retries=5, delay=1):
    for attempt in range(max_retries):
        try:
            return operation(file_path)
        except (PermissionError, OSError):
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)


def wait_until_file_unlocked(path: Path, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            with open(path, 'rb'):
                return True
        except PermissionError:
            time.sleep(0.5)
    raise TimeoutError(f"File {path} still locked after {timeout} seconds")


# =========================
# Pytest setup
# =========================
def pytest_configure(config):
    # fresh artifacts dir per run
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    # HTML report setup
    if not getattr(config.option, "flightpath", None):
        # if not getattr(config.option, "htmlpath", None):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = ARTIFACTS_DIR / "reports" / f"report_{timestamp}.html"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        config.option.flightpath = str(report_file)


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    global global_browser
    if global_browser is None:
        global_browser = playwright.chromium.launch(
            headless=headless_flag,
            slow_mo=slow_mo_speed,
            args=[
                "--start-maximized",
                "--window-position=0,0",
                "--high-dpi-support=1",
                "--force-device-scale-factor=1",
                "--ignore-certificate-errors",
            ],
        )
    yield global_browser
    if global_browser:
        global_browser.close()
        global_browser = None


@pytest.fixture(scope="session")
def context(browser: Browser) -> BrowserContext:
    """Single context for the session. Per-test tracing is handled by an autouse fixture below."""
    global global_context, global_pages

    if global_context is None:
        global_context = browser.new_context(
            viewport={"width": screen_width, "height": screen_height},
            device_scale_factor=1,
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": screen_width, "height": screen_height},
            ignore_https_errors=True,
        )

        # Track all new pages/tabs
        def on_page(page: Page):
            global_pages.append(page)

        global_context.on("page", on_page)

        # Install action highlighter
        if HIGHLIGHT_ENABLED:
            _install_auto_highlighter()

    yield global_context

    # Close context → flush videos to disk
    try:
        global_context.close()
    except Exception:
        pass
    global_context = None
    global_pages.clear()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Return the main page. Create if first use; reuse for speed."""
    global global_pages
    if not global_pages:
        pg = context.new_page()
        global_pages.append(pg)
    main = global_pages[0]
    main.bring_to_front()
    return main


#### changing this to open new tab helper ####


@pytest.fixture(scope="function")
def new_tab(context: BrowserContext) -> Callable[[Callable[[Page], None]], Page]:
    """
    Helper fixture to open a new browser tab.

    Usage in a test:
        def test_something(page, new_tab):
            other_page = new_tab(lambda p: p.click("a[target='_blank']"))
    """

    def _open(action: Callable[[Page], None]) -> Page:
        global global_pages
        with context.expect_page() as new_page_info:
            action(global_pages[-1])
        pg = new_page_info.value
        global_pages.append(pg)
        pg.bring_to_front()
        return pg

    return _open


# =========================
# Per-test tracing (ZIP)
# =========================
@pytest.fixture(autouse=True)
def trace_per_test(request: pytest.FixtureRequest, context: BrowserContext):
    """Start Playwright tracing before each test, stop after, save to artifacts/traces."""
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_path = TRACES_DIR / f"{timestamp}_{test_name}_trace.zip"

    try:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    except Exception:
        pass

    yield

    try:
        context.tracing.stop(path=str(trace_path))
        setattr(request.node, "_pw_trace_path", trace_path)
    except Exception:
        pass


# =========================
# ONE report hook (pytest-html compatible)
# =========================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    SINGLE hook: attaches failure screenshot and per-test trace link to pytest-html report.
    Avoids inserting raw lists into table cells (which caused your earlier INTERNALERROR).
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when != "call":
        return

    # On failure: take screenshot of the last page (if any) and attach to pytest-html
    if rep.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shot = SCREENSHOTS_DIR / f"{timestamp}_{item.name}.png"

        # Find a page to screenshot
        page_to_shoot: Optional[Page] = None
        try:
            from conftest import global_pages  # same module
            if global_pages:
                page_to_shoot = global_pages[-1]
        except Exception:
            pass

        if page_to_shoot:
            try:
                page_to_shoot.screenshot(path=str(shot), full_page=True)
            except Exception:
                pass

        if item.config.pluginmanager.hasplugin("html"):
            # Attach screenshot
            extra_list = getattr(rep, "extra", [])
            if shot.exists():
                extra_list.append(extras.image(str(shot)))
            # Attach trace link (if saved by trace_per_test)
            trace_path = getattr(item, "_pw_trace_path", None)
            if isinstance(trace_path, Path) and trace_path.exists():
                # Link to file; HTML report is self-contained otherwise
                extra_list.append(extras.url(str(trace_path), name="Playwright Trace ZIP"))
            rep.extra = extra_list


# import logging
#
#
# @pytest.fixture
# def logger():
#     logger = logging.getLogger("test-logger")
#     logger.setLevel(logging.INFO)
#
#     if not logger.handlers:
#         handler = logging.StreamHandler()
#         formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#
#     return logger

# =========================
# Auto-highlighter implementation
# =========================
def highlight_selector(page: Page, selector: str, action: str, duration_ms: int = HIGHLIGHT_DURATION_MS):
    """Outline a CSS/XPath selector temporarily (best-effort)."""
    try:
        color = ACTION_COLORS.get(action, "red")
        # If selector looks like XPath, try a query first to ensure it's attached
        if selector.strip().startswith(("//", "xpath=", "css=")) is False:
            page.wait_for_selector(selector, state="attached", timeout=1500)
        page.eval_on_selector(
            selector if selector.startswith(("css=", "xpath=")) is False else selector.replace("css=", "").replace(
                "xpath=", ""),
            f"""(el) => {{
                const prev = el.style.outline;
                el.style.outline = '3px solid {color}';
                setTimeout(() => {{ el.style.outline = prev; }}, {duration_ms});
            }}"""
        )
    except Exception:
        pass


def highlight_locator(locator: Locator, action: str, duration_ms: int = HIGHLIGHT_DURATION_MS):
    """Outline the element behind a Locator temporarily (best-effort)."""
    try:
        color = ACTION_COLORS.get(action, "red")
        locator.evaluate(
            f"""(el) => {{
                const prev = el.style.outline;
                el.style.outline = '3px solid {color}';
                setTimeout(() => {{ el.style.outline = prev; }}, {duration_ms});
            }}"""
        )
    except Exception:
        pass


def _install_auto_highlighter():
    """Monkey-patch Page and Locator interaction methods to auto-highlight targets."""
    if getattr(Page, "_auto_highlight_installed", False):
        return

    page_methods = list(ACTION_COLORS.keys())
    locator_methods = list(ACTION_COLORS.keys())

    # Patch Page methods
    for method_name in page_methods:
        if not hasattr(Page, method_name):
            continue
        original = getattr(Page, method_name)

        def make_wrapper(_original, _method_name):
            def wrapper(self: Page, selector: str, *args, **kwargs):
                if HIGHLIGHT_ENABLED and isinstance(selector, str):
                    try:
                        highlight_selector(self, selector, _method_name)
                    except Exception:
                        pass
                return _original(self, selector, *args, **kwargs)

            return wrapper

        setattr(Page, method_name, make_wrapper(original, method_name))

    # Patch Locator methods
    for method_name in locator_methods:
        if not hasattr(Locator, method_name):
            continue
        original = getattr(Locator, method_name)

        def make_loc_wrapper(_original, _method_name):
            def wrapper(self: Locator, *args, **kwargs):
                if HIGHLIGHT_ENABLED:
                    try:
                        highlight_locator(self, _method_name)
                    except Exception:
                        pass
                return _original(self, *args, **kwargs)

            return wrapper

        setattr(Locator, method_name, make_loc_wrapper(original, method_name))

    setattr(Page, "_auto_highlight_installed", True)


# =========================
# Optional: soft assertion logging (pytest-check)
# =========================
try:
    import pytest_check
except ImportError:
    pytest_check = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    """If pytest-check is installed, print soft assertion errors at the end of each test call."""
    outcome = yield
    if pytest_check:
        errors = getattr(pytest_check, "_errors", [])
        for e in errors:
            print(f"🔸 Soft check failure in {item.name}: {e}")


# =========================
# BRAC Digital Marketplace summary + donut chart injection into pytest-html-report (CLEAN)
# =========================
def pytest_runtest_logreport(report: pytest.TestReport):
    """
    Collect per-test status and duration for overall summary.
    We only care about the 'call' phase (the actual test body).
    """
    if report.when != "call":
        return

    if report.passed:
        BRAC_Digital_Marketplace_METRICS["passed"] += 1
    elif report.failed:
        BRAC_Digital_Marketplace_METRICS["failed"] += 1
    elif report.skipped:
        BRAC_Digital_Marketplace_METRICS["skipped"] += 1

    BRAC_Digital_Marketplace_METRICS["durations"].append(getattr(report, "duration", 0.0))


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int):
    """
    After pytest-html-report writes the HTML file, open the newest report under
    artifacts/reports and inject:
      - our own white header + cards + donut chart at the top
      - a small JS snippet that hides the old green header (second top-level div).
    """
    reports_dir = Path("artifacts") / "reports"
    if not reports_dir.exists():
        return

    html_files = list(reports_dir.glob("report_*.html"))
    if not html_files:
        return

    latest = max(html_files, key=lambda p: p.stat().st_mtime)
    html = latest.read_text(encoding="utf-8")

    # ---- 1) Remove previous injection (avoid duplicates on reruns) ----
    start_token = "<!-- BRAC Digital Marketplace SUMMARY START -->"
    end_token = "<!-- BRAC Digital Marketplace SUMMARY END -->"
    if start_token in html and end_token in html:
        before, _, rest = html.partition(start_token)
        _, _, after = rest.partition(end_token)
        html = before + after

        # ---- 2) Compute metrics ----
    passed = BRAC_Digital_Marketplace_METRICS["passed"]
    failed = BRAC_Digital_Marketplace_METRICS["failed"]
    skipped = BRAC_Digital_Marketplace_METRICS["skipped"]

    total_tests = passed + failed + skipped
    if total_tests == 0:
        total_tests = 1

    total_duration = sum(BRAC_Digital_Marketplace_METRICS["durations"])
    avg_time = total_duration / total_tests

    def fmt_secs(s: float) -> str:
        """Simple seconds, e.g. 19.7s (for Avg Test Time)."""
        return f"{s:.1f}s"

    def fmt_duration_long(s: float) -> str:
        """Minutes + seconds, e.g. 1m 54.6s (for Run Duration)."""
        m = int(s // 60)
        sec = s - m * 60
        if m:
            return f"{m}m {sec:.1f}s"
        return f"{sec:.1f}s"

    # ---- 3) Our header + cards + donut (wrapped in a root div) ----
    now_str = datetime.now().strftime("%d %b %Y, %H:%M")

    summary_block = f"""
<!-- BRAC Digital Marketplace SUMMARY START -->
<div id="BRAC Digital Marketplace-summary-root">
  <div style="background:{PRIMARY_COLOR};padding:16px 32px 8px 32px;border-bottom:1px solid #e0e0e0;color:#ffffff;">
    <div style="font-size:24px;font-weight:600;">📊 {REPORT_TITLE}</div>
    <div style="font-size:13px;margin-top:4px;color:#ffffff;">
      Report generation time: {now_str}
      &nbsp;&nbsp;&nbsp;
      Test Environment: {REPORT_ENV}
    </div>
  </div>

  <div style="background:#ffffff;margin:0;padding:16px 0 24px 0;">
    <div style="max-width:1200px;margin:0 auto;padding:0 24px;">

      <!-- Top stats cards -->
      <div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:flex-start;">
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Total Tests</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;">{passed + failed + skipped}</div>
        </div>
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Passed</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;color:#2e7d32;">{passed}</div>
        </div>
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Failed</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;color:#c62828;">{failed}</div>
        </div>
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Skipped</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;color:#f9a825;">{skipped}</div>
        </div>
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Avg. Test Time</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;">{fmt_secs(avg_time)}</div>
        </div>
        <div style="flex:1 1 140px;min-width:140px;padding:12px 16px;border-radius:16px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
          <div style="font-size:12px;color:#555;">Run Duration</div>
          <div style="font-size:24px;font-weight:600;margin-top:4px;">{fmt_duration_long(total_duration)}</div>
        </div>
      </div>

      <!-- Centered donut chart -->
      <div style="margin-top:32px;text-align:center;">
        <h3 style="margin:0 0 12px 0;font-size:16px;text-align:left;">Test Distribution</h3>
        <div style="width:200px;height:200px;margin:0 auto;">
          <canvas id="BRAC Digital MarketplaceStatusChart"
                  style="width:200px!important;height:200px!important;max-width:200px;max-height:220px;">
          </canvas>
        </div>
        <!-- counts + % legend like your screenshot 3 -->
        <div id="BRAC Digital MarketplaceStatusLegend" style="margin-top:12px;text-align:center;font-size:13px;color:#374151;"></div>
      </div>

    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  (function() {{

    function buildChart() {{
      var canvas = document.getElementById('BRAC Digital MarketplaceStatusChart');
      if (!canvas) return;

      var ctx = canvas.getContext('2d');
      var passed = {passed};
      var failed = {failed};
      var skipped = {skipped};
      var total = passed + failed + skipped;
      if (total === 0) total = 1;

      var passPct = (passed / total) * 100;
      var failPct = (failed / total) * 100;
      var skipPct = (skipped / total) * 100;

      // Center text plugin: "93%" (big, green) + "Passed" (below)
      var centerText = {{
        id: 'centerText',
        afterDraw(chart, args, opts) {{
          var {{ctx, chartArea: {{left, right, top, bottom}}}} = chart;
          var cx = (left + right) / 2;
          var cy = (top + bottom) / 2;
          ctx.save();
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';

          // 93%
          ctx.font = 'bold 22px Arial';
          ctx.fillStyle = '#2e7d32';
          ctx.fillText(Math.round(passPct) + '%', cx, cy - 6);

          // "Passed"
          ctx.font = '14px Arial';
          ctx.fillStyle = '#374151';
          ctx.fillText('Passed', cx, cy + 14);

          ctx.restore();
        }}
      }};

      var chart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
          labels: ['Passed', 'Failed', 'Skipped'],
          datasets: [{{
            data: [passed, failed, skipped],
            backgroundColor: ['#4CAF50', '#F44336', '#FFC107'],
            hoverOffset: 4
          }}]
        }},
        options: {{
          responsive: false,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {{
            legend: {{ display: false }}
          }}
        }},
        plugins: [centerText]
      }});

      // Custom legend with counts + percentages (like screenshot 3)
      var legend = document.getElementById('BRAC Digital MarketplaceStatusLegend');
      if (legend) {{
        legend.innerHTML =
          '<div style="display:inline-flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:center;">' +
            '<div style="display:flex;align-items:center;gap:6px;">' +
              '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#4CAF50;"></span>' +
              '<span>Passed ' + passed + ' (' + passPct.toFixed(1) + '%)</span>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:6px;">' +
              '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#F44336;"></span>' +
              '<span>Failed ' + failed + ' (' + failPct.toFixed(1) + '%)</span>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:6px;">' +
              '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#FFC107;"></span>' +
              '<span>Skipped ' + skipped + ' (' + skipPct.toFixed(1) + '%)</span>' +
            '</div>' +
          '</div>';
      }}
    }}

    function hideOldHeader() {{
      var summaryRoot = document.getElementById('BRAC Digital Marketplace-summary-root');
      // Look at top-level DIVs and HEADERs under <body>
      var candidates = Array.from(document.querySelectorAll('body > div, body > header'));
      candidates.forEach(function(div) {{
        if (div === summaryRoot) return;
        var text = (div.textContent || '').trim();
        if (text.includes("{REPORT_TITLE}") &&
            text.includes("Report generation time") &&
            text.includes("Test Environment")) {{
          div.style.display = 'none';
        }}
      }});
    }}

    // 🔴 hide DEVELOPER & CATEGORIES columns by header text
    function hideReportColumns() {{
      var headersToHide = ['DEVELOPER', 'CATEGORIES'];
      var anyHidden = false;

      var tables = document.querySelectorAll('div.detail-table-wrapper table');
      tables.forEach(function(tbl) {{
        // first row in tbody is the header row
        var headRow = tbl.querySelector('tbody tr:first-child');
        if (!headRow) return;

        var cells = Array.from(headRow.children);  // th elements
        cells.forEach(function(th, idx) {{
          var label = (th.textContent || '').trim().toUpperCase();
          if (headersToHide.indexOf(label) !== -1) {{
            anyHidden = true;
            var colIndex = idx + 1;  // nth-child index (1-based)

            // hide header cell
            th.style.display = 'none';

            // hide every row's cell in that column
            tbl.querySelectorAll('tbody tr').forEach(function(tr) {{
              var cell = tr.querySelector('th:nth-child(' + colIndex + '), td:nth-child(' + colIndex + ')');
              if (cell) {{
                cell.style.display = 'none';
              }}
            }});
          }}
        }});
      }});
        return anyHidden;

    }}

    function init() {{
      buildChart();
      hideOldHeader();
      hideReportColumns();

      var attempts = 0;
      var maxAttempts = 20;

            var timer = setInterval(function() {{
        attempts++;
        if (hideReportColumns() || attempts >= maxAttempts) {{
          clearInterval(timer);
        }}
      }}, 500);



    }}

    if (document.readyState === 'loading') {{
      document.addEventListener('DOMContentLoaded', init);
    }} else {{
      init();
    }}

  }})();
</script>

<!-- BRAC Digital Marketplace SUMMARY END -->
"""

    # ---- 4) Insert our block right after <body> (top of page) ----
    html = html.replace("<body>", "<body>\n" + summary_block, 1)

    latest.write_text(html, encoding="utf-8")

    # Auto open final html report
    _open_report(latest)

    tr = session.config.pluginmanager.get_plugin("terminalreporter")
    if tr:
        tr.write_line(f"Updated HTML report with BRAC Digital Marketplace summary + chart: {latest}")


# =========================

# OPTIONAL: Auto-open final HTML report after finishing

# =========================

def _open_report(path: Path):
    try:

        if os.name == "nt":

            os.startfile(path)  # Windows

        else:

            webbrowser.open_new_tab(path.as_uri())

    except Exception as e:

        print(f"⚠️ Could not auto-open report: {e}")
