#!/bin/bash

#################################################################################
#                                                                               #
#                                                                               #
#  purpose                                                                      #
#      - to manipulate COMSOL file that only matrix is left                     #
#        - so the first column(s) that contain the information about the mesh   #
#          position is cut of as well as metadata header marked as comment      #
#      - but any other file that has data in matrix format can be passed        #
#        because the filter that applies to COMSOL simply has no effect then    #
#        and at the end of the day they generate the same output files          #
#                                                                               #
#  remark                                                                       #
#      - so far no tests are done with large, Large, LARGE files, it can turn   #
#        out that there must be another approach to handle them efficiently     #
#      - either so ALL replacing/deleting in one command call (can be ugly and  #
#        nasty to write) or look out for other languages like Perl; Python can  #
#        do this out of the box for sure but execution speed and Python does    #
#        not have that much in common                                           #
#      - filter does NOT check if the operation happens on a file from comsol,  #
#        i.e. there is no warning or error message when applied to a file that  #
#        does not have comsol metadata header                                   #
#        - also there is no warning/error when the first 3 columns of a         #
#          1 column matrix should be deleted or extracted, the regex parser     #
#          does its job without any checks, it simply keeps on going...         #
#       - anyway, as long as you operate it on a comsol generated file you      #
#         can ignore all these remarks                                          #
#                                                                               #
#                                                                               #
#################################################################################


obsolete_insufficient_awk_approach(){
#! - here to be some (helpful) starting point when one day algorithm should be
#!   written in pure awk
    echo -e "\e[0;31mERROR: do not use something that is not working yet.\e[0;37m"
    #awk '{ if($1 != "%"){ $1=$2=""; print $0}} OFS="\t"'input b.txt > output.txt
    exit
}

replace_spaces_with_tab(){
    sed -i 's/ \+ /\t/g' "$comsol_data_file"
}

delete_lines_starting_with_comment(){
    sed -i '/^\s*%/ d' "$comsol_data_file"
}

return_snapshot_matrix(){
    cut --complement -f"$dimension" "$comsol_data_file" > "$snapshot_file"
}

return_mesh_matrix(){
    cut  -f"$dimension" "$comsol_data_file" > "$mesh_file"
}

display_final_message(){
    echo -e "\e[0;32mfilter was applied to file successfully\e[0m"
}

select_geometrical_dimension_of_data(){
    echo -e "\e[0;33mEnter dimension to be reduced from Comsol: \e[0m"
    options=('1d (x)'
             '2d (x,y)'
             '3d (x,y,z)')
    select opt in "${options[@]}"; do
        if [[ $opt == "" ]]; then
            echo -e "\e[0;31mERROR: invalid option selected."
            echo -e "Program aborted.\e[0;37m"
            exit
        fi
        if [[ $opt == "1d (x)" ]]; then
            dimension="1"
        fi
        if [[ $opt == "2d (x,y)" ]]; then
            dimension="1,2"
        fi
        if [[ $opt == "3d (x,y,z)" ]]; then
            dimension="1,2,3"
        fi
    return
    done
}

return_dimension(){
    dim=`grep -i 'Dimension' $comsol_data_file | awk '{print $3}'`
    expr="$(grep -i 'Expressions' $comsol_data_file | awk '{print $3}')"
    row=$(grep -i 'Nodes' "$comsol_data_file" | awk '{print $3}')
    col="$((dim+expr))"

    if [[ $dim == "" ]]; then
        echo -e "\e[0;31mERROR: $comsol_data_file is already processed"
        echo -e "no value detraction possible!\e[0m"
        col=""
    fi

    echo ""
    echo -e "number of dimension:....$dim"
    echo -e "number of expressions:..$expr"
    echo -e "number of rows:.........$row"
    echo -e "number of columns:......$col"
    echo ""
}

apply_blind_algorithm(){
    replace_spaces_with_tab
    return_dimension
    delete_lines_starting_with_comment
}

retrun_generated_snapshot_mesh_data(){
    return_snapshot_matrix
    return_mesh_matrix
}

display_generated_files(){
    echo -e "\e[0;33m$comsol_data_file\e[0m generated"
    echo -e "- \e[0;32m$snapshot_file\e[0m"
    echo -e "- \e[0;32m$mesh_file\e[0m"
    echo
}

select_folder(){
    echo -e "\e[0;33mEnter number to select directory\e[0m"
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

select_data_file(){
    list_files_in_folder

    echo -en "\e[0;33mset COMSOL/matrix data file: \e[0m"
    read -rp "" comsol_data_file
    if ! [ -f "$comsol_data_file"  ]; then
        echo -ne "\e[0;31mERROR: current folder does not contain file: "
        echo -e "$comsol_data_file\e[0;37m"
        exit
    fi
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

define_snapshot_mesh_filenames(){
#@ - to have consistent filename structure the semantic part is added to the
#@   filename; for this the suffix needs to be removed and added with the
#@   information
    trunk_of_comsol_data=${comsol_data_file%.*}  #@ remove suffix
    snapshot_file="$trunk_of_comsol_data"__snapshots.dat
    mesh_file="$trunk_of_comsol_data"__mesh.dat
}

main(){
    select_folder
    select_data_file
    define_snapshot_mesh_filenames
    select_geometrical_dimension_of_data
    apply_blind_algorithm
    retrun_generated_snapshot_mesh_data
    display_generated_files
    display_final_message
}


main

