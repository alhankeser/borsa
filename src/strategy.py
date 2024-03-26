class Indicator:
    def __init__(self, kind, var) -> None:
        self.kind = kind
        self.var = var
    
    def __str__(self) -> str:
        return f"{self.kind} {self.var}"

class Trigger:
    def __init__(self, name) -> None:
        self.name = name
        self.indicators = self._get_indicators(self.name)
    
    def _get_indicators(self, name):
        splut = self.name.split("__")
        a = splut[0].split(":")[0]
        a_val = int(splut[0].split(":")[1])
        result = [Indicator(a, a_val)]
        mid = splut[1].split(":")[0]
        if mid in ("cross", "comp"):
            b = splut[2].split(":")[0]
            b_val = int(splut[2].split(":")[1])
            result.append(Indicator(b, b_val))
        return result

class TriggerGroup:
    def __init__(self, triggers) -> None:
        self.triggers = [Trigger(t) for t in triggers]
    

class Strategy:
    def __init__(self, trigger_groups) -> None:
        self.trigger_groups = [TriggerGroup(tg) for tg in trigger_groups]

    

