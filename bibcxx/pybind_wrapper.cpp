#include <pybind11/pybind11.h>
int cpp_fort_add(int a, int b);

PYBIND11_MODULE(example, m) {
    m.def("add", &cpp_fort_add, "A function which adds two numbers using Fortran");
}
