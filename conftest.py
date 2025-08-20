headless_flag = False
slow_mo_speed = 2000

from sys import maxsize
import os
import pyautogui
import pytest
from pathlib import Path
import shutil
import time
from datetime import datetime
from typing import Optional, Callable
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
    Locator,
)

# =========================
# Config
# =========================
ARTIFACTS_DIR = Path("artifacts")
print(f"Artifacts path: {ARTIFACTS_DIR}")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
screen_width, screen_height = pyautogui.size()

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

# Action-specific colors
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

# Globals
global_browser: Optional[Browser] = None
global_context: Optional[BrowserContext] = None
global_pages: list[Page] = []
test_failures = []

print(f"Running on screen size: {screen_width}x{screen_height}")

def pytest_configure(config):
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TRACES_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)

def safe_file_operation(file_path, operation, max_retries=5, delay=1):
    for attempt in range(max_retries):
        try:
            return operation(file_path)
        except (PermissionError, OSError):
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)

def wait_until_file_unlocked(path, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            with open(path, 'rb'):
                return True
        except PermissionError:
            time.sleep(0.5)
    raise TimeoutError(f"File {path} still locked after {timeout} seconds")

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
    global global_context, global_pages
    if global_context is None:
        global_context = browser.new_context(
            viewport={"width": screen_width, "height": screen_height},
            device_scale_factor=1,
            record_video_dir=VIDEOS_DIR,
            record_video_size={"width": screen_width, "height": screen_height},
            ignore_https_errors=True,
        )

        # Track all new pages/tabs automatically
        def on_page(page: Page):
            global_pages.append(page)
        global_context.on("page", on_page)

        # Start tracing
        global_context.tracing.start(screenshots=True, snapshots=True, sources=True)

        # Install patches
        if HIGHLIGHT_ENABLED:
            _install_auto_highlighter()

    yield global_context

    # Stop tracing and handle videos
    trace_suffix = (
        f"{test_failures[-1]['timestamp']}_{test_failures[-1]['name']}"
        if test_failures else datetime.now().strftime("%Y%m%d_%H%M%S_session")
    )
    trace_path = TRACES_DIR / f"{trace_suffix}_trace.zip"
    try:
        global_context.tracing.stop(path=trace_path)
    except Exception:
        pass

    # Handle videos for each page
    for fail in test_failures:
        test_name = fail["name"]
        timestamp = fail["timestamp"]
        for page in global_pages:
            if page.video:
                video_path = Path(page.video.path())
                new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"

                def rename_op(_):
                    wait_until_file_unlocked(video_path)
                    if video_path.exists():
                        video_path.rename(new_video_path)

                safe_file_operation(video_path, rename_op)

    global_context.close()
    global_context = None
    global_pages.clear()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Return the main page. Automatically track new tabs."""
    global global_pages
    if not global_pages:
        pg = context.new_page()
        global_pages.append(pg)
    return global_pages[0]  # main page by default

@pytest.fixture
def new_tab(context: BrowserContext) -> Callable[[Callable[[Page], None]], Page]:
    """
    Usage:
        new_page = new_tab(lambda page: page.click("a[target='_blank']"))
    Automatically waits for the new tab and returns it.
    """
    def _open(action: Callable[[Page], None]) -> Page:
        global global_pages
        with context.expect_page() as new_page_info:
            action(global_pages[-1])
        page = new_page_info.value
        global_pages.append(page)
        page.bring_to_front()
        return page
    return _open

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        test_name = item.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_failures.append({"name": test_name, "timestamp": timestamp})

        screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"

        def screenshot_op(_):
            if global_pages:
                page = global_pages[-1]
                try:
                    if hasattr(page, "is_closed") and not page.is_closed():
                        page.screenshot(path=screenshot_path, full_page=True)
                except Exception:
                    pass

        safe_file_operation(screenshot_path, screenshot_op)

# ==========================================
# Auto-highlighter implementation
# ==========================================
def highlight_selector(page: Page, selector: str, action: str, duration_ms: int = HIGHLIGHT_DURATION_MS):
    """Temporarily outline a selector in a color depending on the action."""
    try:
        color = ACTION_COLORS.get(action, "red")
        page.wait_for_selector(selector, state="attached", timeout=1500)
        page.eval_on_selector(
            selector,
            f"""(el) => {{
                const prev = el.style.outline;
                el.style.outline = '3px solid {color}';
                setTimeout(() => {{ el.style.outline = prev; }}, {duration_ms});
            }}"""
        )
    except Exception:
        pass

def highlight_locator(locator: Locator, action: str, duration_ms: int = HIGHLIGHT_DURATION_MS):
    """Temporarily outline the element behind a Locator."""
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

# === Soft Assertion Integration ===
# Logs pytest-check soft failures to console and reports
try:
    import pytest_check
except ImportError:
    pytest_check = None

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call":
        # Regular failures (already present)
        if rep.failed:
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_failures.append({"name": test_name, "timestamp": timestamp})

            screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"

            def screenshot_op(_):
                if global_pages:
                    page = global_pages[-1]
                    try:
                        if hasattr(page, "is_closed") and not page.is_closed():
                            page.screenshot(path=screenshot_path, full_page=True)
                    except Exception:
                        pass

            safe_file_operation(screenshot_path, screenshot_op)

        # Soft assertion errors from pytest-check (optional)
        if pytest_check:
            errors = getattr(pytest_check, "_errors", [])
            for e in errors:
                print(f"🔸 Soft check failure in {item.name}: {e}")