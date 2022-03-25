#!/bin/bash

pd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $pd/config

function add_repo () {
	git remote add $1 $2
	git fetch $1 $tag
	git merge --no-commit FETCH_HEAD --allow-unrelated-histories
	git read-tree --prefix=drivers/staging/$1 -u FETCH_HEAD
	git commit -m "Merge $1 tag $tag into $current_branch"
	echo "$1 remote repo has been added successfully"
}

function fetch_repo () {
	git fetch $1 $tag
	git merge -X subtree=drivers/staging/$1 --no-commit FETCH_HEAD
	git commit -m "Merge $1 tag $tag into $current_branch"
	echo "Tag $tag has been merged successfully"
}

function check_repo () {
	if git remote show | grep $1 > /dev/null 2>/dev/null; then
		echo "Fetching updates for $1..."
		fetch_repo $1
	else
		add_repo $1 $2
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
