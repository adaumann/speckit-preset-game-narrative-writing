"""
test_runtime.py — SugarCube runtime error detector for witchhunter.html
Uses Selenium + Chrome to walk through passages and capture SC error widgets.

Usage:
  pip install selenium webdriver-manager
  python test_runtime.py [--html path/to/witchhunter.html] [--headless]

Exit codes:
  0 — No runtime errors found
  1 — Runtime errors found (see stdout)
  2 — Setup / driver error
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional imports — give a clear message if not installed
# ---------------------------------------------------------------------------
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    sys.exit("Missing selenium. Run: pip install selenium")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    AUTO_DRIVER = True
except ImportError:
    AUTO_DRIVER = False  # Fall back to PATH chromedriver


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_HTML = Path(__file__).parent / "witchhunter.html"
PASSAGE_TIMEOUT = 5      # seconds to wait for a passage to render
ACTION_DELAY   = 0.4     # seconds between clicks
CLEAR_SESSION  = True    # clear localStorage + sessionStorage before each run


class SugarCubeTestRunner:
    """Walk a SugarCube story and collect runtime errors."""

    def __init__(self, html_path: Path, headless: bool = True):
        self.html_path = html_path.resolve()
        self.url = self.html_path.as_uri()
        self.errors: list[dict] = []
        self.visited: list[str] = []
        self.driver = self._make_driver(headless)

    # ------------------------------------------------------------------
    # Driver setup
    # ------------------------------------------------------------------
    def _make_driver(self, headless: bool):
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # Capture browser console logs
        opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        if AUTO_DRIVER:
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=opts)
        else:
            return webdriver.Chrome(options=opts)

    # ------------------------------------------------------------------
    # Page helpers
    # ------------------------------------------------------------------
    def load(self):
        self.driver.get(self.url)
        if CLEAR_SESSION:
            self.driver.execute_script("localStorage.clear(); sessionStorage.clear();")
            self.driver.refresh()
        self._wait_for_passage()

    def _wait_for_passage(self):
        """Wait until SugarCube has finished rendering a passage."""
        try:
            WebDriverWait(self.driver, PASSAGE_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#passages .passage"))
            )
        except TimeoutException:
            pass  # passage container might render differently
        time.sleep(0.3)

    def current_passage(self) -> str:
        try:
            return self.driver.execute_script(
                "return window.SugarCube && window.SugarCube.State.passage || '(unknown)';"
            )
        except Exception:
            return "(error reading passage)"

    def collect_sc_errors(self) -> list[str]:
        """Collect visible SugarCube error messages from .error-view elements."""
        try:
            els = self.driver.find_elements(By.CSS_SELECTOR, ".error-view")
            return [el.text.strip() for el in els if el.text.strip()]
        except Exception:
            return []

    def collect_console_errors(self) -> list[str]:
        """Collect browser console errors (Chrome only)."""
        try:
            logs = self.driver.get_log("browser")
            return [
                f"{l['level']}: {l['message']}"
                for l in logs
                if l["level"] in ("SEVERE", "WARNING") and "SugarCube" in l.get("message", "")
            ]
        except Exception:
            return []

    def record_errors(self, context: str):
        sc_errs  = self.collect_sc_errors()
        con_errs = self.collect_console_errors()
        passage  = self.current_passage()
        if sc_errs or con_errs:
            self.errors.append({
                "passage": passage,
                "context": context,
                "sc_errors": sc_errs,
                "console_errors": con_errs,
            })

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def click_link(self, text: str) -> bool:
        """Click the first visible link containing `text`. Returns True if found."""
        try:
            link = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@class,'macro-link') and contains(.,'{text}')]")
                )
            )
            link.click()
            time.sleep(ACTION_DELAY)
            self._wait_for_passage()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def click_first_link(self) -> bool:
        """Click the first available macro-link in the passage."""
        try:
            links = self.driver.find_elements(
                By.XPATH,
                "//div[@id='passages']//a[contains(@class,'macro-link') or @class='']"
            )
            visible = [l for l in links if l.is_displayed() and l.text.strip()]
            if visible:
                visible[0].click()
                time.sleep(ACTION_DELAY)
                self._wait_for_passage()
                return True
        except Exception:
            pass
        return False

    def navigate_to(self, passage_name: str) -> bool:
        """Navigate directly to a passage via SugarCube's Engine.play."""
        try:
            self.driver.execute_script(
                f"window.SugarCube.Engine.play('{passage_name}');"
            )
            time.sleep(ACTION_DELAY)
            self._wait_for_passage()
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Test scenarios
    # ------------------------------------------------------------------
    def test_initial_load(self):
        print(f"  [1] Initial load → passage: {self.current_passage()}")
        self.record_errors("initial_load")

    def test_tavern_quest_accept(self):
        """Click through: Head to inn → Agree with Mira → get confirmation."""
        self.navigate_to("LOC-DrunkGriffin")
        if self.click_link("Approach the woman"):
            self.record_errors("NODE-002_TavernMira")
            if self.click_link("Agree"):
                self.record_errors("NODE-002b_MiraJoins — after recruit")
                self.click_first_link()  # "Get some rest"
        print(f"  [2] Quest accept passage: {self.current_passage()}")

    def test_hub_navigation(self):
        """Visit both hub passages and check rendering."""
        for hub in ("LOC-Thorngate", "LOC-DrunkGriffin"):
            self.navigate_to(hub)
            self.record_errors(f"hub_{hub}")
            print(f"  [3] Hub {hub}: {len(self.collect_sc_errors())} errors")

    def test_goblin_combat(self):
        """Start goblin lair fight and do one round."""
        # First accept quest to unlock north road
        self.navigate_to("NODE-002_TavernMira")
        self.click_link("Agree")
        time.sleep(0.3)

        # Go to lair
        self.navigate_to("NODE-003_GoblinAmbush")
        self.record_errors("NODE-003_GoblinAmbush")

        if self.click_link("Fight"):
            self.record_errors("CombatUI — initial")
            print(f"  [4] Combat opened: {self.current_passage()}")

            # Attack
            try:
                attack_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(.,'Attack')]")
                    )
                )
                attack_btn.click()
                time.sleep(ACTION_DELAY)
                self.record_errors("CombatUI — after attack")
                print(f"  [4] After attack: {self.current_passage()}")
            except TimeoutException:
                print("  [4] Attack button not found")

    def test_character_sheet(self):
        self.navigate_to("CharacterSheet")
        self.record_errors("CharacterSheet")
        print(f"  [5] CharacterSheet: {len(self.collect_sc_errors())} errors")

    def test_quest_journal(self):
        self.navigate_to("QuestJournal")
        self.record_errors("QuestJournal")
        print(f"  [6] QuestJournal: {len(self.collect_sc_errors())} errors")

    def test_inventory_ui(self):
        self.navigate_to("InventoryUI")
        self.record_errors("InventoryUI")
        print(f"  [7] InventoryUI: {len(self.collect_sc_errors())} errors")

    def test_world_map(self):
        self.navigate_to("WorldMap")
        self.record_errors("WorldMap")
        print(f"  [8] WorldMap: {len(self.collect_sc_errors())} errors")

    def test_craft_ui(self):
        self.driver.execute_script(
            "window.SugarCube.State.variables.craft_active_station = 'alchemy_bench';"
        )
        self.navigate_to("CraftUI")
        self.record_errors("CraftUI")
        print(f"  [9] CraftUI: {len(self.collect_sc_errors())} errors")

    def test_rest_ui(self):
        self.driver.execute_script(
            "window.SugarCube.State.variables.rest_return_passage = 'LOC-DrunkGriffin';"
        )
        self.navigate_to("RestUI")
        self.record_errors("RestUI")
        print(f"  [10] RestUI: {len(self.collect_sc_errors())} errors")

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------
    def run(self) -> int:
        print(f"\nLoading: {self.url}\n")
        try:
            self.load()
            print("Running test scenarios:")
            self.test_initial_load()
            self.test_hub_navigation()
            self.test_tavern_quest_accept()
            self.test_goblin_combat()
            self.test_character_sheet()
            self.test_quest_journal()
            self.test_inventory_ui()
            self.test_world_map()
            self.test_craft_ui()
            self.test_rest_ui()
        finally:
            self.driver.quit()

        print("\n" + "=" * 60)
        if self.errors:
            print(f"FAILED — {len(self.errors)} passages with errors:\n")
            for e in self.errors:
                print(f"  Passage : {e['passage']}")
                print(f"  Context : {e['context']}")
                for msg in e["sc_errors"]:
                    print(f"  SC error: {msg[:200]}")
                for msg in e["console_errors"]:
                    print(f"  Console : {msg[:200]}")
                print()
            return 1
        else:
            print("PASSED — No runtime errors detected.")
            return 0

    def close(self):
        try:
            self.driver.quit()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SugarCube runtime error detector")
    parser.add_argument(
        "--html",
        default=str(DEFAULT_HTML),
        help="Path to the compiled .html file"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode"
    )
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        sys.exit(f"Error: file not found: {html_path}")

    runner = SugarCubeTestRunner(html_path, headless=args.headless)
    try:
        exit_code = runner.run()
    except Exception as exc:
        print(f"Setup error: {exc}", file=sys.stderr)
        runner.close()
        sys.exit(2)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
