# HashGuard

[![CI](https://github.com/RipLiquid/HashGuard/actions/workflows/ci.yml/badge.svg)](https://github.com/RipLiquid/HashGuard/actions/workflows/ci.yml)

HashGuard is a lightweight Python file integrity monitoring tool that uses SHA-256 cryptographic hashing to detect unexpected or unauthorized changes to files.

The application creates a trusted baseline of file hashes and compares future scans against that baseline to identify modified, newly created, deleted, and unchanged files.

## Features

* Generate SHA-256 hashes for files
* Recursively scan directories
* Create a trusted file integrity baseline
* Detect modified files
* Detect newly created files
* Detect deleted files
* Identify unchanged files
* Display scan summaries
* Handle missing baseline files
* Automated unit testing
* GitHub Actions continuous integration
* Test across multiple Python versions
* Uses only the Python Standard Library

## How It Works

HashGuard creates a SHA-256 hash for every file in the monitored directory.

A cryptographic hash acts as a digital fingerprint. Even a small change to a file produces a different SHA-256 hash.

```text
             Initial Scan
                  |
                  v
          Calculate SHA-256
                  |
                  v
          Save baseline.json
                  |
                  v
             Future Scan
                  |
                  v
          Calculate SHA-256
                  |
                  v
         Compare to Baseline
                  |
        +---------+---------+
        |         |         |
        v         v         v
   MODIFIED      NEW     DELETED
        |
        v
       OK
   (if unchanged)
```

## Detection States

| Status     | Description                                     |
| ---------- | ----------------------------------------------- |
| `OK`       | File exists and its hash has not changed        |
| `MODIFIED` | File exists but its SHA-256 hash has changed    |
| `NEW`      | File was not present in the saved baseline      |
| `DELETED`  | File existed in the baseline but is now missing |

## Example

After creating a baseline, files can be modified, added, or deleted.

A subsequent integrity scan may produce:

```text
=== INTEGRITY SCAN ===

[MODIFIED] config.txt
[NEW] newfile.txt
[OK] test.txt
[DELETED] notes.txt

=== SCAN SUMMARY ===
Unchanged: 1
Modified:  1
New:       1
Deleted:   1
```

## Project Structure

```text
HashGuard/
|
├── .github/
│   └── workflows/
│       └── ci.yml
|
├── src/
│   └── integrity_checker.py
|
├── tests/
│   └── test_integrity_checker.py
|
├── test_files/
│   └── sample.txt
|
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

* Python 3.11 or newer

HashGuard has no third-party dependencies and uses only modules included with the Python Standard Library.

## Usage

Clone the repository:

```bash
git clone https://github.com/RipLiquid/HashGuard.git
```

Navigate into the project:

```bash
cd HashGuard
```

Run HashGuard from the `src` directory:

```bash
cd src
python integrity_checker.py
```

The application displays:

```text
=== FILE INTEGRITY CHECKER ===
1. Create baseline
2. Check integrity
3. Exit
```

### Create a Baseline

Select:

```text
1
```

HashGuard scans the monitored directory and stores the SHA-256 hash of each file in `baseline.json`.

Example:

```text
Baseline created successfully.
Files recorded: 3
```

The generated `baseline.json` file represents the trusted state of the monitored files.

### Check File Integrity

Modify, create, or delete a file inside the monitored directory.

Run HashGuard again:

```bash
python integrity_checker.py
```

Select:

```text
2
```

HashGuard compares the current file hashes against the trusted baseline and reports any changes.

## Running Tests

HashGuard includes automated unit tests built with Python's `unittest` framework.

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

Expected output:

```text
test_calculate_hash ... ok
test_integrity_detection ... ok
test_save_and_load_baseline ... ok
test_scan_directory ... ok

----------------------------------------------------------------------
Ran 4 tests

OK
```

The test suite verifies:

* SHA-256 hash generation
* Directory scanning
* Baseline saving and loading
* Modified file detection
* New file detection
* Deleted file detection
* Unchanged file detection

## Continuous Integration

HashGuard uses GitHub Actions for automated continuous integration.

The CI workflow runs automatically when:

* Code is pushed to `main`
* A pull request targets `main`

Tests are executed on:

* Python 3.11
* Python 3.12
* Python 3.13

This ensures changes are automatically validated across multiple Python versions before being integrated into the project.

## Security Concepts Demonstrated

HashGuard demonstrates several foundational cybersecurity concepts:

* File integrity monitoring
* Cryptographic hashing
* SHA-256
* Trusted baselines
* Change detection
* Security monitoring
* Automated security testing
* Continuous integration

File integrity monitoring can help identify unauthorized configuration changes, malware activity, file tampering, and unexpected modifications to critical system files.

## Technologies

* Python
* SHA-256
* `hashlib`
* JSON
* Python `os`
* Python `unittest`
* Git
* GitHub
* GitHub Actions

## Author

Daniyal Tauseef
