program test
    use, intrinsic :: iso_c_binding, only: ik => c_int, rk => c_double
    use svd
    implicit none
  
    integer, parameter :: nr = 5
    integer, parameter :: nc = 4
    integer, parameter :: ns = 3
    real(rk) ::  matrix(nr,nc)
    real(rk) ::  list(ns), diag(ns,ns)
    real(rk) ::  rvec(nc,ns)
    real(rk) ::  lvec(nr,ns)
  
    integer :: i
  
    matrix = 0.0_rk
    matrix(1,:) = real([1,2,3,4],rk)
    matrix(2,:) = real([2,3,4,5],rk)
    matrix(3,:) = real([3,4,5,6],rk)
    matrix(4,:) = real([4,5,6,7],rk)
    matrix(5,:) = real([5,6,7,8],rk)
    write(*, *) "input matrix"
    do i=1,5,1
      write(*, *) matrix(i,:)
    end do
    write(*, *)
  
    call svd_(nr,nc,ns,matrix,list,rvec,lvec)
    diag = 0.0_rk
    write(*, *) "singular values"
    do i = 1 , ns, 1
      diag(i, i) = list(i)
      write(*, *) diag(i,:)
    end do
    write(*,*)
  
    write(*,*) "right vectors"
    do i = 1, nc, 1
      write(*,*) rvec(i,:)
    end do
    write(*,*)
  
    write(*,*) "left vectors"
    do i = 1, nr, 1
      write(*,*) lvec(i,:)
    end do
    write(*,*)
  
    matrix = matmul(lvec,matmul(diag,transpose(rvec)))
    write(*,*) "U.S.V^T"
    do i=1, nr, 1
      write(*,*) matrix(i,:)
    end do
    write(*,*)
  end program test
