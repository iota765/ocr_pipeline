import re
from typing import Dict, List


# ---------- generic PII ----------
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"\b(?:\+?91[-\s]?)?[6-9]\d{9}\b")
DATE = re.compile(r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b")
AADHAAR = re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b")
PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")

# ---------- demographics ----------
PATIENT_NAME = re.compile(r"patient\s*name\s*[:\-]?\s*(.*)", re.IGNORECASE)
IPD = re.compile(r"(?:IPD|I\.?\s*P\.?)\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\/\-\s]+)", re.IGNORECASE)
UHID = re.compile(r"UHID\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\s\/\-]+)", re.IGNORECASE)
BED = re.compile(r"Bed\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)", re.IGNORECASE)
AGE = re.compile(r"Age\s*[:\-]?\s*(\d{1,3})", re.IGNORECASE)
SEX = re.compile(r"Sex\s*[:\-]?\s*(Male|Female|M|F)", re.IGNORECASE)

# ---------- vitals ----------
BP = re.compile(r"BP\s*[:\-]?\s*(\d{2,3}\s*/\s*\d{2,3})", re.IGNORECASE)
PR = re.compile(r"PR\s*[:\-]?\s*(\d{1,3})", re.IGNORECASE)
RR = re.compile(r"RR\s*[:\-]?\s*(\d{1,3})", re.IGNORECASE)
TEMP = re.compile(r"(?:Temp|T)\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)", re.IGNORECASE)

# ---------- medications ----------
# For both progress sheet and drug chart
MED_LINE = re.compile(
    r"\b(?:TAB|TAB\.|CAP|CAP\.|INJ|INJ\.|INI|INI\.|SYP|SYRUP|GEL|OINT|MAB)[^\n]*",
    re.IGNORECASE,
)

DOSE = re.compile(r"\b\d+\s*(?:mg|mcg|ml|amp|cap|tab|gm|g|IU)?\b", re.IGNORECASE)
ROUTE = re.compile(r"\b(?:IV|IM|PO|PIO|P\/O|ORAL|TOPICAL)\b", re.IGNORECASE)
FREQ = re.compile(
    r"\b(OD|BD|TDS|TID|QID|QDS|HS|SOS|PRN|once\s*a\s*day|twice\s*a\s*day|thrice\s*a\s*day)\b",
    re.IGNORECASE,
)

FREQ_FUZZY = [
    ("oncea", "once a day"),
    ("once ", "once a day"),
    ("twicey", "twice a day"),
    ("twice ", "twice a day"),
    ("bd", "BD"),
    ("od", "OD"),
    ("tds", "TDS"),
    ("tid", "TID"),
]


def _dedup(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def extract_medications(text: str) -> List[Dict[str, str]]:
    meds = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if MED_LINE.search(line):
            name = MED_LINE.search(line).group().strip().rstrip(" :")
            dose = DOSE.search(line)
            route = ROUTE.search(line)
            freq = FREQ.search(line)

            freq_clean = ""
            if freq:
                freq_clean = freq.group()
            else:
                lc = line.lower().replace(" ", "")
                for bad, good in FREQ_FUZZY:
                    if bad in lc:
                        freq_clean = good

            meds.append(
                {
                    "name": name,
                    "dose": dose.group() if dose else "",
                    "route": route.group() if route else "",
                    "frequency": freq_clean,
                }
            )
    return meds


def extract_pii(text: str) -> Dict[str, List[str]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # --- Patient name (may be on next line) ---
    patient_names: List[str] = []
    for i, ln in enumerate(lines):
        m = PATIENT_NAME.search(ln)
        if m:
            val = m.group(1).strip()
            if not val and i + 1 < len(lines):
                val = lines[i + 1].strip()
            if val:
                patient_names.append(val)

    # Demographic IDs
    ipd_numbers = _dedup(IPD.findall(text))
    uhid_numbers = _dedup(UHID.findall(text))
    bed_numbers = _dedup(BED.findall(text))
    ages = AGE.findall(text)
    sex = SEX.findall(text)

    # Vitals
    bps = BP.findall(text)
    prs = PR.findall(text)
    rrs = RR.findall(text)
    temps = TEMP.findall(text)

    # Generic PII
    phones = PHONE.findall(text)
    emails = EMAIL.findall(text)
    dates = list(set([d if isinstance(d, str) else d[0] for d in DATE.findall(text)]))
    pans = PAN.findall(text)
    aadhaar = AADHAAR.findall(text)

    # Medications
    meds = extract_medications(text)

    return {
        "patient_names": _dedup(patient_names),
        "ages": ages,
        "sex": sex,
        "ipd_numbers": ipd_numbers,
        "uhid_numbers": uhid_numbers,
        "bed_numbers": bed_numbers,

        "blood_pressures": bps,
        "pulse_rates": prs,
        "respiratory_rates": rrs,
        "temperatures": temps,

        "phone_numbers": phones,
        "emails": emails,
        "dates": dates,
        "pan_numbers": pans,
        "aadhaar_numbers": aadhaar,

        "medications": meds,
    }
