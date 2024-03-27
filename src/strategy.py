class Indicator:
    def __init__(self, kind, var) -> None:
        self.kind = kind
        self.var = var
        self.id = f"{self.kind}_{self.var}"

    
    def __str__(self) -> str:
        return self.id

class Trigger:
    def __init__(self, id) -> None:
        self.id = id
        self.indicators = self._get_indicators(self.id)
    
    def _get_indicators(self, id):
        splut = self.id.split("__")
        a = splut[0].split(":")[0]
        a_val = int(splut[0].split(":")[1])
        result = [Indicator(a, a_val)]
        mid = splut[1].split(":")[0]
        if mid in ("x", ">", "<"):
            b = splut[-1].split(":")[0]
            b_val = int(splut[-1].split(":")[1])
            result.append(Indicator(b, b_val))
        return result
    
    def __str__(self) -> str:
        return f"{self.id}"

class TriggerGroup:
    def __init__(self, triggers) -> None:
        self.triggers = [Trigger(id) for id in triggers]
    

class Strategy:
    def __init__(self, trigger_groups) -> None:
        self.trigger_groups = [TriggerGroup(tg) for tg in trigger_groups]

    def run(self, date):
        pass

