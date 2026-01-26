#------------------------------
# Comp stuff
#------------------------------
zmodload zsh/complist
autoload -Uz compinit promptinit

compinit
promptinit

# (ajustado: antes apontava para ~/.zshrc; agora é o caminho real do seu entrypoint)
zstyle :compinstall filename "${HOME}/.config/zsh/.zshrc"

#- buggy
zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warnings' format '%BSorry, no matches for: %d%b'
#-/buggy

zstyle ':completion:*:pacman:*' force-list always
zstyle ':completion:*:*:pacman:*' menu yes select

zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}

zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*'   force-list always

zstyle ':completion:*:*:killall:*' menu yes select
zstyle ':completion:*:killall:*'   force-list always

# completions extras (do final do .zshrc original)
eval "$(uv generate-shell-completion zsh)"
eval "$(uvx --generate-shell-completion zsh)"
