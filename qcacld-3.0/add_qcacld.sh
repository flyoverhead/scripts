#!/bin/bash

pd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $pd/config

function configure_tree {
	local sum=${#kernel_tree[@]}
	for (( n=0; n<$sum; n++ ))
	do
		src_string=$n
		src_file=$src_string+1
		target_string="${kernel_tree[$src_string]}"
		substring=${target_string:2}
		if cat "${kernel_tree[$src_file]}" | grep "$substring"; then
			:
		elif [ $n -eq 0 ]; then
			sed -i "${kernel_tree[$src_string]}\n" "${kernel_tree[$src_file]}"
		else
			sed -i "${kernel_tree[$src_string]}" "${kernel_tree[$src_file]}"
		fi
		n=$src_string+1		
	done
	rm -f "${qcacld_kconfig[0]}"
	echo "${qcacld_kconfig[1]}" > "${qcacld_kconfig[0]}"
	sed -i "s/${qcacld_kconfig[2]}/${qcacld_kconfig[3]}/g" "${qcacld_kconfig[0]}"
}

function add_repo () {
	git remote add $1 $2
	git subtree add --prefix drivers/staging/$1 $1 $tag
	echo "$1 remote repo successfully added"
}

function fetch_repo () {
	current_branch=$(git branch --show-current)
	git fetch $1 $tag
	git merge --no-commit --allow-unrelated-histories FETCH_HEAD
	git commit -m "Merge tag $tag to $current_branch"
}

function check_repo () {
	if git remote show | grep $1 > /dev/null 2>/dev/null; then
		echo "Fetching updates for $1..."
		fetch_repo $1
	else
		add_repo $1 $2
		fetch_repo $1
	fi
}

function main {	
	sum=${#qcacld_repo[@]}
	for (( n=0; n<$sum; n++ ))
	do
		name=$n
		url=$name+1
		check_repo ${qcacld_repo[$name]} ${qcacld_repo[$url]}
		n=$name+1
	done
}

main
configure_tree > /dev/null 2>/dev/null
