program main
    implicit none

    ! constants
    integer, parameter :: sp = selected_real_kind(6, 37)
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: qp = selected_real_kind(33, 4931)

    ! parameter
    integer :: row, col, i, j

    real(kind=sp), allocatable :: M(:,:)

    character (len=20) file_out_name, file_in_name


    ! parameter declaration
    file_out_name = "output.txt"


    ! interesting part
    print *, 'pass filename'
    read(*,*) file_in_name
    print *, "your input was ", file_in_name

    print *, 'pass the dimension of the file (row, vol):'
    read(*,*) row, col
    print *, "the allocated matrix dimension will be:"
    print *, "rows: ", row
    print *, "cols: ", col
    allocate(M(row, col))

    open(unit=15, file=file_in_name, status='old')
    read(15,*) ((M(i,j), i=1,row), j=1,col)
    close(15)

    print *, "M=", M
    print *, "M_row=", size(M, 1)
    print *, "M_col=", size(M, 2)
    print *,""

    ! works not
    print *, ""
    print *, "M(1,:)=", M(1,:)
    print *, "M(2,:)=", M(2,:)
    print *, "M(3,:)=", M(3,:)
    print *, "M(4,:)=", M(4,:)

    print *, ""
    print *, "M(:,1)=", M(:,1)
    print *, "M(:,2)=", M(:,2)
    print *, "M(:,3)=", M(:,3)
    print *, "M(:,4)=", M(:,4)

    print *, ""
    print *, "M(1,1)=", M(1,1)
    print *, "M(1,2)=", M(1,2)
    print *, "M(1,3)=", M(1,3)
    print *, "M(1,4)=", M(1,4)
    
    print *, ""
    print *, "M(2,1)=", M(2,1)
    print *, "M(2,2)=", M(2,2)
    print *, "M(2,3)=", M(2,3)
    print *, "M(2,4)=", M(2,4)

    print *, ""
    print *, "M(3,1)=", M(3,1)
    print *, "M(3,2)=", M(3,2)
    print *, "M(3,3)=", M(3,3)
    print *, "M(3,4)=", M(3,4)

    print *, ""
    print *, "M(4,1)=", M(4,1)
    print *, "M(4,2)=", M(4,2)
    print *, "M(4,3)=", M(4,3)
    print *, "M(4,4)=", M(4,4)

    open(1, file=file_out_name, status='replace')

     do j=1,col
        do i=1,row
            write(1,'(f8.3,t3)', advance='no') M(i,j)  ! write(1,'("|")',advance='no')
        end do
       write(1,'("")')
    end do
    close(1)

end program main
