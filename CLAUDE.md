# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código neste repositório.

## Propósito do Repositório

Dotfiles pessoais para Linux com ambiente de desktop baseado em Qtile. As configurações ficam em `$HOME` via symlinks gerenciados pelo GNU Stow — **sempre usar `stow --adopt -t ~ .`** para criar ou atualizar links, nunca `ln -s` manual.

## Tecnologias Principais

- **Gerenciador de janelas**: Qtile (Python) — config em `.config/qtile/`
- **Shell**: ZSH com config modular em `.config/zsh/`
- **Editor**: Neovim (LazyVim) — config em `.config/nvim/`
- **Terminal**: Kitty — config em `.config/kitty/`
- **Prompt**: Starship — config em `.config/starship.toml`
- **Launcher**: Rofi — config em `.config/rofi/`

## Arquitetura

### Configuração do ZSH

O `.zshrc` na raiz carrega os arquivos modulares em `.config/zsh/` nesta ordem:

1. `env.zsh` — variáveis de ambiente, PATH (inclui `~/.local/bin`, CUDA, Android SDK, NVM, Claude CLI), configurações de histórico
2. `keybinds.zsh` — modo vi + correções de teclas do terminal (Home, End, Delete, Page Up/Down)
3. `aliases.zsh` — aliases e funções shell (`man` colorido, integração com `yazi`)
4. `completions.zsh` — configuração de completions do ZSH
5. `fzf.zsh` — integração com o FZF (fuzzy finder)
6. `prompt.zsh` — inicialização do Starship; prompt customizado para sessões SSH

### Configuração do Qtile

O `config.py` importa de arquivos modulares:

- `keys.py` — atalhos de teclado usando `mod4` (Super) como modificador principal
- `screens.py` — configuração de monitores e barra de status
- `groups.py` — grupos de workspaces
- `settings.py` — esquema de cores e variáveis globais
- `hooks.py` — hooks do ciclo de vida do WM
- `widgets/fortivpn.py` — widget customizado: clique esquerdo conecta (via rofi), clique direito desconecta; usa terminal para autenticação com PIN/TOTP
- `widgets/ollama.py` — widget de status do Ollama

### Neovim

Usa o template [LazyVim](https://www.lazyvim.org/). A config Lua está em `.config/nvim/lua/config/` (options, keymaps, autocmds) e `.config/nvim/lua/plugins/` (specs de plugins).

Plugins customizados em `lua/plugins/`:
- `lsp.lua` — basedpyright (typeCheckingMode=basic), ruff via conform.nvim, parsers treesitter
- `jupyter.lua` — molten.nvim + image.nvim (backend kitty) + jupytext.nvim
- `ai.lua` — codecompanion.nvim com adapter anthropic (claude-sonnet-4-20250514)
- `terminal.lua` — toggleterm.nvim (`<leader>tp` Python REPL horizontal, `<leader>tg` lazygit float)

LazyVim extras habilitados em `lazy.lua`:
`lang.python`, `lang.markdown`, `lang.docker`, `lang.yaml`, `lang.sql`, `lang.tex`

## Aplicando Mudanças

**Qtile**: Recarregar config com `Super+Ctrl+r`. Erros de sintaxe Python em `.config/qtile/` impedem o reload — verificar com:
```sh
python -m py_compile .config/qtile/config.py
```

**ZSH**: Recarregar o shell após mudanças:
```sh
source ~/.zshrc
```

**Plugins do Neovim**: Mudanças nos specs de plugins entram em vigor na próxima abertura; executar `:Lazy sync` dentro do nvim.

**Starship**: Mudanças em `starship.toml` entram em vigor em novas sessões do shell.

## Widgets Customizados do Qtile

Novos widgets vão em `.config/qtile/widgets/` e devem herdar de uma classe base do Qtile (tipicamente `base._TextBox` ou `base.InLoopPollText`). Importar em `screens.py`.

## Gitignore

Apenas `__pycache__/` e `*.pyc` são ignorados. Todos os outros arquivos do repositório são rastreados.
