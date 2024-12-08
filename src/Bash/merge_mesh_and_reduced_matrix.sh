#!/bin/bash

######################################################################################
#                                                                                    #
#                                                                                    #
#  purpose                                                                           #
#      - to merge two files, the mesh coordinates and the reduced POD matrices that  #
#        contain the values of POD process                                           #
#      - this results in one file where the mapping mesh-coordinates and values      #
#        are as it is provided in COMSOLs export file                                #
#                                                                                    #
#  remark                                                                            #
#      - files tries to be interactive and forgivable as well as extensible,         #
#        however it makes heavy use of 'global' variables because 1) that is the     #
#        way .sh behaves in the first place 2) avoid over-engineering                #
#                                                                                    #
#                                                                                    #
#####################################################################################

iterate_all_selected_files(){
#@ - https://stackoverflow.com/questions/61784456/combine-two-csv-files-based-on-common-column-using-awk-or-sed
#@ - https://unix.stackexchange.com/questions/35369/how-to-define-tab-delimiter-with-cut-in-bash
for file in $POD_file*; do
    [ -f "$file" ] || continue
    generate_mesh_POD_filename "$file"
    merge_mesh_with_POD
    echo -e "\e[0;33m $file\e[0m generated\n \e[0;32m$merged_file\e[0m"
    echo ""
done
}

merge_mesh_with_POD(){
    paste -d$'\t' <(cut -d, -f 1-2 "$mesh_file") "$file" > "$merged_file"
}

select_PODs_file(){
    echo -e "\e[0;33mset POD files: \e[0m" 
    read -rp  "all files starting with text (default 'reduced') are used: " POD_file
    POD_file=${POD_file:-reduced}
}

select_mesh_file(){
    list_files_in_folder
    echo -en "\e[0;33mset mesh file: \e[0m"
    read -rp "" mesh_file
    if ! [ -f "$mesh_file"  ]; then
        echo -ne "\e[0;31mERROR: current folder does not contain file: "
        echo -e "$mesh_file\e[0;37m"
        exit
    fi
}

generate_mesh_POD_filename(){
    trunk_filename=${1%.*}  #@ remove suffix
    merged_file="$trunk_filename"__mesh__POD.dat
}

select_folder(){
    echo -e "\e[0;33mEnter number to select directory: \e[0m"
    options=('current folder'
             '/home/michael/Git/POD_with_Python_and_Comsol/data/'
             '/home/michael/Git/stiffness_matrix____PETSc/data/'
             'set')
    select directory in "${options[@]}"; do
        if [[ "$directory" == "" ]]; then
            echo -e "\e[0;31mERROR: invalid option selected."
            echo -e "Program aborted.\e[0m"
            exit
        fi
        if [[ "$directory" == "current folder" ]]; then
            directory=$(pwd)
        fi

        if [[ "$directory" == "set" ]]; then
            read -rp "pass dir: " directory
        fi
        if ! [ -d "$directory" ]; then
            echo -e "\e[0;31mERROR: directory does not exist.\e[0m"
            exit
        fi
    cd "$directory" || exit
    break
    done
}

display_final_message(){
    echo -e "\e[0;32mfilter was successfully applied to listed files\e[0m"
}

list_files_in_folder(){
#@ - https://stackoverflow.com/questions/2437452/how-to-get-the-list-of-files-in-a-directory-in-a-shell-script
#@ - a friendly gesture to copy&paste file on the fly and avoid copying from
#@   some other window
    echo -e "\e[0;35m\nfolder contains following files to choose"
    echo -e "=========================================\e[0m"
    find . -maxdepth 1 -type f -not -path '*/\.*' | sed 's/^\.\///g' | sort
    echo
}


main(){
    select_folder
    select_mesh_file
    select_PODs_file
    iterate_all_selected_files
    display_final_message
}


main
