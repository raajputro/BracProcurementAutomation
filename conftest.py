from sys import maxsize
import pyautogui
import pytest
from pathlib import Path
import shutil
import time
from datetime import datetime
from typing import Optional, Callable
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

# Configuration
ARTIFACTS_DIR = Path("artifacts")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
screen_width, screen_height = pyautogui.size()

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
            headless=False,
            slow_mo=200,
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
        # Listen for next page event
        with context.expect_page() as new_page_info:
            action(global_pages[-1])  # perform click/action on current page
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

                if global_pages:
                    page = global_pages[-1]
                    try:
                        if hasattr(page, "is_closed") and not page.is_closed():
                            page.screenshot(path=screenshot_path, full_page=True)
                    except Exception:
                        pass

        safe_file_operation(screenshot_path, screenshot_op)
