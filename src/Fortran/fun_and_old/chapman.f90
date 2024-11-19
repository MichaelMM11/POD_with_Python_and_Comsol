Program readit
    use lapackMod, only: eigenvalues, print_eigenvalues, print_eigenvectors
    Implicit None
  
    Real, Dimension( 1:3, 1:2 ) :: a
    real, allocatable, dimension(:,:) :: b
    character(len=5)::charI
    character(len=20)::formatString
    Integer :: i, j, RES
  
    !one line per read
    Write( *, * ) 'Line at a time'
    Open( 10, file = 'dummy.dat' )
    Do i = 1, 3
       Read ( 10, * ) a( i, : )
       Write(  *, * ) a( i, : )
    End Do
    Close( 10 )
    
    Write(*,*) "----"
    Write (*,*) a

    RES = SIZE (a, DIM = 1)
    Write(*,*) "a rows", RES
    RES = SIZE (a, DIM = 2)
    Write(*,*) "a cols", RES
    Write(*,*) "----"
    b = 2*transpose(a)
    Write(*,*) b
    RES = SIZE (b, DIM = 1)
    Write(*,*) "b rows", RES
    RES = SIZE (b, DIM = 2)
    Write(*,*) "b cols", RES


    open(10, file='sample.txt')
        do i=1, size(b,1)
        write(10,*) b(i,:)
        end do
    close(10)

    ! ! All in one go
    ! Write( *, * ) 'All in one go'
    ! Open( 10, file = 'dummy.dat' )
    ! Read ( 10, * ) a
    ! Write(  *, * ) a
    ! Close( 10 )
    ! Write(  *, * ) 2*   transpose(a)
  
    ! ! Non advancing I/O
    ! Write( *, * ) 'Non-advancing'
    ! Open( 10, file = 'dummy.dat' )
    ! Do i = 1, 3
    !    Do j = 1, 3
    !       ! Non advancing I/O requires a 'proper' format
    !       Read ( 10, '( f3.1, 1x )', Advance = 'No' ) a( i, j )
    !       Write(  *, '( f3.1, 1x )', Advance = 'No' ) a( i, j )
    !    End Do
    !    ! Move to next records (lines)
    !    Read ( 10, * )
    !    Write(  *, * )
    ! End Do
    ! Close( 10 )
  
  End Program readit
