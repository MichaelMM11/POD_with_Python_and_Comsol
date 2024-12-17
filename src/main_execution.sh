#!/bin/bash

#################################################################################
#                                                                               #
#                                                                               #
#  purpose                                                                      #
#      - instead to remember which program (Python or Bash) should be executed  #
#          it is of much greater convenience and consistency to 'outsource'     #
#          this issue to an execution file...which it this file                 #
#  remark                                                                       #
#      - user interability is considered not only to be convenient but also     #
#          as a feedback as well, therefore it makes sense to interact with     #
#          one POD-run (from start to end)                                      #
#      - if you want to continue not from step 1 but ...let's say step 4 then   #
#          be aware that some side effects are possible                         #
#                                                                               #
#      - get the files
#          geo.vtu
#          Comsol__qty_snapshots.dat
#        from Comsol->Export->Data->Output->File type (txt and vtu)
#
#################################################################################

bash_folder='/home/michael/Git/POD_with_Python_and_Comsol/src/Bash'
python_folder='/home/michael/Git/POD_with_Python_and_Comsol/src/Python'
gnuplot_folder='/home/michael/Git/POD_with_Python_and_Comsol/src/Gnuplot'

execute_generate_mesh_snapshot_from_file(){
    cd "$bash_folder"
    ./generate_mesh_snapshot_from_file.sh
}

execute_POD_with_solution_matrix(){
    cd "$python_folder"
    echo -e "$python_folder"
    #python_version
    python POD_with_solution_matrix.py
}

execute_make_diff_matrix(){
    cd "$python_folder"
    python make_diff_matrix.py
}

execute_make_vtu_data(){
    cd "$python_folder"
    python make_vtu_data.py
}

execute_make_paraview_animation_files(){
    cd "$python_folder"
    python make_paraview_animation_files.py
}

return_main_folder(){
    cd "$bash_folder"
}

display_successful_run(){
    echo -e "\e[3;32mprogram was successful!\e[0m"
}

body(){
    #echo -e "$1"
    #! works
    #echo -e "want \e[2;93m$1\e[0m: (y|n|a)"
    #read -rp "" gms
    
    read -p $'run \e[3;32m'"$1"$'\e[0m: (y|n|any) ' gms  # https://stackoverflow.com/questions/24998434/read-command-display-the-prompt-in-color-or-enable-interpretation-of-backslas
    #read -rp "want to execute $1 (y|n): " gms

    gms=${gms}
    echo -e "value is $gms"
#! add colour here
    if [[ "$gms" == "y" || "$gms" == "" ]]; then
        #echo -e "\e[2;96m$1\e[0m"
        #echo -e "program is executed"
        $1
    elif [[ "$gms" == "n" ]]; then
        echo -e "program is not executed"  # is skipped
    else
        echo -e "program terminates as a whole"
        exit
    fi
}



main(){
    body execute_generate_mesh_snapshot_from_file
    #body execute_POD_with_solution_matrix
    #body execute_make_diff_matrix
    #body execute_make_vtu_data
    #body execute_make_paraview_animation_files
#     read -rp "want to execute generate_mesh_snapshot_from_file (y|n): " gms
#     gms=${gms}
# #! add colour here
#     if [[ "$gms" == "y" || "$gms" == "" ]]; then
#         echo -e "program is executed"
#         execute_generate_mesh_snapshot_from_file
#     elif [[ "$gms" == "n" ]]; then
#         echo -e "program is not executed"
#     else
#         echo -e "program terminates"
#         exit
#     fi


    #execute_generate_mesh_snapshot_from_file
    #execute_POD_with_solution_matrix
    #execute_make_diff_matrix
    #execute_make_vtu_data
    #execute_make_paraview_animation_files
    #return_main_folder
    display_successful_run
}


main
