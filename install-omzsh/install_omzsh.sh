#!/bin/bash

pd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check zsh installed status
function check_zsh {
   pkg=zsh
   status="$(dpkg-query -W --showformat='${db:Status-Status}' "$pkg" 2>&1)"
   if [ ! $? = 0 ] || [ ! "$status" = installed ]; then
      sudo apt install $pkg
   else
      echo "zsh package is already installed"
   fi
}

# Install omzsh && plugins && themes
function install_omzsh () {
   local list=($@)
   local sum=${#list[@]}
   for (( n=1; n<$sum; n++ ))
      do
         if [[ $(($n % 2)) -eq 0 ]]; then
            git clone --depth=1 ${list[$n]} $dir
         else
            local dir="${list[0]}/${list[$n]}"
            if [ ! -d $dir ]; then
               mkdir -p $dir
            else
               n=$(($n+1))
            fi
         fi
      done
}

# Install fonts
function install_fonts () {
   local list=($@)
   local sum=${#list[@]}
   local dir=${list[0]}
   for (( url=1; url<$sum; url++ ))
      do
         wget -q --show-progress -N ${list[$url]} -P $dir
      done
   fc-cache -fv
}

# Activate plugins
function define_plugins {
   local sum=${#custom_plugins[@]}
   local m=0
   for (( n=1; n<$sum; n++ ))
      do
         if [[ ! $(($n % 2)) -eq 0 ]]; then
            array[$m]=${custom_plugins[$n]}
            n=$(($n+1))
            m=$(($m+1))
         fi
      done
   active_plugins=${array[@]}
}

# Switching everything ON
function switch_on {
   cp "$target_dir/.oh-my-zsh/templates/zshrc.zsh-template" "$target_dir/.zshrc"
   sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/g' "$target_dir/.zshrc"
   sed -i "s/plugins=(git)/plugins=(git $active_plugins)/g" "$target_dir/.zshrc"
   chsh -s /bin/zsh
}

# Main function
function main () {
   source $pd/config
   check_zsh
   install_omzsh ${omzsh[@]}
   install_omzsh ${plugins[@]}
   install_omzsh ${custom_plugins[@]}
   install_omzsh ${custom_themes[@]}
   install_fonts ${fonts[@]}
   define_plugins
   switch_on
}

main
