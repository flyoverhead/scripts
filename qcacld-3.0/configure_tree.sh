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

configure_tree > /dev/null 2>/dev/null
