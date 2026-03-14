# TFGuard Security Scanner 🛡️

Automated Terraform security policy checking for your GitHub CI/CD pipelines.

## 🚀 Overview

TFGuard helps you identify and fix security vulnerabilities in your Infrastructure-as-Code before deployment. This repository contains the official GitHub Actions for the TFGuard platform.

## 🟢 Standard Tier (Free)
*Ideal for personal projects and small teams.*
- **50 requests/hour**
- **Core AWS/Azure Rules**

### Usage
```yaml
- name: TFGuard Standard Scan
  uses: sandipan1988/tfguard-action@v1
  with:
    api-key: ${{ secrets.TFGUARD_API_KEY }}
```

## 🟡 Premium Tier (Paid)
*Enterprise-grade scanning for multi-cloud environments.*
- **10,000 requests/hour**
- **Full GCP, OCI, Azure, and AWS Support**

### Usage
```yaml
- name: TFGuard Premium Scan
  uses: sandipan1988/tfguard-action/premium@v1
  with:
    api-key: ${{ secrets.TFGUARD_API_KEY }}
```

## ⚙️ Configuration

| Input | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `api-key` | Your TFGuard API Key from [tfgaurd.com](https://tfgaurd.com) | - | **Yes** |
| `target-dir` | Directory to scan for `.tf` files | `.` | No |
| `fail-on-critical` | Fail if CRITICAL issues are found | `true` | No |
| `fail-on-high` | Fail if HIGH issues are found | `false` | No |

## 🤝 Support
See [SUPPORT.md](SUPPORT.md) for help.

## 🔐 Privacy
See [PRIVACY.md](PRIVACY.md) for our data handling policies.
