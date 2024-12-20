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
#      - get the files                                                          #
#          geo.vtu                                                              #
#          Comsol__qty_snapshots.dat                                            #
#        from Comsol->Export->Data->Output->File type (txt and vtu)             #
#                                                                               #
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

execute_make_gnuplots(){
    cd "$gnuplot_folder"
    gnuplot POD__acc_energy.gp
    gnuplot POD__eigenvalue.gp
}

return_main_folder(){
    cd "$bash_folder"
}

display_successful_run(){
    echo -e "\e[3;32mprogram was successful!\e[0m"
}

body(){
    #! different ways for colourful messages (= easier to read)
    # note that $1 refers to the 1st argument and is universal in bash
    # variant 1
    #echo -e "want \e[2;93m$1\e[0m: (y|n|a)"
    #read -rp "" gms

    # variant 2
    #read -rp "want to execute $1 (y|n): " gms

    # variant 3
    read -p $'run \e[3;93m'"$1"$'\e[0m: (y|n|any) ' choice
    #@ https://stackoverflow.com/questions/24998434/read-command-display-the-prompt-in-color-or-enable-interpretation-of-backslas

    choice=${choice}
    if [[ "$choice" == "y" || "$choice" == "" ]]; then
        echo -e "step \e[0;92m$1\e[0m is running..."
        $1
    elif [[ "$choice" == "n" ]]; then
        echo -e "step \e[2;97m$1\e[0m is skipped"
    else
        echo -e "\e[0;91mprogram terminated as a whole!\e[0m"
        exit
    fi
}


main(){
    body execute_generate_mesh_snapshot_from_file
    body execute_POD_with_solution_matrix
    body execute_make_diff_matrix
    body execute_make_vtu_data
    body execute_make_paraview_animation_files
    body execute_make_gnuplots

    #execute_generate_mesh_snapshot_from_file
    #execute_POD_with_solution_matrix
    #execute_make_diff_matrix
    #execute_make_vtu_data
    #execute_make_paraview_animation_files
    #execute_make_gnuplots
    #return_main_folder
    display_successful_run
}


main
