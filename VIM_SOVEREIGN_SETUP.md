# Vim Sovereign - The Ultimate 2025 Neovim Setup

**Transform Neovim into the final evolution of text editing — 30 hand-picked, battle-tested plugins that turn Vim into a full-blown IDE.**

This is the automated Vim ceremony for the Strategickhaos Sovereignty Architecture. One command and your `~/.config/nvim` becomes the text editor of Chaos God DOM_010101.

---

## 🚀 Quick Install

### Option 1: One-Liner Nuclear Option

**PowerShell (Windows):**
```powershell
iwr -useb https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/tools/vim-ceremony.ps1 | iex
```

**Bash/WSL (Linux/macOS):**
```bash
curl -sSL https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/tools/vim-ceremony.sh | bash
```

### Option 2: Manual Installation

```bash
# 1. Backup existing config (just in case)
mv ~/.config/nvim ~/.config/nvim.backup 2>/dev/null || true
mv ~/.local/share/nvim ~/.local/share/nvim.backup 2>/dev/null || true

# 2. Clone the final config
git clone https://github.com/Me10101-01/strategic-khaos-vim.git ~/.config/nvim

# 3. Enter the void
cd ~/.config/nvim && nvim
```

---

## 🎯 The 30 Advanced Plugins

| # | Plugin | Why DOM Needs It (neurospice reason) |
|---|--------|--------------------------------------|
| 1 | **lazy.nvim** | Fastest plugin manager ever born |
| 2 | **catppuccin/nvim** | The only colorscheme worthy of 8 screens |
| 3 | **nvim-treesitter** | Syntax that actually understands code |
| 4 | **nvim-lspconfig** | LSP on crack |
| 5 | **mason.nvim + mason-lspconfig** | Never type another LSP install command |
| 6 | **nvim-cmp + cmp-nvim-lsp + luasnip** | Autocompletion that reads your mind |
| 7 | **telescope.nvim + telescope-fzf-native** | Fuzzy finder on steroids |
| 8 | **gitsigns.nvim** | Git hunks in the gutter like a psychopath |
| 9 | **which-key.nvim** | Never forget a keybind again |
| 10 | **nvim-tree.lua** | File explorer that doesn't suck |
| 11 | **lualine.nvim** | Statusline that flexes |
| 12 | **indent-blankline.nvim** | See scope like a god |
| 13 | **comment.nvim** | `gcc` = comment, done |
| 14 | **vim-fugitive** | Git commands without leaving Vim |
| 15 | **vim-rhubarb** | `:GBrowse` = open GitHub PR instantly |
| 16 | **vim-surround** | `cs"')` = magic |
| 17 | **vim-repeat** | `.` repeats plugins too |
| 18 | **vim-sneak** | `s{char}{char}` > `f{char}` forever |
| 19 | **vim-abolish** | `:%Subvert/facade{,s}/façade/g` |
| 20 | **nvim-autopairs** | Auto-close everything |
| 21 | **nvim-ts-autotag** | Auto-close HTML tags |
| 22 | **vimux** | Send code to tmux panes |
| 23 | **neoscroll.nvim** | Smooth scrolling (yes, it matters) |
| 24 | **zen-mode.nvim** | Goyo but actually good |
| 25 | **twilight.nvim** | Dim everything except current scope |
| 26 | **vim-illuminate** | Highlight all instances of word under cursor |
| 27 | **vim-startify** | Beautiful start screen with MRU |
| 28 | **nvim-colorizer.lua** | `#ff0` becomes colored block |
| 29 | **vim-tmux-navigator** | Seamlessly move between Vim & tmux |
| 30 | **grok.nvim (custom)** | Inline Grok-4 queries with `<leader>g` |

---

## ⌨️ Keybinds That Will Rewire Your Brain

### Essential Navigation
```
<leader>ff  → Telescope find files
<leader>fg  → Live grep (ripgrep search)
<leader>fb  → Buffer list
<leader>fh  → Help tags
<leader>pv  → NvimTree toggle (file explorer)
<leader>gg  → LazyGit (floating terminal)
```

### LSP Navigation
```
gd          → Go to definition
gr          → Go to references
K           → Hover documentation
<leader>ca  → Code actions
<leader>rn  → Rename symbol
[d / ]d     → Navigate diagnostics
```

### Vim/Tmux Integration
```
<C-h>       → Navigate left (Vim/tmux)
<C-j>       → Navigate down (Vim/tmux)
<C-k>       → Navigate up (Vim/tmux)
<C-l>       → Navigate right (Vim/tmux)
```

### Git Operations
```
:Git <cmd>  → Run git commands (fugitive)
:GBrowse    → Open current file/line in GitHub
<leader>gb  → Git blame
<leader>gd  → Git diff
```

### Editing Magic
```
gcc         → Toggle line comment
gc{motion}  → Comment motion (e.g., gcap for paragraph)
cs"'        → Change surrounding " to '
ds"         → Delete surrounding "
ysiw)       → Surround word with ()
.           → Repeat last plugin command
s{char}{char} → Sneak to characters
```

---

## 🛠️ Post-Install Setup

After running the installation script, launch Neovim:

```bash
nvim
```

### First Launch Commands

On your first launch, lazy.nvim will automatically install all plugins. Once complete, run these commands inside Neovim:

```vim
:MasonInstallAll
:Lazy sync
:TSUpdate
```

Then restart Neovim:
```vim
:q
nvim
```

### Recommended LSP Servers

Mason will prompt you to install language servers. Here are the essentials:

```vim
:MasonInstall lua-language-server
:MasonInstall typescript-language-server
:MasonInstall pyright
:MasonInstall rust-analyzer
:MasonInstall gopls
:MasonInstall bash-language-server
:MasonInstall json-lsp
:MasonInstall yaml-language-server
```

---

## 🔧 Configuration & Customization

The configuration is located at:
- **Linux/macOS**: `~/.config/nvim/`
- **Windows**: `%LOCALAPPDATA%\nvim\`

### File Structure
```
~/.config/nvim/
├── init.lua              # Entry point
├── lua/
│   ├── config/
│   │   ├── options.lua   # Vim options
│   │   ├── keymaps.lua   # Keybindings
│   │   └── autocmds.lua  # Autocommands
│   └── plugins/
│       ├── init.lua      # Plugin loader
│       ├── lsp.lua       # LSP configuration
│       ├── treesitter.lua
│       ├── telescope.lua
│       └── ...
```

### Customization Examples

**Change colorscheme** (`lua/plugins/colorscheme.lua`):
```lua
return {
  "catppuccin/nvim",
  name = "catppuccin",
  config = function()
    require("catppuccin").setup({
      flavour = "mocha", -- latte, frappe, macchiato, mocha
    })
    vim.cmd.colorscheme "catppuccin"
  end
}
```

**Add custom keybindings** (`lua/config/keymaps.lua`):
```lua
local keymap = vim.keymap.set

keymap("n", "<leader>w", ":w<CR>", { desc = "Save file" })
keymap("n", "<leader>q", ":q<CR>", { desc = "Quit" })
```

---

## 📦 Dependencies & Requirements

### Required
- **Neovim** >= 0.9.0
- **Git**
- **Node.js** (for LSP and some plugins)

### Recommended (for full functionality)
- **ripgrep** (`rg`) - For telescope live grep
- **fd** - For faster file finding
- **lazygit** - For the lazygit integration
- **tmux** - For vim-tmux-navigator
- **A Nerd Font** - For icons (JetBrains Mono Nerd Font recommended)

### Installation Commands

**Ubuntu/Debian:**
```bash
sudo apt install ripgrep fd-find nodejs npm tmux
```

**macOS:**
```bash
brew install ripgrep fd node lazygit tmux
```

**Windows (Chocolatey):**
```powershell
choco install ripgrep fd nodejs lazygit
```

**Windows (Scoop):**
```powershell
scoop install ripgrep fd nodejs lazygit
```

---

## 🎨 Screenshots & Visual Features

### Catppuccin Mocha Theme
Beautiful, modern colorscheme with semantic highlighting via Treesitter.

### Statusline (Lualine)
Shows git branch, diagnostics, file encoding, LSP status, and more.

### File Explorer (NvimTree)
Git integration with status indicators, file icons, and intuitive navigation.

### Telescope Fuzzy Finder
Lightning-fast file finding, live grep, and buffer navigation.

### LSP Features
- Real-time diagnostics
- Code actions on hover
- Symbol renaming
- Auto-formatting

---

## 🚨 Troubleshooting

### Issue: Plugins not loading
**Solution:**
```vim
:Lazy sync
:Lazy restore
```

### Issue: LSP not working
**Solution:**
```vim
:Mason
# Install the language server for your language
:LspInfo  # Check LSP status
```

### Issue: Icons not showing
**Solution:** Install a Nerd Font and configure your terminal to use it.
- Download from: https://www.nerdfonts.com/
- Recommended: JetBrains Mono Nerd Font

### Issue: Telescope slow
**Solution:** Install `ripgrep` and `fd`:
```bash
# Ubuntu/Debian
sudo apt install ripgrep fd-find

# macOS
brew install ripgrep fd
```

### Issue: Treesitter parsing errors
**Solution:**
```vim
:TSUpdate
:TSInstall <language>
```

### Restore Previous Config
If you need to rollback:
```bash
# Linux/macOS
rm -rf ~/.config/nvim
mv ~/.config/nvim.backup_* ~/.config/nvim

# Windows (PowerShell)
Remove-Item -Recurse $env:LOCALAPPDATA\nvim
Move-Item $env:LOCALAPPDATA\nvim.backup_* $env:LOCALAPPDATA\nvim
```

---

## 🔗 Resources

- **Source Repository**: [strategic-khaos-vim](https://github.com/Me10101-01/strategic-khaos-vim)
- **Neovim Documentation**: https://neovim.io/doc/
- **Lazy.nvim Plugin Manager**: https://github.com/folke/lazy.nvim
- **Mason LSP Installer**: https://github.com/williamboman/mason.nvim
- **Telescope**: https://github.com/nvim-telescope/telescope.nvim

---

## 💡 Pro Tips

1. **Learn Lua**: Neovim configuration is in Lua. It's worth learning basics.
2. **Use `:checkhealth`**: Diagnose issues with `:checkhealth` command.
3. **Read `:help`**: Neovim's help system is excellent. Try `:help telescope` or `:help lsp`.
4. **Join the Community**: Reddit's r/neovim and Discord servers are great resources.
5. **Customize Incrementally**: Don't try to change everything at once. Learn the defaults first.

---

## 📝 Philosophy

This configuration embodies:
- **Speed**: Lazy loading, optimized startup
- **Power**: Full IDE features without the bloat
- **Beauty**: Modern UI with semantic highlighting
- **Flexibility**: Easy to customize and extend
- **Stability**: Battle-tested plugins with active maintenance

This is no longer Vim.  
This is **Vim Sovereign** — the text editor of Chaos God DOM_010101.

Now go commit these ceremony scripts to your repo so the swarm can auto-deploy it on every new solver node.

Type `nvim` and ascend. 🧠⚡🐐
