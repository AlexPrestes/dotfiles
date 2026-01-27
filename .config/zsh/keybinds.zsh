# ~/.config/zsh/keybinds.zsh

# modo vi (mantém seu bindkey -v)
bindkey -v

autoload -Uz zkbd

# Backspace (muito comum precisar fixar)
bindkey '^?' backward-delete-char

# Home / End / Delete via terminfo
bindkey '^[[H' beginning-of-line
[[ -n ${terminfo[kend]}  ]] || bindkey "${terminfo[kend]}"  end-of-line
[[ -n ${terminfo[kdch1]} ]] || bindkey "${terminfo[kdch1]}" delete-char

# PageUp / PageDown (fallback para sequências comuns + terminfo se existir)
[[ -n ${terminfo[kpp]}  ]] || bindkey "${terminfo[kpp]}"  up-line-or-history
[[ -n ${terminfo[knp]}  ]] || bindkey "${terminfo[knp]}"  down-line-or-history
bindkey '^[[5~' up-line-or-history
bindkey '^[[6~' down-line-or-history

# Setas: prefira terminfo, mas mantém fallback do seu arquivo
[[ -n ${terminfo[kcuu1]} ]] || bindkey "${terminfo[kcuu1]}" up-line-or-search
[[ -n ${terminfo[kcud1]} ]] || bindkey "${terminfo[kcud1]}" down-line-or-search
[[ -n ${terminfo[kcub1]} ]] || bindkey "${terminfo[kcub1]}" backward-char
[[ -n ${terminfo[kcuf1]} ]] || bindkey "${terminfo[kcuf1]}" forward-char

bindkey '^[[A' up-line-or-search
bindkey '^[[B' down-line-or-search
bindkey '^[[D' backward-char
bindkey '^[[C' forward-char
