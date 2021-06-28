#include <Python.h>


int c_fibonacci(int n)
{
  if (n < 2)
    return n;
  else
    return c_fibonacci(n - 1) + c_fibonacci(n - 2);
}


// function fibonacci
static PyObject* fibonacci(PyObject* self, PyObject* args)
{
  int n;

  if(!PyArg_ParseTuple(args, "i", &n))
    return NULL;

  return Py_BuildValue("i", c_fibonacci(n));
}


// function version
static PyObject* version(PyObject* self){
  return Py_BuildValue("s", "Version 1.0");
}


static PyMethodDef fibonacciMethods[] = {
  {"fibonacci", fibonacci, METH_VARARGS, "Calculates fibonacci numbers."},
  {"version", (PyCFunction)version, METH_NOARGS, "Return the version."},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fibonacciModule = {
  PyModuleDef_HEAD_INIT,
  "myModule",
  "Fibonacci Module",
  -1,
  fibonacciMethods
};

PyMODINIT_FUNC PyInit_fibonacciModule(void){
  return PyModule_Create(&fibonacciModule);
}
