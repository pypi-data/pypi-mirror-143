module memory_leak

    use, intrinsic :: iso_fortran_env
    
    implicit none

    public

    type d_params
        
        integer simType           
        real l0
        real, dimension(3, 4) :: cdims
        logical field_int_on_currently

    end type

contains

        subroutine set_param_defaults(alloc_test, xlc_p)
                
               implicit none
        
                integer :: I,J, flag
                real, intent(inout), allocatable :: alloc_test(:,:)
                type(d_params), intent(inout) :: xlc_p
       
		alloc_test(1,1) = alloc_test(1,1) + 1

        end subroutine set_param_defaults

end module memory_leak
