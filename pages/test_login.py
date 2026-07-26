import json
from urllib.request import Request, build_opener, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler
from urllib.error import URLError, HTTPError
 
class ResetHubPage:
 
    def __init__(self, page):
        self.page = page
 
 
    def generate_reset_link(self, env: str, username: str):
 
        reset_url = (
            f"https://resethub.bracits.com/api/public/link?"
            f"env={env}&username={username}"
        )
 
        password_mgr = HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, reset_url, "linkbot", "7rnJYedY816TA9DjosPPFpyc363Ymk")
        auth_handler = HTTPBasicAuthHandler(password_mgr)
        opener = build_opener(auth_handler)
 
        request = Request(
            reset_url,
            headers={
                "Accept": "application/json"
            },
            method="GET"
        )
 
        try:
            with opener.open(request) as response:
                response_data = response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"ResetHub API request failed: {exc.code} {exc.reason}")
        except URLError as exc:
            raise RuntimeError(f"ResetHub API request failed: {exc.reason}")
 
        data = json.loads(response_data)
        generated_link = data["link"]
 
        print("Generated Link:")
        print(generated_link)
 
        return generated_link
 
 
    def open_generated_link(self, link):
 
        self.page.goto(link)
 
        self.page.wait_for_load_state("domcontentloaded")
        # popup = self.page.locator("#modals")
        # try:
        #     popup.wait_for(state="visible", timeout=60000)
        #     print("Popup appeared.")
        # except TimeoutError:
        #      print("Popup did not appear within 6 seconds.")

        print("Refreshing page...")
        self.page.wait_for_timeout(5000)  # Wait for 2 seconds before refreshing
        self.page.reload(wait_until="domcontentloaded")