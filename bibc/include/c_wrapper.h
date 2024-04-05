// c_wrapper.h

#ifndef FORT_OPERATIONS_H
#define FORT_OPERATIONS_H

#ifdef __cplusplus
extern "C" {
#endif

    // Declares the Fortran subroutine that adds two integers and returns the result.
    // The name is mangled to follow Fortran calling conventions from C.
    extern void fort_add_(int* a, int* b, int* result);

    // Declares a C function that serves as a wrapper around the Fortran subroutine.
    void c_fort_add(int a, int b, int* result);

#ifdef __cplusplus
}
#endif

#endif // FORT_OPERATIONS_H
