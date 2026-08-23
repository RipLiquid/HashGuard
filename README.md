#  HashGuard (File Integrity Checker)

A lightweight Python cybersecurity tool that monitors files for unauthorized or unexpected changes using SHA-256 cryptographic hashing.

The program creates a trusted baseline of file hashes and compares future scans against that baseline to identify modified, newly created, or deleted files.

## Features

- Generate SHA-256 hashes for files
- Recursively scan directories
- Create a trusted file-integrity baseline
- Detect modified files
- Detect newly created files
- Detect deleted files
- Identify unchanged files
- Display a summary of scan results
- Handle missing baseline files
- Uses only the Python Standard Library

## How It Works

The File Integrity Checker generates a SHA-256 hash for every monitored file.

A hash acts like a digital fingerprint for a file.

If the file changes, its SHA-256 hash also changes.

The program stores the original hashes in a baseline and compares them against future scans.

```text
File
  |
  v
SHA-256 Hash
  |
  v
Baseline
  |
  v
Future Scan
  |
  v
Compare Hashes
  |
  +--> OK
  +--> MODIFIED
  +--> NEW
  +--> DELETED
