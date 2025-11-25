# LyraNode Manifest Schema & Tools

This directory contains the schema definitions, validation tools, and examples for LyraNode manifests used in the Sovereignty Architecture.

## Contents

| File | Description |
|------|-------------|
| `lyra-node-manifest.schema.json` | JSON Schema for manifest validation |
| `lyranode-crd.yaml` | Kubernetes Custom Resource Definition |
| `lyranode-example.yaml` | Example Kubernetes LyraNode resource |
| `lyra_node_manifest_example.yaml` | Example plain YAML manifest (validates against schema) |
| `lyra_node_manifest_public.yaml` | Sanitized/public-safe manifest example |
| `manifest_validator.py` | Python tool for validation and signing |
| `requirements-schemas.txt` | Python dependencies |
| `README.md` | This documentation |

## Quick Start

### Install Dependencies

```bash
pip install -r schemas/requirements-schemas.txt
```

### Validate a Manifest

```bash
python schemas/manifest_validator.py validate your-manifest.yaml
```

### Sign a Manifest (GPG)

```bash
python schemas/manifest_validator.py sign your-manifest.yaml --key-id 0xYOURKEY
```

### Verify Signature

```bash
python schemas/manifest_validator.py verify your-manifest.yaml
```

### Sanitize for Public Release

```bash
python schemas/manifest_validator.py sanitize your-manifest.yaml --output public.yaml
```

### Compute Checksums

```bash
python schemas/manifest_validator.py checksum your-manifest.yaml
```

## JSON Schema (Option A)

The `lyra-node-manifest.schema.json` provides:

- **Typed Fields**: UUIDs, semantic versions, enums for statuses
- **Pattern Validation**: URN format for node IDs, hex patterns for checksums
- **Provenance & Signature**: Blocks for cryptographic integrity
- **Sensitivity Classification**: Tags for handling sensitive data
- **Machine-Actionable**: Canonical IDs and artifact URIs

Example validated structure:

```yaml
node:
  id: urn:lyra:node:NitroV15-Lyra:15
  version: "15.2.0"
  status: active   # enum: active|inactive|retired|maintenance|degraded
```

## Kubernetes CRD (Option B)

The `lyranode-crd.yaml` provides:

- **apiVersion**: `lyra.io/v1alpha1`
- **kind**: `LyraNode`
- **Proper spec/status separation**
- **OpenAPI v3 validation**
- **Printer columns** for `kubectl get lyranodes`

Deploy the CRD:

```bash
kubectl apply -f schemas/lyranode-crd.yaml
```

Create a LyraNode:

```bash
kubectl apply -f schemas/lyranode-example.yaml
```

Query LyraNodes:

```bash
kubectl get lyranodes -n sovereignty
kubectl describe lyranode nitrov15-lyra -n sovereignty
```

## Sanitized Manifest (Option C)

The `lyra_node_manifest_public.yaml` demonstrates:

- **Redacted PII**: Operator names replaced with `[REDACTED]`
- **Tokenized Secrets**: Key IDs become `[KEY_REF:*]`
- **Removed Vault Paths**: No internal paths exposed
- **Verification Tokens**: Checksums replaced with `verify://` URIs
- **Classification Metadata**: Preserved for transparency

## Python Validator (Option D)

The `manifest_validator.py` provides:

### Features

- **Schema Validation**: Against JSON Schema Draft 7
- **GPG Signing**: Detached signatures
- **Signature Verification**: Verify manifest integrity
- **Sanitization**: Remove sensitive data for public release
- **Checksum Computation**: SHA256 and SHA512

### API Usage

```python
from manifest_validator import ManifestValidator, ManifestParser, ManifestSigner

# Load and validate
manifest = ManifestParser.load(Path("manifest.yaml"))
validator = ManifestValidator()
is_valid, errors = validator.validate(manifest)

# Sign
signer = ManifestSigner()
signer.sign(Path("manifest.yaml"), key_id="0xYOURKEY")

# Sanitize
from manifest_validator import ManifestSanitizer
sanitizer = ManifestSanitizer()
public_manifest = sanitizer.sanitize(manifest)
```

## Security Recommendations

1. **Never commit sensitive manifests** - Use `.gitignore` for internal manifests
2. **Sign all production manifests** - Use GPG for non-repudiation
3. **Sanitize before sharing** - Always use the sanitizer for public releases
4. **Store keys in vault** - Never embed private keys in manifests
5. **Rotate signing keys** - Follow your organization's key rotation policy

## Manifest Field Classifications

| Classification | Handling |
|----------------|----------|
| `public` | Safe for external distribution |
| `internal` | Organization internal only |
| `confidential` | Need-to-know basis |
| `restricted` | DO NOT PUBLISH |
| `top_secret` | Maximum protection required |

## Integration with CI/CD

Add to your GitHub Actions:

```yaml
- name: Validate Manifests
  run: |
    pip install -r schemas/requirements-schemas.txt
    python schemas/manifest_validator.py validate dao_record.yaml
    python schemas/manifest_validator.py validate discovery.yml
```

## License

Part of the Sovereignty Architecture project. See repository LICENSE for details.
