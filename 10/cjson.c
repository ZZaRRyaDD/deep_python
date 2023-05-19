#include <stdbool.h>
#include <stdio.h>
#include <Python.h>


int compare_symbols(PyObject* firstChar, const char secondChar)
{
    return PyObject_RichCompareBool(
        firstChar,
        PyUnicode_FromString(&secondChar),
        Py_EQ
    );
}

PyObject* cjson_loads(PyObject* self, PyObject* args)
{
    PyObject* json_str;
    if (!PyArg_ParseTuple(args, "U", &json_str))
    {
       PyErr_Format(PyExc_TypeError, "Expected unicode string");
       return NULL;
    }
    Py_ssize_t length_unicode_json_str = PyUnicode_GetLength(json_str);
    bool isNumber = false, isString = false;
    PyObject* dict = NULL;
    PyObject* key = NULL;
    bool keyCreated = false;
    PyObject* value = NULL;
    Py_ssize_t lenKey = 0;
    Py_ssize_t lenValue = 0;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }
    const char openBracket = '{';
    const char closeBracket = '}';
    const char doubleQuote = '"';
    const char colon = ':', emptyChar = ' ', commaChar = ',';
    char* emptyString = "";
    const char oneChar = '1', twoChar = '2', threeChar = '3', fourChar = '4';
    const char fiveChar = '5', sixChar = '6', sevenChar = '7', eightChar = '8';
    const char nineChar = '9';
    if (length_unicode_json_str)
    {
        if(
            PyUnicode_Count(json_str, PyUnicode_FromString(&openBracket), 0, 2) == 0 &&
            PyUnicode_Count(json_str, PyUnicode_FromString(&closeBracket), length_unicode_json_str-2, length_unicode_json_str) == 0
        )
        {
            PyErr_Format(PyExc_TypeError, "Expected start bracket and end bracket in string");
            return NULL;
        }
    }
    else
    {
        PyErr_Format(PyExc_TypeError, "String is empty");
        return NULL;
    }
    
    for (Py_ssize_t i = 0; i < length_unicode_json_str; i++)
    {
        PyObject* element = PyUnicode_Substring(json_str, i, i + 1);
        printf("symbol - %s\n", PyUnicode_AsUTF8(element));

        if (key == NULL && value == NULL && compare_symbols(element, doubleQuote))
        {
            lenKey++;
            key = PyList_New(0);
            if (key == NULL) {
                printf("ERROR: Failed to create List Object\n");
                return NULL;
            }
            continue;
        }

        if (key != NULL && value == NULL)
        {
            // if (keyCreated == true)
            // {
            //     if (compare_symbols(element, doubleQuote))
            //     {
            //         value = PyList_New(0);
            //         if (value == NULL)
            //         {
            //             printf("ERROR: Failed to create List Object\n");
            //             return NULL;
            //         }
            //         isString = true;
            //         continue;
            //     }
            //     else if
            //     (
            //         compare_symbols(element, oneChar) ||
            //         compare_symbols(element, twoChar) ||
            //         compare_symbols(element, threeChar) ||
            //         compare_symbols(element, fourChar) ||
            //         compare_symbols(element, fiveChar) ||
            //         compare_symbols(element, sixChar) ||
            //         compare_symbols(element, sevenChar) ||
            //         compare_symbols(element, eightChar) ||
            //         compare_symbols(element, nineChar)
            //     )
            //     {
            //         value = PyList_New(0);
            //         if (value == NULL)
            //         {
            //             printf("ERROR: Failed to create List Object\n");
            //             return NULL;
            //         }
            //         isNumber = true;
            //         continue;
            //     }
            //     else if
            //     (
            //         compare_symbols(element, colon) ||
            //         compare_symbols(element, emptyChar)
            //     ) 
            //     {
            //         continue;
            //     }
            // }

            if (lenKey > 0 && compare_symbols(element, doubleQuote))
            {   
                const char* string = PyUnicode_AsUTF8(
                    PyUnicode_Join(PyUnicode_FromString(emptyString), key)
                );
                if (!(key = Py_BuildValue("s", string))) {
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }
                lenKey = 0;
                keyCreated = true;
            }
            else if (lenKey > 0)
            {
                lenKey++;
                if (PyList_Append(key, element) == -1)
                {
                    printf("ERROR: Failed to add item to List Object\n");
                    return NULL;
                }
            }
        }

        // if (key != NULL && value != NULL)
        // {
        //     if (
        //         compare_symbols(element, doubleQuote) &&
        //         isString
        //     )
        //     {
        //         const char* string = PyUnicode_AsUTF8(
        //             PyUnicode_Join(PyUnicode_FromString(emptyString), value)
        //         );
        //         if (!(value = Py_BuildValue("s", string))) {
        //             printf("ERROR: Failed to build string value\n");
        //             return NULL;
        //         }
        //     }
        //     else if (
        //         compare_symbols(element, commaChar) &&
        //         isNumber
        //         )
        //     {
        //         const char* string = PyUnicode_AsUTF8(
        //             PyUnicode_Join(PyUnicode_FromString(emptyString), value)
        //         );
        //         if (!(value = Py_BuildValue("i", string))) {
        //             printf("ERROR: Failed to build integer value\n");
        //             return NULL;
        //         }
        //     }
        //     else
        //     {
        //         lenValue++;
        //         if (PyList_Append(value, element) == -1)
        //         {
        //             printf("ERROR: Failed to add item to List Object\n");
        //             return NULL;
        //         }
        //     }
        //     PyMem_Free(value);
        //     lenValue = 0;
        //     if (PyDict_SetItem(dict, key, value) < 0) {
        //         printf("ERROR: Failed to set item\n");
        //         return NULL;
        //     }
        //     PyMem_Free(key);
        //     PyMem_Free(value);
        // }
    }
    return dict;
}

// PyObject* cjson_dumps(PyObject* self, PyObject* args)
// {
//     PyObject* dict;
//     if (!PyArg_ParseTuple(args, "O", &dict))
//     {
//        PyErr_Format(PyExc_TypeError, "Expected dict object");
//        return NULL;
//     }
//     PyObject* listItems = PyDict_Items(&dict);
//     long listSize = PyList_Size(listItems);
//     for (long i = 0; i < listSize; i++) 
//     {
//         PyObject* element = PyList_GetItem(listItems, i);
//         element
//     }
// }

static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Loads dict from string"},
    // {"dumps", cjson_dumps, METH_VARARGS, "Convert dict to string"},
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
