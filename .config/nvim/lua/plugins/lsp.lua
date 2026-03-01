return {
  -- basedpyright: substitui pyright com type checking básico
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        basedpyright = {
          settings = {
            basedpyright = {
              typeCheckingMode = "basic",
            },
          },
        },
      },
    },
  },
  -- ruff: formatter e linter via conform.nvim
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "ruff_format", "ruff_fix" },
      },
    },
  },
  -- treesitter parsers para Data Science / ML workflow
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      vim.list_extend(opts.ensure_installed, {
        "python", "sql", "lua", "markdown", "markdown_inline",
        "latex", "yaml", "dockerfile", "toml", "json", "bash",
      })
    end,
  },
}
