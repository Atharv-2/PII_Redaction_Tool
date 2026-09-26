# PII Redaction Tool

A Python-based PII Redaction Tool that detects and replaces Personally Identifiable Information (PII) from DOCX documents while maintaining consistent replacements throughout the document.

## Overview

This project was developed as part of the Scaler AI Labs PII Redaction Tool assignment.

The tool processes a DOCX document, detects supported PII categories using pattern-based and rule-based detection, and replaces the detected information with synthetic values.

The main objective is to prevent sensitive information from remaining exposed in the processed document.

## Features

- DOCX document processing
- PII detection using regular expressions and rule-based detection
- Consistent replacement of repeated PII
- Address detection including multi-line addresses
- Phone number detection
- Email detection
- Person name detection
- Company name detection
- IP address detection
- SSN detection
- Credit card detection with Luhn validation
- Date of birth detection
- Processing of:
  - Normal paragraphs
  - Table cells
  - Headers
  - Footers

## Supported PII Categories

The tool currently supports:

| Category | Detection Method |
|---|---|
| Names | Known-name and labelled-name matching |
| Companies | Known-company and generic company matching |
| Emails | Regular expression |
| Phone Numbers | Regular expression |
| Addresses | PIN-based and rule-based detection |
| IP Addresses | Regular expression |
| SSNs | Regular expression |
| Credit Cards | Pattern matching + Luhn validation |
| Date of Birth | Labelled and text-based patterns |

## How It Works

The redaction pipeline follows these steps:

```text
DOCX Input
    |
    v
Extract document text
    |
    v
Normalize text
    |
    v
Run PII detectors
    |
    v
Collect detected spans
    |
    v
Resolve overlapping detections
    |
    v
Generate consistent synthetic replacements
    |
    v
Replace PII
    |
    v
Generate redacted DOCX