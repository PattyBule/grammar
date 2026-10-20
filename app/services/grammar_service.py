import re
from typing import Dict, List, Tuple


class GrammarService:
    def __init__(self):
        self.ordered_patterns = [
            ("me need", "I need"),
            ("me want", "I want"),
            ("me am", "I am"),
            ("i am go", "I am going"),
            ("he go", "he goes"),
            ("she go", "she goes"),
            ("they go", "they go"),
            ("you forgot", "you forgot"),
            ("why you not", "why didn't you"),
            ("why you no", "why didn't you"),
            ("i am agree", "I agree"),
            ("i need you to do this now", "Could you please take care of this for me as soon as possible?"),
            ("this file wrong", "this file is wrong"),
            ("this wrong", "this is wrong"),
            ("a apple", "an apple"),
            ("many informations", "much information"),
            ("can to go", "can go"),
            ("send me file", "please send me the file"),
            ("send file now", "please send the file now"),
            ("why you not send", "why didn't you send"),
            ("me need file", "I need the file"),
        ]

    def check_and_correct(self, text: str):
        raw = text.strip()
        normalized = self.normalize_spacing(raw)
        repaired = self.repair_word_order(normalized)
        corrected = self.apply_rule_fixes(repaired)
        corrected = self.fix_common_grammar(corrected)
        corrected = self.fix_sentence_end(corrected)

        issues = self.detect_issues(raw, corrected)
        return {
            "corrected_text": corrected,
            "issues": issues,
        }

    def normalize_spacing(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("  ", " ")
        return text

    def repair_word_order(self, text: str) -> str:
        lower = text.lower()
        replacements = {
            "me need": "I need",
            "me want": "I want",
            "me am": "I am",
            "why you not": "why didn't you",
            "why you no": "why didn't you",
            "this file wrong": "this file is wrong",
            "this wrong": "this is wrong",
            "send me file": "please send me the file",
            "send file now": "please send the file now",
            "file me": "me file",
            "me file": "my file",
            "i need this now": "I need this as soon as possible",
        }

        for source, target in replacements.items():
            if source in lower:
                text = re.sub(rf"\b{re.escape(source)}\b", target, text, flags=re.IGNORECASE)
        return text

    def apply_rule_fixes(self, text: str) -> str:
        corrected = text
        for source, target in self.ordered_patterns:
            corrected = re.sub(rf"\b{re.escape(source)}\b", target, corrected, flags=re.IGNORECASE)
        corrected = corrected.replace("  ", " ").strip()
        return corrected

    def fix_common_grammar(self, text: str) -> str:
        replacements = {
            "dont": "don't",
            "dont ": "don't ",
            "i need you to do this now": "Could you please take care of this for me as soon as possible?",
            "i am agree": "I agree",
            "he go": "he goes",
            "she go": "she goes",
            "there is two": "there are two",
            "this is wrong": "this is wrong",
            "a apple": "an apple",
            "many informations": "much information",
            "I am go": "I am going",
            "i am go": "I am going",
            "why didnt you": "why didn't you",
        }
        for source, target in replacements.items():
            text = re.sub(rf"\b{re.escape(source)}\b", target, text, flags=re.IGNORECASE)
        return text

    def fix_sentence_end(self, text: str) -> str:
        if not text:
            return text
        text = text.strip()
        if text and text[-1] not in ".!?":
            text += "."
        return text

    def detect_issues(self, raw: str, corrected: str):
        issues = []
        raw_lower = raw.lower()
        corrected_lower = corrected.lower()

        if "me " in raw_lower:
            issues.append({
                "issue_type": "word_order",
                "original_text": "me",
                "suggestion": "I",
                "explanation": "Pronouns in subject position should usually be in nominative form, for example 'I' not 'me'.",
                "severity": "high",
            })

        if "why you not" in raw_lower or "why you no" in raw_lower:
            issues.append({
                "issue_type": "word_order",
                "original_text": "why you not",
                "suggestion": "why didn't you",
                "explanation": "Questions in English usually use auxiliary verbs like 'did' in this structure.",
                "severity": "high",
            })

        if raw_lower != corrected_lower:
            issues.append({
                "issue_type": "sentence_reconstruction",
                "original_text": raw,
                "suggestion": corrected,
                "explanation": "The sentence structure has been reorganized to better match natural English word order.",
                "severity": "medium",
            })

        return issues
