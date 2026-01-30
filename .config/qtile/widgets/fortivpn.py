import subprocess
from libqtile.widget import base

class FortiVPNWidget(base.BackgroundPoll):
    """
    Widget simples para FortiVPN (fortivpn).
    Mostra 'VPN [off]' ou 'VPN [nome]'.
    Clique esquerdo: escolher perfil (rofi) e conectar (abre terminal para senha/TOTP)
    Clique direito: desconectar
    """

    defaults = [
        ("update_interval", 3, "Tempo entre atualizações (s)"),
        ("active_color", "#00ff88", "Cor quando conectado"),
        ("inactive_color", "#ff5555", "Cor quando desconectado"),
        ("rofi_prompt", "VPN", "Prompt do rofi"),
        ("default_user", "", "Usuário padrão (opcional)"),
        ("terminal_cmd", ["kitty", "-e"], "Comando do terminal para rodar fortivpn connect"),
    ]

    def __init__(self, **config):
        super().__init__("", markup=True, **config)
        self.add_defaults(FortiVPNWidget.defaults)

        self.add_callbacks({
            "Button1": self.select_and_connect,
            "Button3": self.disconnect,
        })

        self.text = self.poll()

    # ---------- helpers ----------
    def _run(self, cmd):
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(errors="replace")

    def _popen_quiet(self, cmd):
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    # ---------- status ----------
    def poll(self):
        try:
            out = self._run(["fortivpn", "status"])
            # Esperado: "Status: Connected" / "Status: Disconnected"
            if "Connected" in out:
                name = self._connected_name(out) or "on"
                return f"<span color='{self.active_color}'>VPN [{name}]</span>"
            return f"<span color='{self.inactive_color}'>VPN [off]</span>"
        except Exception:
            return f"<span color='{self.inactive_color}'>VPN [err]</span>"

    def _connected_name(self, status_output):
        # Se o fortivpn status não trouxer nome, retorna None.
        # Mantém simples: tenta extrair algo após "Connected" se existir.
        # Caso não exista, o widget mostra "on".
        for line in status_output.splitlines():
            if "Connected" in line:
                # exemplos possíveis (depende da versão): "Status: Connected" ou "Connected: <vpn>"
                parts = line.split()
                if len(parts) >= 3:
                    # última palavra pode ser o nome (heurística)
                    maybe = parts[-1].strip()
                    if maybe.lower() not in ("connected", "status:", "status"):
                        return maybe
        return None

    # ---------- list + rofi ----------
    def _list_vpns(self):
        out = self._run(["fortivpn", "list"])
        vpns = []
        for line in out.splitlines():
            s = line.strip()
            # seu exemplo: "obra-vpn"
            if s and not s.endswith(":") and not s.lower().startswith(("vpns", "personal", "enterprise")):
                # pega apenas entradas indentadas (normalmente 4 espaços)
                if line.startswith("    ") or line.startswith("\t"):
                    vpns.append(s)
        return vpns

    def _rofi_select(self, options):
        rofi = subprocess.run(
            ["rofi", "-dmenu", "-p", self.rofi_prompt],
            input=("\n".join(options)).encode(),
            stdout=subprocess.PIPE
        )
        return rofi.stdout.decode().strip()

    # ---------- actions ----------
    def select_and_connect(self):
        try:
            vpns = self._list_vpns()
            if not vpns:
                self.text = f"<span color='{self.inactive_color}'>VPN [none]</span>"
                self.bar.draw()
                return

            choice = self._rofi_select(vpns)
            if not choice:
                return

            self.connect(choice)

        except Exception as e:
            self.text = f"<span color='{self.inactive_color}'>VPN [err]</span>"
            self.bar.draw()

    def connect(self, vpn_name):
        # Abre terminal para permitir prompt de senha (PIN+TOTP)
        # Usa -u se default_user estiver definido; usa -p para prompt.
        cmd = ["fortivpn", "connect", vpn_name]
        if self.default_user:
            cmd += ["-u", self.default_user]
        cmd += ["-p"]

        self._popen_quiet(self.terminal_cmd + cmd)
        self._refresh()

    def disconnect(self):
        try:
            self._popen_quiet(["fortivpn", "disconnect"])
        except Exception:
            pass
        self._refresh()

    def _refresh(self):
        self.text = self.poll()
        self.bar.draw()

