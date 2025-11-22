# Sovereignty Architecture Utilities

This document describes the utility tools available in the Sovereignty Architecture system.

## Zip File Analyzer (`analyze_zip.py`)

A comprehensive utility for analyzing zip file contents, extracting metadata, and validating archive integrity.

### Features

- 📊 **Comprehensive Analysis**: Analyzes file counts, sizes, compression ratios
- 🔍 **Detailed Reports**: Per-file metadata including CRC checksums
- 🔐 **Integrity Checks**: Validates archive integrity with built-in testing
- 📝 **Multiple Formats**: Output in text or JSON format
- 💾 **File Export**: Save analysis results to file
- 🛡️ **Security**: SHA256 hash calculation for file verification

### Usage

#### Basic Analysis

```bash
./analyze_zip.py files.zip
```

This will display a summary report including:
- File information (name, path, size, SHA256 hash)
- Archive contents (file/directory counts, compression stats)
- File type distribution
- Integrity check results

#### Detailed Analysis

```bash
./analyze_zip.py -d files.zip
```

Includes all basic information plus:
- Per-file metadata (sizes, compression ratios, timestamps)
- CRC32 checksums
- Individual file modification dates

#### JSON Output

```bash
./analyze_zip.py -f json files.zip > analysis.json
```

Outputs structured JSON data suitable for:
- Automated processing
- Integration with other tools
- API responses
- Database storage

#### Save to File

```bash
./analyze_zip.py -o report.txt files.zip
./analyze_zip.py -f json -o report.json files.zip
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `zip_file` | Path to the zip file to analyze (required) |
| `-d, --detailed` | Include detailed per-file analysis |
| `-f, --format {text,json}` | Output format (default: text) |
| `-o, --output OUTPUT` | Save analysis to file instead of stdout |
| `-h, --help` | Show help message and exit |

### Examples

#### Analyze and Save Report

```bash
# Analyze a deployment package
./analyze_zip.py deployment.zip -o deployment_report.txt

# Generate JSON for automation
./analyze_zip.py -f json -d package.zip > package_analysis.json
```

#### Integration with CI/CD

```bash
# Validate archive in CI pipeline
if ./analyze_zip.py release.zip -f json | jq -e '.archive_info.integrity_check == "PASSED"'; then
    echo "Archive validation passed"
else
    echo "Archive validation failed"
    exit 1
fi
```

#### Security Verification

```bash
# Extract and verify SHA256 hash
HASH=$(./analyze_zip.py -f json files.zip | jq -r '.file_info.hash_sha256')
echo "Archive SHA256: $HASH"
```

### Output Format

#### Text Format Example

```
======================================================================
📦 ZIP FILE ANALYSIS REPORT
======================================================================

🕒 Analysis Time: 2025-11-22T23:00:00.000000

📄 File Information:
   Name: example.zip
   Path: /path/to/example.zip
   Size: 1.23 MB
   SHA256: abc123...

📊 Archive Contents:
   Total Entries: 42
   Files: 38
   Directories: 4
   Compressed Size: 1.15 MB
   Uncompressed Size: 3.45 MB
   Compression Ratio: 66.67%
   Integrity Check: PASSED

📑 File Types Distribution:
   .txt: 15 file(s)
   .py: 10 file(s)
   .json: 8 file(s)
   .md: 5 file(s)
```

#### JSON Format Structure

```json
{
  "status": "success",
  "timestamp": "2025-11-22T23:00:00.000000",
  "file_info": {
    "path": "/path/to/example.zip",
    "name": "example.zip",
    "size": 1234567,
    "size_formatted": "1.23 MB",
    "hash_sha256": "abc123..."
  },
  "archive_info": {
    "total_files": 42,
    "total_directories": 4,
    "file_count": 38,
    "total_compressed_size": 1150000,
    "total_compressed_size_formatted": "1.15 MB",
    "total_uncompressed_size": 3450000,
    "total_uncompressed_size_formatted": "3.45 MB",
    "compression_ratio": 66.67,
    "integrity_check": "PASSED",
    "file_types": {
      ".txt": 15,
      ".py": 10,
      ".json": 8,
      ".md": 5
    }
  }
}
```

### Error Handling

The tool provides clear error messages for common issues:

- **File not found**: Returns error status with message
- **Invalid zip file**: Detects and reports non-zip files
- **Corrupted archives**: Reports integrity check failures

All errors include:
- Error status indicator
- Descriptive error message
- Timestamp of the analysis attempt

### Exit Codes

- `0`: Success - analysis completed without errors
- `1`: Error - file not found, invalid zip, or analysis failed

### Integration with Sovereignty Architecture

This tool integrates with the Sovereignty Architecture system:

- **Audit Logging**: Analysis results can be logged for compliance
- **Deployment Validation**: Verify deployment packages before rollout
- **Security Scanning**: Generate hashes for artifact verification
- **CI/CD Pipelines**: Automated package validation
- **Documentation**: Generate reports for release notes

### Security Considerations

- **Hash Verification**: SHA256 hashes for file integrity verification
- **Integrity Checks**: Built-in CRC and zip integrity validation
- **Safe Analysis**: Read-only operation, no file extraction
- **No Code Execution**: Pure analysis, no embedded code execution

### Dependencies

The tool uses only Python standard library modules:
- `zipfile`: Zip archive handling
- `hashlib`: Hash calculation
- `json`: JSON output formatting
- `pathlib`: Path handling
- Standard library utilities

No external dependencies required.

## Additional Utilities

### Benchmark Runner (`scripts/run_benchmarks.py`)

Enterprise-grade benchmark execution with UPL-safe automation.

### Sleep Mode Configuration (`scripts/configure_sleep_mode.py`)

System sleep mode configuration for power management.

### GitLens Integration (`scripts/gl2discord.sh`)

Discord notification integration for GitLens events.

---

**Strategickhaos DAO LLC** - UPL-Safe Automation
