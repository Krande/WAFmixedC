subroutine fort_add(a, b, result)
    implicit none
    integer, intent(in) :: a, b
    integer, intent(out) :: result

    result = a + b
end subroutine fort_add