import os


terminal = "kitty"
terminal_gpu = f"exec {terminal} --env GPU_MODE=1 -- zsh -c 'prime-run zsh --login'"
browser = os.environ.get("BROWSER", "firefox")
home = os.path.expanduser("~")

mod = "mod4"

MYCOLORS = [
    "#232323",
    "#ff000f",
    "#8ce10b",
    "#ffb900",
    "#008df8",
    "#6d43a6",
    "#00d8eb",
    "#ffffff",
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]
