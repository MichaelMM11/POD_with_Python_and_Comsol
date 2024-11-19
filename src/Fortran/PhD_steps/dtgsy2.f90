! To compile program with LAPACK:
! gfortran  main.f90 -L/home/pato/src/lia/lapack -llapack -lrefblas
program main
    implicit none

    integer, parameter :: m=4, n=4 ! constants for test.
    integer, parameter :: lda=m, ldb=n, ldc=m, ldd=m, lde=n, ldf=m ! expected leading dimensions
    integer, parameter :: lwork=2*m*n !  If IJOB = 1 or 2 and TRANS = 'N', LWORK >= max(1,2*M*N).
    double precision  :: a(lda, m), b(ldb, n), c(ldc, n), d(ldd, m), e(lde, n), f(ldf, n) ! Matrices
    integer :: iwork(m+n+6), ijob, info, pq
    double precision :: scale, dif, work(lwork), rdsum, rdscal
!     a = reshape([-7.1555770296603405D-01, 0.0000000000000000D+00, 0.0000000000000000D+00, 0.0000000000000000D+00, &
! 5.5780493624012634D-02, 6.9981835964317174D-01, 0.0000000000000000D+00, 0.0000000000000000D+00, &
! -9.5693138681233525D-02, -6.5851962292754551D-01, 1.0032243285305493D+00, -1.3124006597006899D+00, &
! -1.3454038718762107D+00, -1.2853831529832671D-01, 1.0907645058376629D+00, 1.0032243285305493D+00], [4, 4])
    a(1,1)=4
    a(1,2)=1
    a(1,3)=1
    a(1,4)=2

    a(2,1)=0
    a(2,2)=3
    a(2,3)=4
    a(2,4)=1

    a(3,1)=0
    a(3,2)=1
    a(3,3)=3
    a(3,4)=1

    a(4,1)=0
    a(4,2)=0
    a(4,3)=0
    a(4,4)=6
    call pprint("a := ")
    call printgo(a, 4,4)

    b(1,1)=1
    b(1,2)=1
    b(1,3)=1
    b(1,4)=1

    b(2,1)=0
    b(2,2)=3
    b(2,3)=4
    b(2,4)=1

    b(3,1)=0
    b(3,2)=1
    b(3,3)=3
    b(3,4)=1

    b(4,1)=0
    b(4,2)=0
    b(4,3)=0
    b(4,4)=4
    call pprint("b := ")
    call printgo(b, 4,4)

    d(1,1)=2
    d(1,2)=1
    d(1,3)=1
    d(1,4)=3

    d(2,1)=0
    d(2,2)=1
    d(2,3)=2
    d(2,4)=1

    d(3,1)=0
    d(3,2)=0
    d(3,3)=1
    d(3,4)=1

    d(4,1)=0
    d(4,2)=0
    d(4,3)=0
    d(4,4)=2
    call pprint("d := ")
    call printgo(d, 4,4)

    e(1,1)=1
    e(1,2)=1
    e(1,3)=1
    e(1,4)=2

    e(2,1)=0
    e(2,2)=1
    e(2,3)=4
    e(2,4)=1

    e(3,1)=0
    e(3,2)=0
    e(3,3)=1
    e(3,4)=1

    e(4,1)=0
    e(4,2)=0
    e(4,3)=0
    e(4,4)=1
    call pprint("e := ")
    call printgo(e, 4,4)

    c(1,1)=-4
    c(1,2)=7
    c(1,3)=1
    c(1,4)=12

    c(2,1)=-9
    c(2,2)=2
    c(2,3)=-2
    c(2,4)=-2

    c(3,1)=-4
    c(3,2)=2
    c(3,3)=-2
    c(3,4)=8

    c(4,1)=-7
    c(4,2)=7
    c(4,3)=-6
    c(4,4)=19
    call pprint("c := ")
    call printgo(c, 4,4)

    f(1,1)=-7
    f(1,2)=5
    f(1,3)=0
    f(1,4)=7

    f(2,1)=-5
    f(2,2)=1
    f(2,3)=-8
    f(2,4)=0

    f(3,1)=-1
    f(3,2)=2
    f(3,3)=-3
    f(3,4)=5

    f(4,1)=-3
    f(4,2)=2
    f(4,3)=0
    f(4,4)=5
    call pprint("f := ")
    call printgo(f, 4,4)
    ijob=0
    call DTGSY2( 'N', ijob, m, n, a, lda, b, ldb, c,ldc, d, ldd, &
        e, lde, f, ldf, scale, rdsum, rdscal, &
                      iwork, pq, info )
    ! call dtgsyl('N', ijob, m, n, a, lda, b, ldb, c, ldc, d, ldd, &
    !     e, lde, f, ldf, scale, dif, work, lwork, iwork, info)
    print *, ''
    call printmat(f, 4, 4)
end program

subroutine printmat(a, r, c)
    implicit none
    double precision :: a (r,c)
    integer i,j,r,c
    do i=1, r
        do j=1,c
            WRITE (*,'(f0.4)',advance="no")  a(i,j) ! print elements
            WRITE (*,'(a)', advance="no") ", " ! separate elements with comma
        enddo
        print *, '' ! print newline
    enddo
end subroutine

subroutine printgo(a, r, c)
    implicit none
    integer i,j,r,c
    double precision :: a (r,c)
    write(*, '(a)', advance="no") "[]float64{"
    do i=1, r
        do j=1,c
            WRITE (*,'(f0.4)',advance="no")  a(i,j) ! print elements
            WRITE (*,'(a)', advance="no") ", " ! separate elements with comma
        enddo
    enddo
    write(*, '(a)') "}"
end subroutine

subroutine pprint(c)
    implicit none
    character (len=*), intent (in) :: c
    write (*, "(a)",advance="no") c
end subroutine

subroutine println(c)
    implicit none
    character (len=*), intent (in) :: c
    call pprint(c)
    print *, ""
end subroutine
