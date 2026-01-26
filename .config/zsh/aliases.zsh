#------------------------------
# Alias Color
#------------------------------
alias ls='ls --color=auto -Fh'
alias diff='diff --color=auto'
alias grep='grep --color=auto'
alias ip='ip -color=auto'
alias dmesg='dmesg --color=always'

#------------------------------
# Alias Stuff
#------------------------------
#alias g++="g++ -std=c++11 -Wall -Wextra -Wpedantic -O2 -lcunit $(pkg-config --cflags --libs opencv4)"
alias ncdu="ncdu --color dark"
alias mpic++="mpic++ -std=c++17 -Wall -Wextra -Wpedantic"
alias gfortran="gfortran -Wall -Wextra -Wpedantic"
alias R="R --quiet"
alias xclip="xclip -sel clip"
alias cp='rsync -ah --progress'
alias ipy='ipython --no-confirm-exit'
alias jpy='jupyter-lab -y'

#------------------------------
# ShellFuncs
#------------------------------
# -- coloured manuals
man() {
  env \
    LESS_TERMCAP_mb=$(printf "\e[1;31m") \
    LESS_TERMCAP_md=$(printf "\e[1;31m") \
    LESS_TERMCAP_me=$(printf "\e[0m") \
    LESS_TERMCAP_se=$(printf "\e[0m") \
    LESS_TERMCAP_so=$(printf "\e[1;44;33m") \
    LESS_TERMCAP_ue=$(printf "\e[0m") \
    LESS_TERMCAP_us=$(printf "\e[1;32m") \
    man "$@"
}

function y() {
  local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
  yazi "$@" --cwd-file="$tmp"
  if cwd="$(command cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
    builtin cd -- "$cwd"
  fi
  rm -f -- "$tmp"
}
