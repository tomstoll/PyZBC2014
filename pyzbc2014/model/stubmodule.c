#include <Python.h>

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "libzbc2014",
    NULL,
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_libzbc2014(void)
{
    return PyModule_Create(&moduledef);
}