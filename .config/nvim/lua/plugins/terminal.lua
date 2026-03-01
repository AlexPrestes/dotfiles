return {
  {
    "akinsho/toggleterm.nvim",
    opts = {
      direction = "horizontal",
      size = 15,
    },
    keys = {
      { "<leader>tp", "<cmd>ToggleTerm direction=horizontal<cr>",
        desc = "Python REPL (horizontal)" },
      { "<leader>tg",
        function()
          local Terminal = require("toggleterm.terminal").Terminal
          Terminal:new({ cmd = "lazygit", direction = "float",
            hidden = true }):toggle()
        end,
        desc = "Lazygit (float)" },
    },
  },
}
