import subprocess
from libqtile.widget import base

class OllamaWidget(base.BackgroundPoll):
    """
    Widget simples para monitorar e controlar o Ollama.
    Mostra 'Ollama [off]' ou 'Ollama [modelo]' com cor configurável.
    Clique esquerdo: escolher modelo (rofi)
    Clique direito: parar todos
    """

    defaults = [
        ("update_interval", 5, "Tempo entre atualizações (s)"),
        ("active_color", "#00ff88", "Cor quando ativo"),
        ("inactive_color", "#ff5555", "Cor quando parado"),
        ("text_color", (255, 255, 255), "Cor RGB do texto base"),
    ]

    def __init__(self, **config):
        # Ativa suporte a tags <span color="">
        super().__init__("", markup=True, **config)
        self.add_defaults(OllamaWidget.defaults)

        self.add_callbacks({
            "Button1": self.select_model,  # esquerdo: escolhe modelo
            "Button3": self.stop_all       # direito: para tudo
        })

        self.text = self.poll()

    def rgb_to_hex(self, rgb):
        """Converte (R, G, B) → #rrggbb"""
        if isinstance(rgb, tuple):
            return "#{:02x}{:02x}{:02x}".format(*rgb)
        return rgb

    def poll(self):
        """Atualiza o texto do widget"""
        if self.is_running():
            model = self.get_running_model()
            color = self.active_color
            return f"<span color='{color}'>Ollama [{model}]</span>"
        else:
            color = self.inactive_color
            return f"<span color='{color}'>Ollama [off]</span>"

    def is_running(self):
        """Verifica se há algum modelo rodando"""
        try:
            out = subprocess.check_output(["ollama", "ps"]).decode().strip().splitlines()
            return len(out) > 1
        except Exception:
            return False

    def get_running_model(self):
        """Retorna o nome do modelo atual"""
        try:
            out = subprocess.check_output(["ollama", "ps"]).decode().strip().splitlines()
            if len(out) > 1:
                return out[1].split()[0]
        except Exception:
            pass
        return "off"

    def select_model(self):
        """Abre o rofi para escolher o modelo"""
        try:
            output = subprocess.check_output(["ollama", "list"]).decode().strip().splitlines()
            models = [line.split()[0] for line in output[1:] if line]
            if not models:
                self.text = "<span color='#ff5555'>Nenhum modelo encontrado</span>"
                self.bar.draw()
                return

            rofi = subprocess.run(
                ["rofi", "-dmenu", "-p", "Escolha modelo Ollama"],
                input="\n".join(models).encode(),
                stdout=subprocess.PIPE
            )
            model_choice = rofi.stdout.decode().strip()

            if model_choice:
                self.load_model(model_choice)

        except Exception as e:
            self.text = f"<span color='#ff5555'>Erro: {e}</span>"
            self.bar.draw()

    def load_model(self, model_name):
        """Carrega modelo com `ollama run`"""
        try:
            # Para modelo anterior, se existir
            current_model = self.get_running_model()
            if current_model != "off":
                subprocess.run(
                    ["ollama", "stop", current_model],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

            # Inicia novo modelo
            subprocess.Popen(
                ["ollama", "run", model_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except Exception as e:
            self.text = f"<span color='{self.inactive_color}'>Erro: {e}</span>"
            self.bar.draw()

    def stop_all(self):
        """Para todos os modelos rodando"""
        try:
            output = subprocess.check_output(["ollama", "ps"]).decode().strip().splitlines()
            running_models = [line.split()[0] for line in output[1:] if line]
            for model in running_models:
                subprocess.run(
                    ["ollama", "stop", model],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
        except Exception as e:
            self.text = f"<span color='{self.inactive_color}'>Erro: {e}</span>"
            self.bar.draw()

    def _refresh(self):
        """Atualiza o texto da barra"""
        self.text = self.poll()
        self.bar.draw()

