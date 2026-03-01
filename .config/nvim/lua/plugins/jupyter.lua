return {
  -- image.nvim: renderização de imagens no Kitty
  {
    "3rd/image.nvim",
    opts = {
      backend = "kitty",
    },
  },
  -- molten.nvim: execução de notebooks Jupyter inline
  {
    "benlubas/molten-nvim",
    build = ":UpdateRemotePlugins",
    init = function()
      vim.g.molten_image_provider = "image.nvim"
      vim.g.molten_output_win_max_height = 20
    end,
  },
  -- jupytext.nvim: converte .ipynb <-> .py percent format
  {
    "GCBallesteros/jupytext.nvim",
    opts = {
      style = "percent",
      output_extension = "auto",
      force_ft = nil,
    },
  },
}
