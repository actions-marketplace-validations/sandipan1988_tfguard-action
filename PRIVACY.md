# Privacy Policy for TFGuard

Last updated: March 14, 2026

## Introduction
TFGuard ("we," "us," or "our") is committed to protecting your privacy. This Privacy Policy explains how we handle your information when you use the TFGuard GitHub Action and associated services.

## Data Collection
### 1. Source Code
TFGuard does **not** store your Terraform source code. When you use the TFGuard GitHub Action:
- Your code is analyzed for security policy violations.
- The code is processed in-memory.
- Only metadata about the analysis (e.g., number of resources, violation types, execution time) is logged for security and analytics purposes.

### 2. API Keys
When you generate an API key on tfgaurd.com, we store:
- Your username (linked to your WhatsApp number or account).
- A hash of your API key.
- Usage statistics (count and last used timestamp).

### 3. Usage Analytics
We collect anonymized usage data to improve our security rules, including:
- Resource types scanned (e.g., `aws_s3_bucket`).
- Types of security violations found.
- GitHub repository names (where available via Action context).

## Data Security
We implement industry-standard security measures to protect your API keys and usage data. 

## Third-Party Services
TFGuard uses:
- **Twilio**: For sending WhatsApp OTPs (if applicable).
- **Google OAuth**: For authentication (if applicable).

## Changes to This Policy
We may update this policy from time to time. We will notify users of any significant changes by updating the "Last updated" date at the top of this policy.

## Contact Us
If you have questions about this Privacy Policy, please contact us at support@tfgaurd.com.
