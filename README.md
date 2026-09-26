# PII Redaction Tool

## Overview

This project is a PII (Personally Identifiable Information) redaction tool developed for the Scaler AI Labs assignment.

The tool reads a Red Herring Prospectus in DOCX format, detects different types of personally identifiable or sensitive information, and replaces the detected information with synthetic/fake alternatives while preserving the overall document structure.

## PII Types Detected

The tool supports detection and redaction of:

- Full Names
- Email Addresses
- Phone Numbers
- Company Names
- Physical/Mailing Addresses
- Social Security Numbers (SSNs)
- Credit Card Numbers
- Dates of Birth
- IP Addresses

## Approach

The solution uses a rule-based detection pipeline implemented in Python.

Different detection techniques are used depending on the PII type:

- **Email addresses:** Regular expressions
- **Phone numbers:** Regular expressions supporting Indian mobile numbers and landline formats
- **IP addresses:** Regular expressions
- **SSNs:** Regular expressions
- **Credit card numbers:** Regular expressions with Luhn validation
- **Dates of birth:** Pattern-based detection
- **Names:** Known-name matching and contextual/label-based detection
- **Company names:** Known-company matching and pattern-based detection
- **Addresses:** Keyword-based and multi-line address detection using address indicators and PIN codes

The detected PII is replaced using synthetic values.

## Consistent Replacement

A mapping system is used so that the same PII value is replaced with the same synthetic value throughout the document.

For example:

```text
Original:
person@example.com

Redacted:
user1@example.com