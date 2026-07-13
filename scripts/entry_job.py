from concurrent.futures import ThreadPoolExecutor
from src.database.queries import db_call, get_active_entries
from src.utils.start_entry import start_entry

def main():
    entries = db_call(get_active_entries).get("data")
    
    with ThreadPoolExecutor(max_workers=len(entries)) as executor:
        executor.map(
            lambda entry: start_entry(entry["id"]),
            entries
        )


if __name__ == "__main__":
    main()