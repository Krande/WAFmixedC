extern void fort_add_(int* a, int* b, int* result);

void c_fort_add(int a, int b, int* result) {
    fort_add_(&a, &b, result);
}