#!/bin/bash

user=flypatriot
target_dir=/home/$user
omzsh_dir=$target_dir/.oh-my-zsh
custom_dir=$omzsh_dir/custom
plugins_dir=$custom_dir/plugins
themes_dir=$custom_dir/themes
fonts_dir=$target_dir/.local/share/fonts


# Installing oh-my-zsh

if [ ! -d $target_dir/.oh-my-zsh ]; then
    git clone --depth=1 git://github.com/robbyrussell/oh-my-zsh.git $target_dir/.oh-my-zsh
fi

# Installing plugins
autosuggestions=(zsh-autosuggestions https://github.com/zsh-users/zsh-autosuggestions.git)
syntax_highlighting=(zsh-syntax-highlighting https://github.com/zsh-users/zsh-syntax-highlighting.git)
completions=(zsh-completions https://github.com/zsh-users/zsh-completions.git)
history_substring_search=(zsh-history-substring-search https://github.com/zsh-users/zsh-history-substring-search.git)

# TODO: convert to function with array
if [ ! -d $target_dir/.oh-my-zsh/custom/plugins/zsh-autosuggestions ]; then
    git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions $target_dir/.oh-my-zsh/custom/plugins/zsh-autosuggestions
fi

if [ ! -d $target_dir/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting ]; then
    git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git $target_dir/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
fi

if [ ! -d $target_dir/.oh-my-zsh/custom/plugins/zsh-completions ]; then
    git clone --depth=1 https://github.com/zsh-users/zsh-completions $target_dir/.oh-my-zsh/custom/plugins/zsh-completions
fi

if [ ! -d $target_dir/.oh-my-zsh/custom/plugins/zsh-history-substring-search ]; then
    git clone --depth=1 https://github.com/zsh-users/zsh-history-substring-search $target_dir/.oh-my-zsh/custom/plugins/zsh-history-substring-search
fi

if [ ! -d $target_dir/.oh-my-zsh/plugins/fzf ]; then
    git clone --depth 1 https://github.com/junegunn/fzf.git $target_dir/.oh-my-zsh/plugins/fzf
fi

if [ ! -d $target_dir/.oh-my-zsh/custom/plugins/k ]; then
    git clone --depth 1 https://github.com/supercrabtree/k $target_dir/.oh-my-zsh/custom/plugins/k
fi

# Installing fonts
# TODO: convert to function
wget -q --show-progress -N https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Hack/Regular/complete/Hack%20Regular%20Nerd%20Font%20Complete.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/RobotoMono/Regular/complete/Roboto%20Mono%20Nerd%20Font%20Complete.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/DejaVuSansMono/Regular/complete/DejaVu%20Sans%20Mono%20Nerd%20Font%20Complete.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf -P $target_dir/.local/share/fonts/
wget -q --show-progress -N https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf -P $target_dir/.local/share/fonts/

fc-cache -fv

# Installing theme
# TODO
if [ ! -d $target_dir/.oh-my-zsh/custom/themes/powerlevel10k ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git $target_dir/.oh-my-zsh/custom/themes/powerlevel10k
fi

# Switching everything ON

cp "$target_dir/.oh-my-zsh/templates/zshrc.zsh-template" "$target_dir/.zshrc"
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/g' "$target_dir/.zshrc"
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting zsh-completions zsh-history-substring-search k)/g' "$target_dir/.zshrc"
chsh -s /bin/zsh