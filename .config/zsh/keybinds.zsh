# ~/.config/zsh/keybinds.zsh

# modo vi (mantém seu bindkey -v)
bindkey -v

autoload -Uz zkbd

# Backspace (muito comum precisar fixar)
bindkey '^?' backward-delete-char

# --- Atalhos de Teclado (Bindkeys) ---
# Home e End
bindkey "^[[H" beginning-of-line
bindkey "^[[F" end-of-line

# Del (Delete)
bindkey "^[[3~" delete-char

# Page Up e Page Down (Navegar no histórico)
bindkey "^[[5~" up-line-or-history
bindkey "^[[6~" down-line-or-history

bindkey '^[[A' up-line-or-search
bindkey '^[[B' down-line-or-search
bindkey '^[[D' backward-char
bindkey '^[[C' forward-char
