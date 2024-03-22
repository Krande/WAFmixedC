extern "C" void c_fort_add(int a, int b, int* result);

extern "C" int cpp_fort_add(int a, int b) {
    int result;
    c_fort_add(a, b, &result);
    return result;
}
