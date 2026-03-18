def decide(state, intensity, stress, energy, time):
    if stress > 7 and intensity > 4:
        return "grounding + breathing", "now"
    if energy < 3:
        return "rest", "within_15_min"
    if state in ["sad","anxious"]:
        return "journaling", "later_today"
    if energy > 7 and stress < 4:
        return "deep_work", "now"
    if time == "night":
        return "sleep routine", "tonight"
    return "light_planning", "later_today"