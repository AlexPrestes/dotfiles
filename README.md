# dotfiles

Configurações pessoais para ambiente Linux com Qtile.

## Dependências

- [GNU Stow](https://www.gnu.org/software/stow/)

## Instalação

Clone o repositório diretamente em `$HOME`:

```sh
git clone git@github.com:arexprestes/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

Use o `stow` com a flag `--adopt` para criar os symlinks. O `--adopt` move arquivos já existentes no sistema para dentro do repositório antes de criar os links — útil para absorver configs que ainda não estão versionadas:

```sh
stow --adopt -t ~ .
```

> **Atenção:** o `--adopt` sobrescreve os arquivos do repositório com as versões locais. Se houver divergência, revise com `git diff` após rodar o comando e descarte o que não quiser manter.

## Estrutura

```
~/dotfiles/
├── .config/
│   ├── qtile/       # Gerenciador de janelas (Python)
│   ├── zsh/         # Configuração modular do ZSH
│   ├── nvim/        # Neovim (LazyVim)
│   ├── kitty/       # Terminal
│   ├── rofi/        # Launcher
│   └── starship.toml
├── .local/bin/      # Scripts utilitários e statusbar
├── .zshrc
└── .Xresources
```
