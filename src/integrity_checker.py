import hashlib
import json
import os


def calculate_hash(file_path):
    """Calculate and return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def scan_directory(directory):
    """Scan a directory and return file paths with their SHA-256 hashes."""
    file_hashes = {}

    for root, folders, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hashes[file_path] = calculate_hash(file_path)

    return file_hashes


def save_baseline(file_hashes, baseline_file):
    """Save file hashes to a JSON baseline file."""
    with open(baseline_file, "w") as file:
        json.dump(file_hashes, file, indent=4)


def load_baseline(baseline_file):
    """Load hashes from an existing baseline file."""
    with open(baseline_file, "r") as file:
        return json.load(file)


def display_name(file_path):
    """Return only the file name for cleaner output."""
    return os.path.basename(file_path)


def check_integrity(directory, baseline_file):
    """Compare current files against the saved baseline."""

    if not os.path.exists(baseline_file):
        print("\n[ERROR] No baseline found.")
        print("Create a baseline before checking integrity.")
        return

    baseline = load_baseline(baseline_file)
    current_files = scan_directory(directory)

    unchanged = 0
    modified = 0
    new = 0
    deleted = 0

    print("\n=== INTEGRITY SCAN ===\n")

    for file_path in current_files:
        if file_path not in baseline:
            print(f"[NEW] {display_name(file_path)}")
            new += 1

        elif current_files[file_path] != baseline[file_path]:
            print(f"[MODIFIED] {display_name(file_path)}")
            modified += 1

        else:
            print(f"[OK] {display_name(file_path)}")
            unchanged += 1

    for file_path in baseline:
        if file_path not in current_files:
            print(f"[DELETED] {display_name(file_path)}")
            deleted += 1

    print("\n=== SCAN SUMMARY ===")
    print(f"Unchanged: {unchanged}")
    print(f"Modified:  {modified}")
    print(f"New:       {new}")
    print(f"Deleted:   {deleted}")


def main():
    directory = "../test_files"
    baseline_file = "../baseline.json"

    print("\n=== FILE INTEGRITY CHECKER ===")
    print("1. Create baseline")
    print("2. Check integrity")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        results = scan_directory(directory)
        save_baseline(results, baseline_file)

        print("\nBaseline created successfully.")
        print(f"Files recorded: {len(results)}")

    elif choice == "2":
        check_integrity(directory, baseline_file)

    elif choice == "3":
        print("\nExiting File Integrity Checker.")

    else:
        print("\nInvalid option.")


if __name__ == "__main__":
    main()