return {
  {
    "olimorris/codecompanion.nvim",
    opts = {
      adapters = {
        anthropic = function()
          return require("codecompanion.adapters").extend("anthropic", {
            schema = { model = { default = "claude-sonnet-4-20250514" } },
          })
        end,
      },
      strategies = {
        chat = { adapter = "anthropic" },
        inline = { adapter = "anthropic" },
      },
    },
  },
}
