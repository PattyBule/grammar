from app.api.schemas import RewriteRequest, RewriteOption


class RewriteService:
    def process(self, request: RewriteRequest):
        original = request.text.strip()
        corrected = self._correct_common_errors(original)

        tone = self._analyze_tone(original)

        options = [
            RewriteOption(
                style="neutral",
                text=self._neutral_version(original),
                explanation="Keeps the message clear and direct while remaining natural.",
            ),
            RewriteOption(
                style="natural",
                text=self._natural_version(original),
                explanation="This version sounds more like everyday natural English.",
            ),
            RewriteOption(
                style="polite",
                text=self._polite_version(original),
                explanation="This version softens the request and makes it more respectful.",
            ),
            RewriteOption(
                style="formal",
                text=self._formal_version(original),
                explanation="Suitable for work communication and formal emails.",
            ),
        ]

        return {
            "original_text": original,
            "corrected_text": corrected,
            "tone_analysis": tone,
            "rewrite_options": [option.model_dump() for option in options],
            "summary": "The sentence was checked for grammar and rewritten in a more natural and socially polite style.",
        }

    def _correct_common_errors(self, text: str) -> str:
        corrected = text
        replacements = {
            "He go": "He goes",
            "he go": "he goes",
            "I am go": "I am going",
            "she don't": "she doesn't",
            "a apple": "an apple",
            "many informations": "much information",
            "I am agree": "I agree",
        }
        for source, target in replacements.items():
            if source in corrected.lower():
                corrected = corrected.replace(source, target)
        corrected = corrected.strip()
        if corrected and corrected[-1] not in ".!?":
            corrected += "."
        return corrected

    def _analyze_tone(self, text: str):
        normalized = text.lower()
        if "please" in normalized or "could you" in normalized or "would you" in normalized:
            tone = "polite"
            reasons = ["The sentence uses a polite request structure."]
            intensity = 0.35
        elif "now" in normalized or "immediately" in normalized or "must" in normalized:
            tone = "direct"
            reasons = ["The sentence sounds urgent or demanding."]
            intensity = 0.9
        elif "sorry" in normalized or "thank you" in normalized:
            tone = "friendly"
            reasons = ["The sentence is gentle and warm in tone."]
            intensity = 0.4
        else:
            tone = "neutral"
            reasons = ["The sentence is neutral and factual."]
            intensity = 0.5
        return {
            "tone": tone,
            "intensity": intensity,
            "confidence": 0.9,
            "reasons": reasons,
        }

    def _neutral_version(self, text: str) -> str:
        if "need" in text.lower() and "now" in text.lower():
            return "I need this as soon as possible."
        if "you forgot" in text.lower():
            return "I think I may have missed your message."
        return text

    def _natural_version(self, text: str) -> str:
        if "need" in text.lower() and "now" in text.lower():
            return "Could you help me with this as soon as possible?"
        if "you forgot" in text.lower():
            return "I think I may have missed your message. Could you send it again?"
        return text

    def _polite_version(self, text: str) -> str:
        if "need" in text.lower() and "now" in text.lower():
            return "Could you please take care of this for me as soon as possible?"
        if "you forgot" in text.lower():
            return "Sorry, I may have missed your message. Could you please send it again?"
        return "Could you please help me with this?"

    def _formal_version(self, text: str) -> str:
        if "need" in text.lower() and "now" in text.lower():
            return "I would appreciate it if you could take care of this as soon as possible."
        if "you forgot" in text.lower():
            return "I believe I may have missed your message. Could you kindly send it again?"
        return "I would appreciate your assistance with this matter."
