from sys import maxsize
import pyautogui
import pytest
from pathlib import Path
import shutil
import time
from datetime import datetime
from typing import Optional
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
global_page: Optional[Page] = None
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
            slow_mo=500
            #args=["--start-fullscreen"]
            #no_viewport=True
        )
    yield global_browser
    if global_browser:
        global_browser.close()
        global_browser = None


@pytest.fixture(scope="session")
def context(browser: Browser) -> BrowserContext:
    global global_context
    if global_context is None:
        global_context = browser.new_context(
            viewport={"width": screen_width, "height": screen_height},
            record_video_dir=VIDEOS_DIR,
            record_video_size={"width": screen_width, "height": screen_height}
        )
        global_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield global_context

    # Handle trace and video on test failures
    for fail in test_failures:
        test_name = fail["name"]
        timestamp = fail["timestamp"]
        trace_path = TRACES_DIR / f"{timestamp}_{test_name}_trace.zip"
        global_context.tracing.stop(path=trace_path)

        for page in global_context.pages:
            if page.video:
                video_path = Path(page.video.path())
                page.close()
                new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"

                def rename_op(_):
                    wait_until_file_unlocked(video_path)
                    video_path.rename(new_video_path)

                safe_file_operation(video_path, rename_op)

    # Clean up context
    global_context.close()
    global_context = None


@pytest.fixture(scope="session")
def page(context: BrowserContext) -> Page:
    global global_page
    if global_page is None:
        global_page = context.new_page()
    yield global_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Used to detect test failures and mark them for post-processing"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        test_name = item.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_failures.append({"name": test_name, "timestamp": timestamp})

        # Take screenshot for the failed test
        screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"

        def screenshot_op(_):
            global_page.screenshot(path=screenshot_path, full_page=True)

        safe_file_operation(screenshot_path, screenshot_op)
