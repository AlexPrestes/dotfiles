-- ~/.config/nvim/lua/plugins/lsp.lua
return {
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
    },
    config = function()
      -- Configuração do Mason (gerenciador de LSPs)
      require("mason").setup()
      require("mason-lspconfig").setup({
        ensure_installed = { "pyright" }, -- Lista de LSPs para instalar automaticamente
      })

      -- Configuração do Pyright
      local lspconfig = require("lspconfig")
      local util = require("lspconfig/util")

      lspconfig.pyright.setup({
        on_attach = function(client, bufnr)
          -- Atalhos específicos para Python (opcional)
          local opts = { buffer = bufnr }
          vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
          vim.keymap.set("n", "K", vim.lsp.buf.hover, opts)
          vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts)
        end,
        settings = {
          pyright = {
            -- Configurações específicas do Pyright (opcional)
            analysis = {
              typeCheckingMode = "off", -- Pode ser "basic", "strict" ou "off"
              autoSearchPaths = true,
              useLibraryCodeForTypes = true,
              diagnosticMode = "workspace",
            },
            python = {
              pythonPath = ".venv/bin/python",
              venvPath = ".",
            },
          },
        },
      })
    end,
  },
}
