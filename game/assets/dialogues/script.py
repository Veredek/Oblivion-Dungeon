# ====== Script Class ======
class Script:
    def __init__(self):
        self.state = 0

    def script(self):
        return main_script[self.state]

# ====== Main Script ======
main_script = [
    "Você acorda em um lugar estranho e não se lembra de muita coisa, então não sabe se já esteve aqui antes...",
    "Atrás de você se encontra uma grande porta trancada, e a sua frente uma porta aberta.",
    "AFTER"
]