program consts

!implicit none  ! the whole point what happens when not used
i = 1.0
call sub(y)

end

subroutine sub(x)
!implicit none
!real x

write (*,*) 'x= ', x
return
end
