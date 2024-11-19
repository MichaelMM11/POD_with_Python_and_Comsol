program hello
real, parameter :: pi = 3.14159265
integer, parameter :: n = 10
real :: result_sin(n)
integer :: i

do concurrent (i = 1:n)  ! Careful, the syntax is slightly different
  result_sin(i) = sin(i * pi/4.)
  print *, result_sin(i)
end do

print *, result_sin

  ! This is a comment line; it is ignored by the compiler
  print *, 'Hello, World!'
end program hello
