from typing import Dict, List


class ToneService:
    def analyze(self, text: str) -> Dict:
        normalized = text.lower()

        reasons: List[str] = []

        if any(word in normalized for word in ["please", "could you", "would you", "can you", "i would appreciate", "kindly"]):
            tone = "polite"
            reasons.append("The sentence uses a polite request form.")
        elif any(word in normalized for word in ["must", "need this now", "do this now", "immediately", "right now", "asap", "urgent"]):
            tone = "direct"
            reasons.append("The sentence sounds urgent or commanding.")
        elif any(word in normalized for word in ["sorry", "thank you", "thanks", "could", "would", "help me"]):
            tone = "friendly"
            reasons.append("The sentence is soft and warm.")
        else:
            tone = "neutral"
            reasons.append("The sentence is neutral in tone.")

        intensity = 0.9 if tone == "direct" else 0.5 if tone == "neutral" else 0.3
        confidence = 0.9 if reasons else 0.7

        return {
            "tone": tone,
            "intensity": intensity,
            "confidence": confidence,
            "reasons": reasons,
        }
