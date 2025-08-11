# # from sys import maxsize
# # import pyautogui
# # import pytest
# # from pathlib import Path
# # import shutil
# # import time
# # from datetime import datetime
# # from typing import Optional
# # from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
# #
# # # Configuration
# # ARTIFACTS_DIR = Path("artifacts")
# # VIDEOS_DIR = ARTIFACTS_DIR / "videos"
# # TRACES_DIR = ARTIFACTS_DIR / "traces"
# # SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
# # screen_width, screen_height = pyautogui.size()
# #
# # # Globals
# # global_browser: Optional[Browser] = None
# # global_context: Optional[BrowserContext] = None
# # global_page: Optional[Page] = None
# # test_failures = []
# #
# # print(f"Running on screen size: {screen_width}x{screen_height}")
# #
# #
# # def pytest_configure(config):
# #     if ARTIFACTS_DIR.exists():
# #         shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)
# #     VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
# #     TRACES_DIR.mkdir(exist_ok=True)
# #     SCREENSHOTS_DIR.mkdir(exist_ok=True)
# #
# #
# # def safe_file_operation(file_path, operation, max_retries=5, delay=1):
# #     for attempt in range(max_retries):
# #         try:
# #             return operation(file_path)
# #         except (PermissionError, OSError):
# #             if attempt == max_retries - 1:
# #                 raise
# #             time.sleep(delay)
# #
# #
# # def wait_until_file_unlocked(path, timeout=10):
# #     end_time = time.time() + timeout
# #     while time.time() < end_time:
# #         try:
# #             with open(path, 'rb'):
# #                 return True
# #         except PermissionError:
# #             time.sleep(0.5)
# #     raise TimeoutError(f"File {path} still locked after {timeout} seconds")
# #
# #
# # @pytest.fixture(scope="session")
# # def playwright() -> Playwright:
# #     with sync_playwright() as p:
# #         yield p
# #
# #
# # @pytest.fixture(scope="session")
# # def browser(playwright: Playwright) -> Browser:
# #     """Launch Chromium with a MAXIMIZED OS window (not just a large viewport)."""
# #     global global_browser
# #     if global_browser is None:
# #         global_browser = playwright.chromium.launch(
# #             headless=False,
# #             slow_mo=200,
# #             args=[
# #                 "--start-maximized",  # open the OS window maximized
# #                 "--window-position=0,0",  # ensure it starts on the primary display
# #             ],
# #         )
# #     yield global_browser
# #     if global_browser:
# #         global_browser.close()
# #         global_browser = None
# #
# #
# # @pytest.fixture(scope="session")
# # def context(browser: Browser) -> BrowserContext:
# #     """
# #     Use the real window size (viewport=None) so the page matches the maximized window.
# #     Also record videos at the screen resolution to capture full content.
# #     """
# #     global global_context
# #     if global_context is None:
# #         global_context = browser.new_context(
# #             viewport=None,  # disable fixed viewport emulation; use real window size
# #             record_video_dir=VIDEOS_DIR,
# #             record_video_size={"width": screen_width, "height": screen_height},
# #         )
# #         # Start tracing once; we'll stop on teardown after collecting failures
# #         global_context.tracing.start(screenshots=True, snapshots=True, sources=True)
# #     yield global_context
# #
# #     # Handle trace and video on test failures
# #     # NOTE: tracing.stop() can only be called once per context. If there were failures,
# #     # export a single trace zip tagged with the last failure (or "session").
# #     trace_suffix = (
# #         f"{test_failures[-1]['timestamp']}_{test_failures[-1]['name']}"
# #         if test_failures else datetime.now().strftime("%Y%m%d_%H%M%S_session")
# #     )
# #     trace_path = TRACES_DIR / f"{trace_suffix}_trace.zip"
# #     try:
# #         global_context.tracing.stop(path=trace_path)
# #     except Exception:
# #         # Ignore if already stopped or not started
# #         pass
# #
# #     # Move/rename page videos for each failure (if any)
# #     for fail in test_failures:
# #         test_name = fail["name"]
# #         timestamp = fail["timestamp"]
# #         for page in list(global_context.pages):
# #             if page.video:
# #                 video_path = Path(page.video.path())
# #                 new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"
# #
# #                 def rename_op(_):
# #                     wait_until_file_unlocked(video_path)
# #                     if video_path.exists():
# #                         video_path.rename(new_video_path)
# #
# #                 safe_file_operation(video_path, rename_op)
# #
# #     # Clean up context
# #     global_context.close()
# #     global_context = None
# #
# #
# # @pytest.fixture(scope="session")
# # def page(context: BrowserContext) -> Page:
# #     global global_page
# #     if global_page is None:
# #         global_page = context.new_page()
# #         try:
# #             # Ensure window is front-most
# #             global_page.bring_to_front()
# #
# #             # Hard-maximize the OS window via Chrome DevTools Protocol (Chromium only)
# #             try:
# #                 cdp = context.new_cdp_session(global_page)
# #                 win = cdp.send("Browser.getWindowForTarget")
# #                 if win and "windowId" in win:
# #                     cdp.send("Browser.setWindowBounds", {
# #                         "windowId": win["windowId"],
# #                         "bounds": {"windowState": "maximized"}
# #                     })
# #             except Exception:
# #                 # Fallback: set explicit window size to screen resolution
# #                 try:
# #                     global_page.context.close()
# #                 except Exception:
# #                     pass
# #                 # Recreate context with explicit window size equal to screen
# #                 new_ctx = global_browser.new_context(
# #                     viewport=None,
# #                     record_video_dir=VIDEOS_DIR,
# #                     record_video_size={"width": screen_width, "height": screen_height},
# #                     screen={"width": screen_width, "height": screen_height}
# #                 )
# #                 global_page = new_ctx.new_page()
# #                 global_page.bring_to_front()
# #         except Exception:
# #             pass
# #     yield global_page
# #
# #
# # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     """Detect test failures and mark them for post-processing."""
# #     outcome = yield
# #     rep = outcome.get_result()
# #     setattr(item, "rep_" + rep.when, rep)
# #
# #     if rep.when == "call" and rep.failed:
# #         test_name = item.name
# #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# #         test_failures.append({"name": test_name, "timestamp": timestamp})
# #
# #         # Take screenshot for the failed test
# #         screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"
# #
# #         def screenshot_op(_):
# #             global_page.screenshot(path=screenshot_path, full_page=True)
# #
# #         safe_file_operation(screenshot_path, screenshot_op)
# from sys import maxsize
# import pyautogui
# import pytest
# from pathlib import Path
# import shutil
# import time
# from datetime import datetime
# from typing import Optional
# from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
#
# # Configuration
# ARTIFACTS_DIR = Path("artifacts")
# VIDEOS_DIR = ARTIFACTS_DIR / "videos"
# TRACES_DIR = ARTIFACTS_DIR / "traces"
# SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
# screen_width, screen_height = pyautogui.size()
#
# # Globals
# global_browser: Optional[Browser] = None
# global_context: Optional[BrowserContext] = None
# global_page: Optional[Page] = None
# test_failures = []
#
# print(f"Running on screen size: {screen_width}x{screen_height}")
#
#
# def pytest_configure(config):
#     if ARTIFACTS_DIR.exists():
#         shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)
#     VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
#     TRACES_DIR.mkdir(exist_ok=True)
#     SCREENSHOTS_DIR.mkdir(exist_ok=True)
#
#
# def safe_file_operation(file_path, operation, max_retries=5, delay=1):
#     for attempt in range(max_retries):
#         try:
#             return operation(file_path)
#         except (PermissionError, OSError):
#             if attempt == max_retries - 1:
#                 raise
#             time.sleep(delay)
#
#
# def wait_until_file_unlocked(path, timeout=10):
#     end_time = time.time() + timeout
#     while time.time() < end_time:
#         try:
#             with open(path, 'rb'):
#                 return True
#         except PermissionError:
#             time.sleep(0.5)
#     raise TimeoutError(f"File {path} still locked after {timeout} seconds")
#
#
# @pytest.fixture(scope="session")
# def playwright() -> Playwright:
#     with sync_playwright() as p:
#         yield p
#
#
# @pytest.fixture(scope="session")
# def browser(playwright: Playwright) -> Browser:
#     """Launch Chromium with a MAXIMIZED OS window and DPI-stable flags."""
#     global global_browser
#     if global_browser is None:
#         global_browser = playwright.chromium.launch(
#             headless=False,
#             slow_mo=200,
#             args=[
#                 "--start-maximized",            # open the OS window maximized
#                 "--window-position=0,0",        # ensure it starts on the primary display
#                 "--high-dpi-support=1",         # better scaling on Windows
#                 "--force-device-scale-factor=1" # avoid 125%/150% OS scaling issues
#             ],
#         )
#     yield global_browser
#     if global_browser:
#         global_browser.close()
#         global_browser = None
#
#
# @pytest.fixture(scope="session")
# def context(browser: Browser) -> BrowserContext:
#     """
#     Use an explicit viewport that matches the (maximized) window to avoid DPI scaling quirks,
#     and record video at the same resolution.
#     """
#     global global_context
#     if global_context is None:
#         global_context = browser.new_context(
#             viewport={"width": screen_width, "height": screen_height},
#             device_scale_factor=1,
#             record_video_dir=VIDEOS_DIR,
#             record_video_size={"width": screen_width, "height": screen_height},
#         )
#         # Start tracing once; we'll stop on teardown after collecting failures
#         global_context.tracing.start(screenshots=True, snapshots=True, sources=True)
#     yield global_context
#
#     # Handle trace and video on test failures
#     trace_suffix = (
#         f"{test_failures[-1]['timestamp']}_{test_failures[-1]['name']}"
#         if test_failures else datetime.now().strftime("%Y%m%d_%H%M%S_session")
#     )
#     trace_path = TRACES_DIR / f"{trace_suffix}_trace.zip"
#     try:
#         global_context.tracing.stop(path=trace_path)
#     except Exception:
#         pass
#
#     # Move/rename page videos for each failure (if any)
#     for fail in test_failures:
#         test_name = fail["name"]
#         timestamp = fail["timestamp"]
#         for page in list(global_context.pages):
#             if page.video:
#                 video_path = Path(page.video.path())
#                 new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"
#
#                 def rename_op(_):
#                     wait_until_file_unlocked(video_path)
#                     if video_path.exists():
#                         video_path.rename(new_video_path)
#
#                 safe_file_operation(video_path, rename_op)
#
#     # Clean up context
#     global_context.close()
#     global_context = None
#
#
# @pytest.fixture(scope="session")
# def page(context: BrowserContext) -> Page:
#     global global_page
#     if global_page is None:
#         global_page = context.new_page()
#         try:
#             # Ensure window is front-most
#             global_page.bring_to_front()
#
#             # Hard-maximize the OS window via CDP (Chromium-only)
#             try:
#                 cdp = context.new_cdp_session(global_page)
#                 win = cdp.send("Browser.getWindowForTarget")
#                 if win and "windowId" in win:
#                     cdp.send("Browser.setWindowBounds", {
#                         "windowId": win["windowId"],
#                         "bounds": {"windowState": "maximized"}
#                     })
#             except Exception:
#                 pass
#
#             # Final sync: make the emulated viewport exactly match current inner size
#             try:
#                 inner = global_page.evaluate("({ w: window.innerWidth, h: window.innerHeight })")
#                 if inner and inner.get("w") and inner.get("h"):
#                     global_page.set_viewport_size({"width": int(inner["w"]), "height": int(inner["h"])})
#             except Exception:
#                 pass
#         except Exception:
#             pass
#     return global_page
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Detect test failures and mark them for post-processing."""
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#
#     if rep.when == "call" and rep.failed:
#         test_name = item.name
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         test_failures.append({"name": test_name, "timestamp": timestamp})
#
#         # Take screenshot for the failed test
#         screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"
#
#         def screenshot_op(_):
#             global_page.screenshot(path=screenshot_path, full_page=True)
#
#         safe_file_operation(screenshot_path, screenshot_op)
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
    """Launch Chromium with a MAXIMIZED OS window and DPI-stable flags."""
    global global_browser
    if global_browser is None:
        global_browser = playwright.chromium.launch(
            headless=False,
            slow_mo=200,
            args=[
                "--start-maximized",            # open the OS window maximized
                "--window-position=0,0",        # ensure it starts on the primary display
                "--high-dpi-support=1",         # better scaling on Windows
                "--force-device-scale-factor=1" # avoid 125%/150% OS scaling issues
            ],
        )
    yield global_browser
    if global_browser:
        global_browser.close()
        global_browser = None


@pytest.fixture(scope="session")
def context(browser: Browser) -> BrowserContext:
    """
    Use an explicit viewport that matches the (maximized) window to avoid DPI scaling quirks,
    and record video at the same resolution.
    """
    global global_context
    if global_context is None:
        global_context = browser.new_context(
            viewport={"width": screen_width, "height": screen_height},
            device_scale_factor=1,
            record_video_dir=VIDEOS_DIR,
            record_video_size={"width": screen_width, "height": screen_height},
        )
        # Start tracing once; we'll stop on teardown after collecting failures
        global_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield global_context

    # Handle trace and video on test failures
    trace_suffix = (
        f"{test_failures[-1]['timestamp']}_{test_failures[-1]['name']}"
        if test_failures else datetime.now().strftime("%Y%m%d_%H%M%S_session")
    )
    trace_path = TRACES_DIR / f"{trace_suffix}_trace.zip"
    try:
        global_context.tracing.stop(path=trace_path)
    except Exception:
        pass

    # Move/rename page videos for each failure (if any)
    for fail in test_failures:
        test_name = fail["name"]
        timestamp = fail["timestamp"]
        for page in list(global_context.pages):
            if page.video:
                video_path = Path(page.video.path())
                new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"

                def rename_op(_):
                    wait_until_file_unlocked(video_path)
                    if video_path.exists():
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
        global_page.set_default_navigation_timeout(60000)
        try:
            # Ensure window is front-most
            global_page.bring_to_front()

            # Hard-maximize the OS window via CDP (Chromium-only)
            try:
                cdp = context.new_cdp_session(global_page)
                win = cdp.send("Browser.getWindowForTarget")
                if win and "windowId" in win:
                    cdp.send("Browser.setWindowBounds", {
                        "windowId": win["windowId"],
                        "bounds": {"windowState": "maximized"}
                    })
            except Exception:
                pass

            # Final sync: make the emulated viewport exactly match current inner size
            try:
                inner = global_page.evaluate("({ w: window.innerWidth, h: window.innerHeight })")
                if inner and inner.get("w") and inner.get("h"):
                    global_page.set_viewport_size({"width": int(inner["w"]), "height": int(inner["h"])})
            except Exception:
                pass
        except Exception:
            pass
    return global_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Detect test failures and mark them for post-processing."""
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
