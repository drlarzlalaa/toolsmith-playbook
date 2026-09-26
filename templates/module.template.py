"""{{description}}"""

__all__ = ["check", "Finding", "SEVERITY"]

SEVERITY = {"low": 1, "medium": 2, "high": 3}


class Finding:
    def __init__(self, severity, code, message):
        self.severity, self.code, self.message = severity, code, message

    def __str__(self):
        return "[%s] %s: %s" % (self.severity.upper(), self.code, self.message)

    def as_dict(self):
        return dict(severity=self.severity, code=self.code, message=self.message)


def check(text):
    """Return a list of Finding for the given text. TODO: replace this example rule."""
    findings = []
    if "TODO" in text:
        findings.append(Finding("low", "EXAMPLE", "the text contains the word TODO"))
    return findings
