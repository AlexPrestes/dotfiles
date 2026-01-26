return {
  {
    "navarasu/onedark.nvim",
    lazy = false, -- Carregar imediatamente
    priority = 1000, -- Prioridade máxima para evitar conflitos
    config = function()
      require("onedark").setup({
        style = "warmer", -- Estilo "warmer" (mais quente)
      })
      vim.cmd.colorscheme("onedark") -- Definir como tema padrão
    end,
  },
}
