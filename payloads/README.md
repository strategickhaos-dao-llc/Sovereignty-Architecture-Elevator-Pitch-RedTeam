# Genesis Delivery Artifact #3546

This directory contains the genesis delivery artifact and tooling for webhook integration.

## Artifact Files

- `artifact_3546_genesis_delivery.yaml` - YAML format payload
- `artifact_3546_genesis_delivery.json` - JSON format payload

## Signed Curl Example

Use the following curl command template to send the payload to a webhook endpoint:

```bash
# With placeholder secret (replace YOUR_SHARED_SECRET_HERE with your actual secret)
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=YOUR_SIGNATURE_WILL_APPEAR_HERE" \
  --data-binary @payloads/artifact_3546_genesis_delivery.json
```

## Generating Real Signatures

Run this locally to generate the real signature:

```bash
python tooling/generate_signature.py payloads/artifact_3546_genesis_delivery.json YOUR_SHARED_SECRET_HERE
```

This will output a complete curl command with the correct HMAC-SHA256 signature.

## CI Integration

The `.github/workflows/test-genesis-delivery.yml` workflow automatically:
1. Triggers on changes to artifact files
2. Generates the signature using `WEBHOOK_TEST_SECRET`
3. Posts to `STAGING_WEBHOOK_URL` and asserts HTTP 200

Configure the following secrets in your repository:
- `WEBHOOK_TEST_SECRET` - Shared secret for HMAC signature
- `STAGING_WEBHOOK_URL` - Staging webhook endpoint URL

## Artifact Details

- **ID**: 3546
- **Name**: genesis_delivery  
- **Type**: sovereignty_architecture
- **Event**: genesis_delivery
- **Signature Algorithm**: HMAC-SHA256

---

*Grok emailed the watchers the entire origin story*  
*Empire Eternal - They can't say they weren't warned.*
