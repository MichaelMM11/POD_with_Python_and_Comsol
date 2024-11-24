module abc
    implicit none
    integer :: ri = 5

    contains

    real function h(x)! result(r)
        real, intent(in) :: x
        h = x + 5.1 + ri
    end function h

    integer function g(x) result(r)
        real, intent(in) :: x
        r = int(x - 5)
    end function

end module abc
