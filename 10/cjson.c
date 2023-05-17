#include <stdbool.h>
#include <stdio.h>
#include <Python.h>

PyObject* cjson_loads(PyObject* self, PyObject* args)
{
    PyObject* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str))
    {
       PyErr_Format(PyExc_TypeError, "Expected unicode string");
       return NULL;
    }
    PyObject* unicode_json_str = PyUnicode_FromString((char*) &json_str);
    Py_ssize_t length_unicode_json_str = PyUnicode_GetLength(unicode_json_str);
    bool isOpenBracket = false;
    bool isNumber = false, isString = false;
    PyObject* dict = NULL;
    PyObject* key = NULL;
    PyObject* value = NULL;
    int lenKey = 0;
    int lenValue = 0;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }
    char openBracket = '{', closeBracket = '}', doubleQuote = '"';
    char colon = ':', emptyChar = ' ', commaChar = ',';
    char oneChar = '1', twoChar = '2', threeChar = '3', fourChar = '4';
    char fiveChar = '5', sixChar = '6', sevenChar = '7', eightChar = '8';
    char nineChar = '9';
    for (Py_ssize_t i = 0; i < length_unicode_json_str; i++)
    {
        PyObject* element = PyUnicode_Substring(unicode_json_str, i, i + 1);
        PyObject* element_str = PyUnicode_FromObject(element);

        PyObject* objectsRepresentation = PyObject_Repr(element_str);
        PyObject* str = PyUnicode_AsEncodedString(objectsRepresentation, "utf-8", "~E~");
        const char *bytes = PyBytes_AS_STRING(str);
        printf("REPR: %s\n", bytes);

        if (PyUnicode_CompareWithASCIIString(element_str, &openBracket) == 0)
        {
            isOpenBracket = true;
            continue;
        }

        if (
            PyUnicode_CompareWithASCIIString(element_str, &closeBracket) == 0 &&
            isOpenBracket == true
        )
        {
            break;
        }
        else
        {
            PyErr_Format(PyExc_TypeError, "Expected start bracket and end bracket in string");
            return NULL;
        }

        if (
            key == NULL &&
            value == NULL &&
            PyUnicode_CompareWithASCIIString(element_str, &doubleQuote) == 0
        )
        {
            lenKey++;
            size_t n = lenKey * sizeof(PyObject);
            key = PyMem_Malloc(n);
            if (key == NULL)
            {
                printf("ERROR: Failed allocate memory\n");
                return NULL;
            }
            (&key)[lenKey - 1] = (PyObject*)"";
            continue;
        }

        if (key != NULL && value == NULL)
        {
            if (
                key == NULL &&
                PyUnicode_CompareWithASCIIString(element_str, &doubleQuote) == 0
            )
            {
                lenKey++;
                key = (PyObject*)PyMem_Realloc(key, sizeof(Py_UNICODE) * lenKey);
                (&key)[lenKey - 1] = (PyObject*)"\0";
                if (!(key = Py_BuildValue("s", key))) {
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }
                PyMem_Free(key);
                lenKey = 0;
            }
            else if (key != NULL)
            {
                if (PyUnicode_CompareWithASCIIString(element_str, &doubleQuote) == 0)
                {
                    lenValue++;
                    size_t n = lenKey * sizeof(PyObject);
                    value = PyMem_Malloc(n);
                    if (value == NULL)
                    {
                        printf("ERROR: Failed allocate memory\n");
                        return NULL;
                    }
                    (&value)[lenValue - 1] = (PyObject*)"";
                    isString = true;
                    continue;
                }
                else if (
                    PyUnicode_CompareWithASCIIString(element_str, &oneChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &twoChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &threeChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &fourChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &fiveChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &sixChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &sevenChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &eightChar) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &nineChar) == 0
                )
                {
                    lenValue++;
                    size_t n = lenKey * sizeof(PyObject);
                    value = PyMem_Malloc(n);
                    if (value == NULL)
                    {
                        printf("ERROR: Failed allocate memory\n");
                        return NULL;
                    }
                    (&value)[lenValue-1] = element_str;
                    isNumber = true;
                    continue;
                }
                else if (
                    PyUnicode_CompareWithASCIIString(element_str, &colon) == 0 ||
                    PyUnicode_CompareWithASCIIString(element_str, &emptyChar) == 0
                ) 
                {
                    continue;
                }
            }
            else
            {
                lenKey++;
                key = (PyObject*)PyMem_Realloc(key, sizeof(Py_UNICODE) * lenKey);
                (&key)[lenKey - 1] = element_str;
            }
        }

        if (key != NULL && value != NULL)
        {
            if (
                PyUnicode_CompareWithASCIIString(element_str, &doubleQuote) == 0 &&
                isString
            )
            {
                lenValue++;
                value = (PyObject*)PyMem_Realloc(value, sizeof(Py_UNICODE) * lenValue);
                (&value)[lenValue - 1] = (PyObject*)"\0";
                if (!(value = Py_BuildValue("s", value))) {
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }
                PyMem_Free(value);
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    return NULL;
                }
                PyMem_Free(key);
                PyMem_Free(value);
            }
            else if (
                PyUnicode_CompareWithASCIIString(element_str, &commaChar) == 0 &&
                isNumber
                )
            {
                lenValue++;
                value = (PyObject*)PyMem_Realloc(value, sizeof(Py_UNICODE) * lenValue);
                (&value)[lenValue - 1] = (PyObject*)"\0";
                if (!(value = Py_BuildValue("i", value))) {
                    printf("ERROR: Failed to build integer value\n");
                    return NULL;
                }
                PyMem_Free(value);
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    return NULL;
                }
                PyMem_Free(key);
                PyMem_Free(value);
            }
            else
            {
                lenValue++;
                value = (PyObject*)PyMem_Realloc(value, sizeof(Py_UNICODE) * lenValue);
                (&value)[lenKey - 1] = PyUnicode_FromObject(element_str);
            }
        }
    }
    return dict;
}

PyObject* cjson_dumps(PyObject* self, PyObject* args)
{
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict))
    {
       PyErr_Format(PyExc_TypeError, "Expected dict object");
       return NULL;
    }
    PyObject* listItems = PyDict_Items(&dict);
    long listSize = PyList_Size(listItems);
    for (long i = 0; i < listSize; i++) 
    {
        PyObject* element = PyList_GetItem(listItems, i);
        element
    }
}

static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Loads dict from string"},
    {"dumps", cjson_dumps, METH_VARARGS, "Convert dict to string"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef cjsonmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "Module serializer or deserialize object with json into c code",
    1,
    methods,
};

PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create(&cjsonmodule);
}
