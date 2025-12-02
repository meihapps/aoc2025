import importlib.util
import os
import sys
from pathlib import Path


class AOCMenu:
    def __init__(self, project_root: Path | None = None):
        self.root: Path = project_root or Path(__file__).parent
        self.year: str | None = None
        self.day: str | None = None
        self.part: str | None = None

    def discover_years(self) -> list[str]:
        years: list[str] = []
        for item in self.root.iterdir():
            if item.is_dir() and item.name.startswith("year_"):
                year = item.name.replace("year_", "")
                years.append(year)
        return sorted(years)

    def discover_days(self, year: str) -> list[str]:
        days: list[str] = []
        year_path = self.root / f"year_{year}"
        if not year_path.exists():
            return []

        for item in year_path.iterdir():
            if item.is_dir() and item.name.startswith("day_"):
                day = item.name.replace("day_", "")
                days.append(day)
        return sorted(days)

    def get_available_parts(self, year: str, day: str) -> list[str]:
        solution_path = self.root / f"year_{year}" / f"day_{day}" / "solution.py"
        if not solution_path.exists():
            return []

        # Load the module to check for part functions
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        module = importlib.util.module_from_spec(spec)  # pyright: ignore[reportArgumentType]

        try:
            spec.loader.exec_module(module)  # pyright: ignore[reportOptionalMemberAccess]
            parts: list[str] = []
            if hasattr(module, "part_1"):
                parts.append("1")
            if hasattr(module, "part_2"):
                parts.append("2")
            return parts
        except Exception:
            return []

    def run_solution(self, year: str, day: str, part: str):
        solution_path = self.root / f"year_{year}" / f"day_{day}" / "solution.py"

        # Change to the solution directory to handle relative file paths
        original_cwd = os.getcwd()
        os.chdir(solution_path.parent)

        try:
            spec = importlib.util.spec_from_file_location("solution", solution_path)
            module = importlib.util.module_from_spec(spec)  # pyright: ignore[reportArgumentType]
            spec.loader.exec_module(module)  # pyright: ignore[reportOptionalMemberAccess]

            func_name = f"part_{part}"
            if hasattr(module, func_name):
                func = getattr(module, func_name)  # pyright: ignore[reportAny]
                return func()  # pyright: ignore[reportAny]
            else:
                return f"Function {func_name} not found"
        except Exception as e:
            return f"Error executing solution: {e}"
        finally:
            os.chdir(original_cwd)

    def display_available_options(self, title: str, options: list[str]) -> None:
        print(f"\n{'=' * 40}")
        print(f"{title:^40}")
        print(f"{'=' * 40}")
        print(f"Available: {', '.join(options)}")

    def get_direct_input(
        self, prompt: str, valid_options: list[str], allow_back: bool = False
    ) -> str:
        while True:
            # Build prompt
            full_prompt = f"\n{prompt}"
            if allow_back:
                full_prompt += " (or 'back' to go back, 'exit' to quit): "
            else:
                full_prompt += " (or 'exit' to quit): "

            choice = input(full_prompt).strip().lower()

            if choice == "exit":
                sys.exit(0)

            if allow_back and choice == "back":
                return "back"

            # Check direct match first
            if choice in valid_options:
                return choice

            # Try zero-padded match for days
            padded_choice = choice.zfill(2)
            if padded_choice in valid_options:
                return padded_choice

            print(f"Invalid choice. Available options: {', '.join(valid_options)}")

    def year_menu(self) -> None:
        years = self.discover_years()

        if not years:
            print("No years found in the project directory.")
            sys.exit(0)

        self.display_available_options("Select Year", years)
        choice = self.get_direct_input("Enter year", years)

        self.year = choice
        self.day_menu()

    def day_menu(self) -> None:
        days = self.discover_days(self.year)  # pyright: ignore[reportArgumentType]

        if not days:
            print(f"No days found for year {self.year}.")
            return

        self.display_available_options(f"Year {self.year} - Select Day", days)
        choice = self.get_direct_input("Enter day", days, allow_back=True)

        if choice == "back":
            self.year = None
            return

        self.day = choice
        self.part_menu()

    def part_menu(self) -> None:
        parts = self.get_available_parts(self.year, self.day)  # pyright: ignore[reportArgumentType]

        if not parts:
            print(f"No solution parts found for year {self.year}, day {self.day}.")
            return

        self.display_available_options(
            f"Year {self.year}, Day {self.day} - Select Part", parts
        )
        choice = self.get_direct_input("Enter part", parts, allow_back=True)

        if choice == "back":
            self.day = None
            return

        self.execute_solution(choice)

    def execute_solution(self, part: str) -> None:
        print(f"\nExecuting Year {self.year}, Day {self.day}, Part {part}...")
        print("-" * 40)

        result = self.run_solution(self.year, self.day, part)  # pyright: ignore[reportArgumentType]
        print(f"Result: {result}")

        _ = input("\nPress Enter to continue...")

    def run(self) -> None:
        print("Welcome to Advent of Code Solution Runner!")

        while True:
            if not self.year:
                self.year_menu()
            elif not self.day:
                self.day_menu()
            else:
                self.part_menu()


def test_menu():
    menu = AOCMenu()

    # Test year discovery
    years = menu.discover_years()
    print(f"Available years: {years}")

    if not years:
        return

    # Test day discovery
    test_year = years[0]
    days = menu.discover_days(test_year)
    print(f"Available days for {test_year}: {days}")

    if not days:
        return

    # Test part discovery
    test_day = days[0]
    parts = menu.get_available_parts(test_year, test_day)
    print(f"Available parts for {test_year} day {test_day}: {parts}")

    if not parts:
        return

    # Test solution execution for all available parts
    for test_part in parts:
        print(
            f"\nTesting execution of year {test_year}, day {test_day}, part {test_part}:"
        )
        result = menu.run_solution(test_year, test_day, test_part)
        print(f"Result: {result}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_menu()
    else:
        menu = AOCMenu()
        menu.run()


if __name__ == "__main__":
    main()
