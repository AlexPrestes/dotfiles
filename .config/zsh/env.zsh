#------------------------------------------------------------------#
# File:     env.zsh (derivado do .zshrc original)
#------------------------------------------------------------------#

#-----------------------------
# Source some stuff
#-----------------------------
if [[ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  . /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

BASE16_SHELL="$HOME/.config/base16-shell/base16-default.dark.sh"
[[ -s $BASE16_SHELL ]] && source $BASE16_SHELL

#source $HOME/intel/oneapi/compiler/latest/env/vars.sh

#------------------------------
# History stuff
#------------------------------
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000

#------------------------------
# Variables
#------------------------------
export BROWSER="firefox"
export EDITOR="nvim"
export VISUAL="nvim"
export VI="nvim"
export RANGER_DEVICONS_SEPARATOR=" "
export LESS='-R --use-color -Dd+r$Du+b$'
export MANPAGER="less -R --use-color -Dd+r -Du+b"
export MANROFFOPT="-P -c"
export QT_QPA_PLATFORMTHEME=qt5ct
export TCLLIBPATH="/usr/lib/tcl8.6:/usr/lib/tk8.6"
export ANDROID_SDK_ROOT="/opt/android-sdk"

export PATH="$PATH:$HOME/bin:$HOME/.local/bin:$HOME/.dotnet/tools:/opt/prismlaucher:/opt/PokeMMO:$ANDROID_SDK_ROOT/platform-tools:/opt/cuda/bin"
export PATH="$PATH:$HOME/.claude/bin"

export LD_LIBRARY_PATH=/opt/cuda/lib64:$LD_LIBRARY_PATH

export OLLAMA_GPU_OVERHEAD=512


#-----------------------------
# Dircolors
#-----------------------------
LS_COLORS='rs=0:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:tw=30;42:ow=34;42:st=37;44:ex=01;32:';
export LS_COLORS

#------------------------------
# Comp path extras
#------------------------------
fpath+=~/.zfunc

#------------------------------
# NVM
#------------------------------
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
