from typing import List

from app.api.schemas import GrammarIssue


class GrammarService:
    def check_and_correct(self, text: str):
        issues: List[GrammarIssue] = []
        corrected = text

        patterns = [
            ("I am go", "I am going", "grammar", "Verb form should match the present continuous tense.", "medium"),
            ("He go", "He goes", "grammar", "Third-person singular subjects need the -s form in the present tense.", "high"),
            ("she don't", "she doesn't", "grammar", "Use the correct present-tense form for third-person singular subjects.", "high"),
            ("a apple", "an apple", "article", "Use 'an' before a vowel sound.", "medium"),
            ("many informations", "much information", "word_choice", "Use 'information' as an uncountable noun.", "medium"),
            ("I can to go", "I can go", "grammar", "The infinitive is not used after 'can'.", "medium"),
            ("I am agree", "I agree", "grammar", "'Agree' is usually used directly without 'am'.", "medium"),
        ]

        lower_text = text.lower()
        for original, replacement, issue_type, explanation, severity in patterns:
            if original in lower_text:
                corrected = corrected.replace(original, replacement)
                issues.append(
                    GrammarIssue(
                        issue_type=issue_type,
                        original_text=original,
                        suggestion=replacement,
                        explanation=explanation,
                        severity=severity,
                    )
                )

        # Additional common fixes
        corrected = corrected.replace(" dont ", " doesn't ")
        corrected = corrected.replace(" do not ", " do not ")
        corrected = corrected.replace(" i need you to do this now ", " Could you please take care of this for me as soon as possible? ")

        # Fix common punctuation/spacing drift
        corrected = corrected.strip()
        if corrected and corrected[-1] not in ".!?":
            corrected += "."

        return {
            "corrected_text": corrected,
            "issues": issues,
        }
