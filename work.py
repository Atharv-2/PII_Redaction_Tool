import re
import unicodedata
from dataclasses import dataclass
from docx import Document


# =========================================================
# FILE PATHS
# =========================================================

input_file = r"C:\Users\ATHARV\OneDrive\Desktop\PII_Redacted\Red Herring Prospectus.docx"

output_file = r"C:\Users\ATHARV\OneDrive\Desktop\PII_Redacted\Final_Redacted_Prospectus.docx"


# =========================================================
# FAKE VALUES
# =========================================================

FAKE_NAMES = [
    "John Smith",
    "Peter Parker",
    "Michael Brown",
    "David Wilson",
    "James Anderson",
    "Robert Taylor",
    "William Harris",
    "Daniel Thomas",
    "Alex Johnson",
    "Chris Martin",
    "Matthew Clark",
    "Andrew Lewis",
    "Steven Walker",
    "Kevin Young",
    "Brian King",
    "Edward Wright"
]

FAKE_COMPANIES = [
    "Alpha Technologies Limited",
    "Global Solutions Private Limited",
    "Prime Industries Limited",
    "Vertex Systems Limited",
    "Nova Enterprises Limited",
    "Future Industries Limited",
    "Blue Horizon Private Limited",
    "Silverline Industries Limited",
    "Crestwood Holdings Limited",
    "Meridian Corp Private Limited"
]


# =========================================================
# KNOWN PERSON NAMES
# =========================================================

KNOWN_NAMES = [
    "Kushal Subbayya Hegde",
    "Pushpa Kushal Hegde",
    "Rajesh Kushal Hegde",
    "Rohit Kushal Hegde",
    "Rakhi Girija Shetty",
    "Sangeeta Ramprasad Rai",
    "Sarthak Malvadkar",
    "Sandesh Bhagwat",
    "Amod Joshi",
    "Dinesh Hirachand Munot",
    "Ajay Shriram Patil",
    "Ram Kumar Tiwari",
    "Indu Jacob",
    "Lalit Muljibhai Sarvaiya",
    "Lokesh Shah",
    "Soumavo Sarkar",
    "Kishan Rastogi",
    "Abhijit Diwan",
    "Prakash Boricha",
    "Shanti Gopalkrishnan",
    "Eric Bacha",
    "Sachin Gawade",
    "Pravin Teli",
    "Siddharth Jadhav",
    "Tushar Gavankar",
    "Varun Badai",
    "Hitesh Ramani",
    "Chitra Raste",
    "Sharmila Joshi",
    "Cherag Gyara",
    "Manisha Shukla",
    "Tushar Wakhele",
    "Ashish Mathew Pulloor",
    "Anand Soni"
]


# =========================================================
# KNOWN COMPANIES
# =========================================================

KNOWN_COMPANIES = [
    "KSH International Limited",
    "Waterloo Industrial Park VI Private Limited",
    "Waterloo Motors Private Limited",
    "KSH Project Management Services Private Limited",
    "KSH Infra Park 5 Private Limited",
    "KSH Infra Park VI Private Limited",
    "KSH Distriparks Private Limited",
    "KSH Integrated Logistics Private Limited",
    "Kushal Motors and Electricals Private Limited",
    "Waterloo Industrial Park I Private Limited",
    "Waterloo Industrial Park II Private Limited",
    "Waterloo Industrial Park III Private Limited",
    "Waterloo Industrial Park IV Private Limited",
    "Waterloo Industrial Park V Private Limited",
    "Waterloo Industrial Park VIII Private Limited",
    "Waterloo Industrial Park IX Private Limited",
    "Waterloo Industrial Park IX A Private Limited",
    "Waterloo Industrial Park IX B Private Limited",
    "KSH Infra Park IV Private Limited",
    "CARE Analytics and Advisory Private Limited",
    "Kirtane & Pandit LLP"
]


# =========================================================
# ADDRESS KEYWORDS
# =========================================================

ADDRESS_KEYWORDS = [
    "road",
    "street",
    "lane",
    "village",
    "plot",
    "building",
    "floor",
    "taluka",
    "district",
    "society",
    "apartment",
    "park",
    "nagar",
    "s. no.",
    "s.no.",
    "survey no",
    "block",
    "sector",
    "chawl",
    "chs",
    "wing",
    "marg",
    "gali",
    "colony",
    "tehsil",
    "bunglow",
    "bungalow",
    "flat",
    "house",
    "gat no",
    "near",
    "opposite",
    "behind",
    "residency",
    "industrial estate",
    "tower",
    "business centre",
    "business center",
    "complex",
    "bhavan",
    "campus",
    "centre",
    "center",
    "estate"
]


# =========================================================
# PIN CODE
# Supports:
# 411045
# 411 045
# 411-045
# =========================================================

PIN_PATTERN = r"\b\d{3}\s*[-–]?\s*\d{3}\b"


# =========================================================
# SPAN
# =========================================================

@dataclass
class Span:
    start: int
    end: int
    category: str
    text: str
    priority: int


# =========================================================
# MAPPER
# =========================================================

class Mapper:

    def __init__(self):
        self.maps = {}
        self.counts = {}

    def get(self, category, original, factory):

        mapping = self.maps.setdefault(
            category,
            {}
        )

        key = original.strip().lower()

        if key not in mapping:

            mapping[key] = factory(
                len(mapping)
            )

            self.counts[category] = (
                self.counts.get(
                    category,
                    0
                ) + 1
            )

        return mapping[key]

    def unique_count(self, category):

        return len(
            self.maps.get(
                category,
                {}
            )
        )

    def total_count(self, category):

        return self.counts.get(
            category,
            0
        )


mapper = Mapper()


# =========================================================
# FAKE VALUE FUNCTIONS
# =========================================================

def fake_name(original):

    return mapper.get(
        "names",
        original,
        lambda i:
            FAKE_NAMES[
                i % len(FAKE_NAMES)
            ]
    )


def fake_company(original):

    return mapper.get(
        "companies",
        original,
        lambda i:
            FAKE_COMPANIES[
                i % len(FAKE_COMPANIES)
            ]
    )


def fake_email(original):

    return mapper.get(
        "emails",
        original,
        lambda i:
            f"user{i + 1}@example.com"
    )


def fake_phone(original):

    return mapper.get(
        "phones",
        original,
        lambda i:
            f"+91 90000{i + 1:05d}"
    )


def fake_address(original):

    return mapper.get(
        "addresses",
        original,
        lambda i:
            f"{100 + i} Example Street, Mumbai, Maharashtra 400001"
    )


def fake_ssn(original):

    return mapper.get(
        "ssn",
        original,
        lambda i:
            "123-45-6789"
    )


def fake_credit_card(original):

    return mapper.get(
        "credit_cards",
        original,
        lambda i:
            "4111 1111 1111 1111"
    )


def fake_ip(original):

    return mapper.get(
        "ips",
        original,
        lambda i:
            "192.0.2.1"
    )


def fake_dob(original):

    return mapper.get(
        "dob",
        original,
        lambda i:
            "01/01/1990"
    )


# =========================================================
# NORMALIZE
# =========================================================

def normalize(text):

    text = text.replace(
        "\xa0",
        " "
    )

    text = text.replace(
        "\t",
        " "
    )

    text = unicodedata.normalize(
        "NFKC",
        text
    )

    text = re.sub(
        r"[ ]{2,}",
        " ",
        text
    )

    return text


# =========================================================
# GENERIC SPAN CREATOR
# =========================================================

def make_spans(
    pattern,
    text,
    category,
    priority,
    flags=0
):

    result = []

    for match in re.finditer(
        pattern,
        text,
        flags
    ):

        result.append(
            Span(
                match.start(),
                match.end(),
                category,
                match.group(),
                priority
            )
        )

    return result


# =========================================================
# EMAIL
# =========================================================

def find_emails(text):

    pattern = (
        r"\b"
        r"[\w.%+-]+"
        r"@"
        r"[\w.-]+"
        r"\."
        r"[A-Za-z]{2,}"
        r"\b"
    )

    return make_spans(
        pattern,
        text,
        "email",
        1
    )


# =========================================================
# IP ADDRESS
# =========================================================

def find_ips(text):

    pattern = (
        r"\b"
        r"(?:\d{1,3}\.){3}"
        r"\d{1,3}"
        r"\b"
    )

    return make_spans(
        pattern,
        text,
        "ip",
        1
    )


# =========================================================
# SSN
# =========================================================

def find_ssn(text):

    pattern = r"\b\d{3}-\d{2}-\d{4}\b"

    return make_spans(
        pattern,
        text,
        "ssn",
        1
    )


# =========================================================
# CREDIT CARD
# =========================================================

def luhn_check(number):

    digits = [
        int(x)
        for x in number
        if x.isdigit()
    ]

    total = 0

    for i, digit in enumerate(
        reversed(digits)
    ):

        if i % 2 == 1:

            digit *= 2

            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0


def find_credit_cards(text):

    pattern = (
        r"(?<!\d)"
        r"(?:\d[ -]?){13,19}"
        r"(?!\d)"
    )

    result = []

    for match in re.finditer(
        pattern,
        text
    ):

        clean = re.sub(
            r"\D",
            "",
            match.group()
        )

        if (
            13 <= len(clean) <= 19
            and luhn_check(clean)
        ):

            result.append(
                Span(
                    match.start(),
                    match.end(),
                    "credit_card",
                    match.group(),
                    1
                )
            )

    return result


# =========================================================
# PHONE
# =========================================================

def find_phones(text):

    pattern = (
        r"(?<!\d)"
        r"(?:"
        r"\+\s*(?:\+\s*)?91[\s-]*"
        r")?"
        r"(?:"
        r"\(\s*\d{2,4}\s*\)"
        r"[\s-]*"
        r"\d{4}[\s-]\d{4}"
        r"|"
        r"\(\s*\d{2,4}\s*\)"
        r"[\s-]*"
        r"\d{6,8}"
        r"|"
        r"\d{2,4}[\s-]"
        r"\d{4}[\s-]\d{4}"
        r"|"
        r"\d{2,4}[\s-]"
        r"\d{6,8}"
        r"|"
        r"\d{5}[\s-]\d{5}"
        r"|"
        r"[6-9]\d{9}"
        r")"
        r"(?!\d)"
    )

    return make_spans(
        pattern,
        text,
        "phone",
        1
    )


# =========================================================
# DOB
# =========================================================

def find_dob(text):

    result = []

    labelled = (
        r"(?i)"
        r"(date of birth|dob|date-of-birth)"
        r"(\s*[:\-]\s*)"
        r"("
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r")"
    )

    for match in re.finditer(
        labelled,
        text
    ):

        result.append(
            Span(
                match.start(3),
                match.end(3),
                "dob",
                match.group(3),
                1
            )
        )

    prose = (
        r"(?i)"
        r"\bborn\s+(?:on\s+)?"
        r"("
        r"\d{1,2}(?:st|nd|rd|th)?"
        r"\s+[A-Za-z]+\s+\d{4}"
        r"|"
        r"[A-Za-z]+\s+"
        r"\d{1,2}(?:st|nd|rd|th)?,?"
        r"\s+\d{4}"
        r")"
    )

    for match in re.finditer(
        prose,
        text
    ):

        result.append(
            Span(
                match.start(1),
                match.end(1),
                "dob",
                match.group(1),
                1
            )
        )

    return result


# =========================================================
# KNOWN NAMES
# =========================================================

def find_known_names(text):

    result = []

    for name in sorted(
        KNOWN_NAMES,
        key=len,
        reverse=True
    ):

        flexible = r"\s+".join(
            re.escape(part)
            for part in name.split()
        )

        pattern = (
            r"(?<![A-Za-z])"
            + flexible
            + r"(?![A-Za-z])"
        )

        for match in re.finditer(
            pattern,
            text,
            re.IGNORECASE
        ):

            result.append(
                Span(
                    match.start(),
                    match.end(),
                    "name",
                    match.group(),
                    2
                )
            )

    return result


# =========================================================
# LABELLED NAMES
# =========================================================

def find_labelled_names(text):

    result = []

    pattern = re.compile(
        r"(?i)"
        r"\bcontact\s+person\s*:\s*"
        r"([^\n;]+?)"
        r"(?="
        r"\b(?:telephone|"
        r"email|"
        r"website|"
        r"sebi\s+registration|"
        r"sebi\s+registration\s+no)"
        r"\b"
        r"|\n|$)"
    )

    for match in pattern.finditer(
        text
    ):

        value = match.group(1).strip()

        value = re.split(
            r"\b(?:"
            r"company secretary|"
            r"website|"
            r"email|"
            r"telephone"
            r")\b",
            value,
            flags=re.I
        )[0]

        for item in re.split(
            r"/",
            value
        ):

            item = item.strip(
                " ,"
            )

            if len(
                item.split()
            ) < 2:
                continue

            start = text.find(
                item,
                match.start(1),
                match.end(1)
            )

            if start >= 0:

                result.append(
                    Span(
                        start,
                        start + len(item),
                        "name",
                        item,
                        2
                    )
                )

    return result


# =========================================================
# KNOWN COMPANIES
# =========================================================

def find_known_companies(text):

    result = []

    for company in sorted(
        KNOWN_COMPANIES,
        key=len,
        reverse=True
    ):

        flexible = r"\s+".join(
            re.escape(part)
            for part in company.split()
        )

        pattern = (
            r"(?<![A-Za-z])"
            + flexible
            + r"(?![A-Za-z])"
        )

        for match in re.finditer(
            pattern,
            text,
            re.IGNORECASE
        ):

            result.append(
                Span(
                    match.start(),
                    match.end(),
                    "company",
                    match.group(),
                    4
                )
            )

    return result


# =========================================================
# GENERIC COMPANIES
# =========================================================

def find_generic_companies(text):

    result = []

    pattern = (
        r"\b"
        r"[A-Z][A-Za-z&.,' -]{2,80}"
        r"\b"
        r"(?:"
        r"Private Limited"
        r"|Limited"
        r"|LLP"
        r"|Corporation"
        r"|Inc\."
        r"|Incorporated"
        r")"
        r"\b"
    )

    for match in re.finditer(
        pattern,
        text
    ):

        value = match.group().strip()

        lower = value.lower()

        if lower in {
            "private limited",
            "public limited",
            "limited liability partnership"
        }:
            continue

        result.append(
            Span(
                match.start(),
                match.end(),
                "company",
                value,
                4
            )
        )

    return result


# =========================================================
# MULTI-LINE ADDRESS DETECTOR
# =========================================================

def find_pin_address_lines(text):

    result = []

    lines = text.split("\n")

    line_starts = []

    cursor = 0

    for line in lines:

        line_starts.append(
            cursor
        )

        cursor += len(line) + 1

    pin_re = re.compile(
        PIN_PATTERN
    )

    address_words = [
        "road",
        "street",
        "lane",
        "apartment",
        "society",
        "bunglow",
        "bungalow",
        "building",
        "flat",
        "house",
        "plot",
        "park",
        "colony",
        "residency",
        "nagar",
        "tower",
        "floor",
        "bhavan",
        "complex",
        "village",
        "district",
        "taluka",
        "marg",
        "near",
        "behind",
        "opposite",
        "estate",
        "wing",
        "centre",
        "center",
        "business centre",
        "business center",
        "block",
        "sector"
    ]

    for i, line in enumerate(lines):

        pin_matches = list(
            pin_re.finditer(
                line
            )
        )

        if not pin_matches:
            continue

        for pin_match in pin_matches:

            end = (
                line_starts[i]
                + pin_match.end()
            )

            start_line = i

            for j in range(
                max(0, i - 3),
                i
            ):

                previous = lines[j].strip()

                if not previous:
                    continue

                lower = previous.lower()

                has_address_word = any(
                    word in lower
                    for word in address_words
                )

                has_address_number = bool(
                    re.search(
                        r"\b(?:"
                        r"\d{1,4}"
                        r"|"
                        r"[A-Z]-\d+"
                        r"|"
                        r"S\.?\s*No\.?"
                        r"|"
                        r"Plot\s+No\.?"
                        r"|"
                        r"Gat\s+No\.?"
                        r")",
                        previous,
                        re.I
                    )
                )

                if (
                    has_address_word
                    or has_address_number
                ):
                    start_line = j
                else:
                    break

            start = line_starts[
                start_line
            ]

            candidate = text[
                start:end
            ].strip()

            if len(candidate) < 15:
                continue

            lower_candidate = candidate.lower()

            has_address_word = any(
                word in lower_candidate
                for word in address_words
            )

            has_number = bool(
                re.search(
                    r"\b\d+[A-Za-z]?"
                    r"(?:[-/]\d+)*\b",
                    candidate
                )
            )

            if not (
                has_address_word
                or has_number
            ):
                continue

            result.append(
                Span(
                    start,
                    end,
                    "address",
                    candidate,
                    3
                )
            )

    return result


# =========================================================
# ADDRESS DETECTOR
# =========================================================

def find_addresses(text):

    result = []

    lines = text.split("\n")

    line_starts = []

    cursor = 0

    for line in lines:

        line_starts.append(
            cursor
        )

        cursor += len(line) + 1

    pin_re = re.compile(
        PIN_PATTERN
    )

    for i, line in enumerate(lines):

        matches = list(
            pin_re.finditer(line)
        )

        if not matches:
            continue

        for pin_match in matches:

            before_pin = line[
                :pin_match.end()
            ]

            label_pattern = re.compile(
                r"(?i)"
                r"(?:"
                r"registered\s+office"
                r"|corporate\s+office"
                r"|registered\s+address"
                r"|corporate\s+address"
                r"|address"
                r"|located\s+at"
                r"|situated\s+at"
                r"|facility\s+located\s+at"
                r"|having\s+its\s+registered\s+office\s+at"
                r"|having\s+its\s+corporate\s+office\s+at"
                r")"
            )

            labels = list(
                label_pattern.finditer(
                    before_pin
                )
            )

            if labels:

                label = labels[-1]

                start = (
                    line_starts[i]
                    + label.end()
                )

                while (
                    start <
                    line_starts[i]
                    + len(line)
                    and text[start] in " :,-"
                ):
                    start += 1

                end = (
                    line_starts[i]
                    + pin_match.end()
                )

                candidate = text[
                    start:end
                ].strip()

                if len(candidate) >= 10:

                    result.append(
                        Span(
                            start,
                            end,
                            "address",
                            candidate,
                            3
                        )
                    )

                    continue

            start_pattern = re.compile(
                r"(?i)"
                r"(?:"
                r"S\.?\s*No\.?\s*"
                r"|Plot\s+No\.?\s*"
                r"|Gat\s+No\.?\s*"
                r"|Flat\s*[-–]?\s*"
                r"|House\s+No\.?\s*"
                r"|H\.?\s*No\.?\s*"
                r"|A-\d+\s*,?\s*"
                r"|B-\d+\s*,?\s*"
                r"|\d{1,4}[A-Za-z]?"
                r"(?:[-/]\d+)+\s*,?\s*"
                r")"
            )

            candidates = list(
                start_pattern.finditer(
                    before_pin
                )
            )

            if candidates:

                candidate_match = (
                    candidates[-1]
                )

                start = (
                    line_starts[i]
                    + candidate_match.start()
                )

                prefix = line[
                    :candidate_match.start()
                ]

                previous_comma = (
                    prefix.rfind(",")
                )

                if previous_comma >= 0:

                    previous_part = (
                        prefix[
                            previous_comma + 1:
                        ].strip()
                    )

                    if re.search(
                        r"(?i)\b("
                        r"apartment|"
                        r"bunglow|"
                        r"bungalow|"
                        r"society|"
                        r"residency|"
                        r"complex|"
                        r"building|"
                        r"tower|"
                        r"park|"
                        r"estate|"
                        r"colony"
                        r")\b",
                        previous_part
                    ):

                        start = (
                            line_starts[i]
                            + previous_comma
                            + 1
                        )

                end = (
                    line_starts[i]
                    + pin_match.end()
                )

                candidate = text[
                    start:end
                ].strip()

                if len(candidate) >= 10:

                    result.append(
                        Span(
                            start,
                            end,
                            "address",
                            candidate,
                            3
                        )
                    )

                    continue

            keyword_pattern = re.compile(
                r"(?i)\b("
                + "|".join(
                    re.escape(x)
                    for x in ADDRESS_KEYWORDS
                )
                + r")\b"
            )

            keywords = list(
                keyword_pattern.finditer(
                    before_pin
                )
            )

            if keywords:

                keyword = keywords[-1]

                prefix = line[
                    :keyword.start()
                ]

                comma = prefix.rfind(",")

                if comma >= 0:

                    start = (
                        line_starts[i]
                        + comma
                        + 1
                    )

                else:

                    start = (
                        line_starts[i]
                        + keyword.start()
                    )

                end = (
                    line_starts[i]
                    + pin_match.end()
                )

                candidate = text[
                    start:end
                ].strip()

                if len(candidate) >= 10:

                    result.append(
                        Span(
                            start,
                            end,
                            "address",
                            candidate,
                            3
                        )
                    )

    return result


# =========================================================
# ADDRESS BLOCK DETECTOR
# =========================================================

def find_address_blocks(text):

    result = []

    lines = text.split("\n")

    line_starts = []

    cursor = 0

    for line in lines:

        line_starts.append(
            cursor
        )

        cursor += len(line) + 1

    strong_words = [
        "road",
        "street",
        "lane",
        "apartment",
        "society",
        "bunglow",
        "bungalow",
        "building",
        "flat",
        "house",
        "plot",
        "park",
        "colony",
        "residency",
        "nagar",
        "tower",
        "floor",
        "bhavan",
        "complex",
        "village",
        "district",
        "taluka",
        "marg",
        "near",
        "behind",
        "opposite",
        "estate",
        "wing",
        "block",
        "sector",
        "business centre",
        "business center"
    ]

    for i, line in enumerate(lines):

        value = line.strip()

        if not value:
            continue

        lower = value.lower()

        has_address_word = any(
            word in lower
            for word in strong_words
        )

        has_number = bool(
            re.search(
                r"\b(?:"
                r"s\.?\s*no\.?"
                r"|plot\s+no\.?"
                r"|gat\s+no\.?"
                r"|flat\s*[-/]?\s*\d+"
                r"|house\s+no\.?"
                r"|\d{1,4}[-/]\d+"
                r"|\d{3,4}\s*[-–]\s*\d{3,4}"
                r")\b",
                value,
                re.I
            )
        )

        if not (
            has_address_word
            and has_number
        ):
            continue

        start_line = i
        end_line = i

        if i > 0:

            previous = lines[
                i - 1
            ].strip()

            previous_lower = (
                previous.lower()
            )

            previous_has_address_word = any(
                word in previous_lower
                for word in strong_words
            )

            previous_has_number = bool(
                re.search(
                    r"\b\d{1,4}\b",
                    previous
                )
            )

            if (
                previous_has_address_word
                or previous_has_number
            ):

                start_line = i - 1

        if i + 1 < len(lines):

            nxt = lines[
                i + 1
            ].strip()

            nxt_lower = nxt.lower()

            next_has_address_word = any(
                word in nxt_lower
                for word in strong_words
            )

            next_has_pin = bool(
                re.search(
                    PIN_PATTERN,
                    nxt
                )
            )

            if (
                next_has_address_word
                or next_has_pin
            ):

                end_line = i + 1

        start = line_starts[
            start_line
        ]

        end = (
            line_starts[end_line]
            + len(lines[end_line])
        )

        candidate = text[
            start:end
        ].strip()

        if len(candidate) < 15:
            continue

        result.append(
            Span(
                start,
                end,
                "address",
                candidate,
                3
            )
        )

    return result


# =========================================================
# PIPELINE
# =========================================================

PIPELINE = [
    find_emails,
    find_ips,
    find_ssn,
    find_credit_cards,
    find_phones,
    find_dob,
    find_pin_address_lines,
    find_addresses,
    find_address_blocks,
    find_known_names,
    find_labelled_names,
    find_known_companies,
    find_generic_companies
]


# =========================================================
# FAKERS
# =========================================================

FAKERS = {
    "email": fake_email,
    "ip": fake_ip,
    "ssn": fake_ssn,
    "credit_card": fake_credit_card,
    "phone": fake_phone,
    "dob": fake_dob,
    "address": fake_address,
    "name": fake_name,
    "company": fake_company
}


# =========================================================
# OVERLAP RESOLUTION
# =========================================================

def resolve_overlaps(spans):

    spans = sorted(
        spans,
        key=lambda s: (
            s.priority,
            -(s.end - s.start),
            s.start
        )
    )

    chosen = []

    occupied = []

    for span in spans:

        overlap = False

        for start, end in occupied:

            if not (
                span.end <= start
                or span.start >= end
            ):

                overlap = True
                break

        if overlap:
            continue

        chosen.append(
            span
        )

        occupied.append(
            (
                span.start,
                span.end
            )
        )

    return sorted(
        chosen,
        key=lambda s: s.start
    )


# =========================================================
# DETECT PII
# =========================================================

def detect_spans(text):

    all_spans = []

    for detector in PIPELINE:

        detected = detector(
            text
        )

        all_spans.extend(
            detected
        )

    return resolve_overlaps(
        all_spans
    )


# =========================================================
# REDACT TEXT
# =========================================================

def redact(text):

    if not text.strip():
        return text

    text = normalize(
        text
    )

    spans = detect_spans(
        text
    )

    for span in reversed(
        spans
    ):

        replacement = FAKERS[
            span.category
        ](
            span.text
        )

        text = (
            text[:span.start]
            + replacement
            + text[span.end:]
        )

    return text


# =========================================================
# COLLECT DOCUMENT PARAGRAPHS
# =========================================================

def collect_paragraphs(doc):

    paragraphs = []

    paragraphs.extend(
        doc.paragraphs
    )

    for table in doc.tables:

        for row in table.rows:

            for cell in row.cells:

                paragraphs.extend(
                    cell.paragraphs
                )

    for section in doc.sections:

        paragraphs.extend(
            section.header.paragraphs
        )

        paragraphs.extend(
            section.footer.paragraphs
        )

    return paragraphs


# =========================================================
# SET PARAGRAPH TEXT
# =========================================================

def set_paragraph_text(
    paragraph,
    new_text
):

    if not paragraph.runs:

        paragraph.add_run(
            new_text
        )

        return

    paragraph.runs[0].text = (
        new_text
    )

    for run in paragraph.runs[1:]:

        run.text = ""


# =========================================================
# PROCESS DOCUMENT
# =========================================================

def redact_document(
    input_path,
    output_path
):

    doc = Document(
        input_path
    )

    paragraphs = collect_paragraphs(
        doc
    )

    original_texts = []

    for paragraph in paragraphs:

        original_texts.append(
            normalize(
                paragraph.text
            )
        )

    combined_parts = []

    paragraph_ranges = []

    cursor = 0

    for i, value in enumerate(
        original_texts
    ):

        start = cursor

        end = (
            start
            + len(value)
        )

        paragraph_ranges.append(
            (
                start,
                end
            )
        )

        combined_parts.append(
            value
        )

        cursor = end

        if (
            i
            != len(original_texts) - 1
        ):

            combined_parts.append(
                "\n"
            )

            cursor += 1

    combined = "".join(
        combined_parts
    )

    spans = detect_spans(
        combined
    )

    replacements = [
        []
        for _ in paragraphs
    ]

    for span in spans:

        replacement = FAKERS[
            span.category
        ](
            span.text
        )

        for i, (
            paragraph_start,
            paragraph_end
        ) in enumerate(
            paragraph_ranges
        ):

            if (
                span.end <= paragraph_start
                or
                span.start >= paragraph_end
            ):
                continue

            local_start = (
                max(
                    span.start,
                    paragraph_start
                )
                - paragraph_start
            )

            local_end = (
                min(
                    span.end,
                    paragraph_end
                )
                - paragraph_start
            )

            replacements[i].append(
                (
                    local_start,
                    local_end,
                    replacement
                )
            )

    for i, paragraph in enumerate(
        paragraphs
    ):

        text = original_texts[i]

        edits = sorted(
            replacements[i],
            key=lambda x: x[0],
            reverse=True
        )

        for (
            start,
            end,
            replacement
        ) in edits:

            text = (
                text[:start]
                + replacement
                + text[end:]
            )

        if text != paragraph.text:

            set_paragraph_text(
                paragraph,
                text
            )

    doc.save(
        output_path
    )


# =========================================================
# REPORT
# =========================================================

def print_report():

    print()
    print("=" * 60)
    print("PII REDACTION COMPLETED")
    print("=" * 60)

    categories = [
        ("names", "Names"),
        ("companies", "Companies"),
        ("emails", "Emails"),
        ("phones", "Phones"),
        ("addresses", "Addresses"),
        ("ssn", "SSNs"),
        ("credit_cards", "Credit Cards"),
        ("dob", "DOBs"),
        ("ips", "IP Addresses")
    ]

    for category, label in categories:

        print(
            f"{label}: "
            f"{mapper.unique_count(category)} "
            f"unique / "
            f"{mapper.total_count(category)} "
            f"total"
        )

    print()

    print("Output file:")
    print(output_file)

    print()
    print("=" * 60)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    redact_document(
        input_file,
        output_file
    )

    print_report()