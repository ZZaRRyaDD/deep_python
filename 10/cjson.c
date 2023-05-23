#include <stdbool.h>
#include <stdio.h>
#include <Python.h>


int compare_symbols(PyObject* firstChar, const char secondChar)
{
    return PyUnicode_Compare(firstChar, PyUnicode_FromString(&secondChar)) == 0;
}

int compare_symbols_ptr(PyObject* firstChar, const char* secondChar)
{
    return PyUnicode_Compare(firstChar, PyUnicode_FromString(secondChar)) == 0;
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
        PyErr_Format(PyExc_MemoryError, "Failed to create Dict Object");
        return NULL;
    }
    const char* emptyString = "";
    const char* openBracket = "{";
    const char* closeBracket = "}";
    const char* commaChar = ",";
    const char* doubleQuote = "\"";
    const char* oneChar = "1";
    const char* twoChar = "2";
    const char* threeChar = "3";
    const char* fourChar = "4";
    const char* fiveChar = "5";
    const char* sixChar = "6";
    const char* sevenChar = "7";
    const char* eightChar = "8";
    const char* nineChar = "9";
    if (length_unicode_json_str)
    {
        if(
            PyUnicode_Count(json_str, PyUnicode_FromString(openBracket), 0, 2) == 0 &&
            PyUnicode_Count(json_str, PyUnicode_FromString(closeBracket), length_unicode_json_str-2, length_unicode_json_str) == 0
        )
        {
            PyErr_Format(PyExc_ValueError, "Expected start bracket and end bracket in string");
            return NULL;
        }
    }
    else
    {
        PyErr_Format(PyExc_ValueError, "String is empty");
        return NULL;
    }

    for (Py_ssize_t i = 0; i < length_unicode_json_str; i++)
    {
        PyObject* element = PyUnicode_Substring(json_str, i, i + 1);

        if (key == NULL && value == NULL && compare_symbols_ptr(element, doubleQuote))
        {
            lenKey++;
            key = PyList_New(0);
            if (key == NULL) {
                PyErr_Format(PyExc_MemoryError, "Failed to create List Object");
                return NULL;
            }
            continue;
        }

        if (key != NULL && value == NULL)
        {
            if (keyCreated == true)
            {
                if (compare_symbols_ptr(element, doubleQuote))
                {
                    value = PyList_New(0);
                    if (value == NULL)
                    {
                        PyErr_Format(PyExc_MemoryError, "Failed to create List Object");
                        return NULL;
                    }
                    isString = true;
                }
                else if
                (
                    compare_symbols_ptr(element, oneChar) ||
                    compare_symbols_ptr(element, twoChar) ||
                    compare_symbols_ptr(element, threeChar) ||
                    compare_symbols_ptr(element, fourChar) ||
                    compare_symbols_ptr(element, fiveChar) ||
                    compare_symbols_ptr(element, sixChar) ||
                    compare_symbols_ptr(element, sevenChar) ||
                    compare_symbols_ptr(element, eightChar) ||
                    compare_symbols_ptr(element, nineChar)
                )
                {
                    value = PyList_New(0);
                    if (value == NULL)
                    {
                        PyErr_Format(PyExc_MemoryError, "Failed to create List Object");
                        return NULL;
                    }
                    isNumber = true;
                    lenValue++;
                    if (PyList_Append(value, element) == -1)
                    {
                        PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                        return NULL;
                    }
                }
                continue;
            }

            if (lenKey > 0 && compare_symbols_ptr(element, doubleQuote))
            {   
                const char* string = PyUnicode_AsUTF8(PyUnicode_Join(
                    PyUnicode_FromString(emptyString),
                    key
                ));
                key = Py_BuildValue("s", string);
                if (key == NULL) {
                    PyErr_Format(PyExc_ValueError, "Failed to build string value");
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
                    PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                    return NULL;
                }
            }
        }

        if (key != NULL && value != NULL)
        {
            if (compare_symbols_ptr(element, doubleQuote) && isString)
            {
                const char* string = PyUnicode_AsUTF8(
                    PyUnicode_Join(PyUnicode_FromString(emptyString), value)
                );
                if (!(value = Py_BuildValue("s", string))) {
                    PyErr_Format(PyExc_ValueError, "Failed to build string value");
                    return NULL;
                }
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    PyErr_Format(PyExc_ValueError, "Failed to set item");
                    return NULL;
                }
                isNumber = false;
                isString = false;
                keyCreated = false;
                key = (PyObject*)NULL;
                value = (PyObject*)NULL;
            }
            else if (
                compare_symbols_ptr(element, commaChar) &&
                isNumber
                )
            {
                PyObject* string = PyUnicode_Join(PyUnicode_FromString(emptyString), value);
                PyObject* tempLong = PyLong_FromUnicodeObject(string, 10);
                value = Py_BuildValue("l", PyLong_AsLong(tempLong));
                if (value == NULL) {
                    PyErr_Format(PyExc_ValueError, "Failed to build integer value");
                    return NULL;
                }
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    PyErr_Format(PyExc_ValueError, "Failed to set item");
                    return NULL;
                }
                isNumber = false;
                isString = false;
                keyCreated = false;
                key = (PyObject*)NULL;
                value = (PyObject*)NULL;
            }
            else
            {
                lenValue++;
                if (PyList_Append(value, element) == -1)
                {
                    PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                    return NULL;
                }
                continue;
            }
        }
    }
    return Py_BuildValue("O", dict);
}

PyObject* cjson_dumps(PyObject* self, PyObject* args)
{
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict))
    {
       PyErr_Format(PyExc_TypeError, "Expected dict object");
       return NULL;
    }
    const char* emptyString = "";
    const char* spaceString = " ";
    const char* openBracket = "{";
    const char* closeBracket = "}";
    const char* commaChar = ",";
    const char* doubleQuote = "\"";
    const char* colon = ":";
    PyObject* tempItem = NULL;
    PyObject* futureString = NULL;
    if (!(futureString = PyList_New(0))) {
        PyErr_Format(PyExc_MemoryError, "Failed to create List Object");
        return NULL;
    }

    tempItem = PyUnicode_FromString(openBracket);
    if (PyList_Append(futureString, tempItem) == -1)
    {
        PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
        return NULL;
    }

    PyObject* keys = PyDict_Keys(dict);
    Py_ssize_t length = PyObject_Length(keys);
    PyObject* values = PyDict_Values(dict);
    for (Py_ssize_t i = 0; i < length; i++) 
    {
        tempItem = PyUnicode_FromString(doubleQuote);
        if (PyList_Append(futureString, tempItem) == -1)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
            return NULL;
        }
        PyObject* key = PyList_GetItem(keys, i);
        tempItem = PyUnicode_FromObject(key);
        if (PyList_Append(futureString, tempItem) == -1)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
            return NULL;
        }

        tempItem = PyUnicode_FromString(doubleQuote);
        if (PyList_Append(futureString, tempItem) == -1)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
            return NULL;
        }

        tempItem = PyUnicode_FromString(colon);
        if (PyList_Append(futureString, tempItem) == -1)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
            return NULL;
        }
        tempItem = PyUnicode_FromString(spaceString);
        if (PyList_Append(futureString, tempItem) == -1)
        {
            PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
            return NULL;
        }

        PyObject* value = PyDict_GetItem(dict, key);
        tempItem = PyUnicode_FromObject(PyObject_Str(value));
        if (!PyLong_Check(value))
        {
            tempItem = PyUnicode_FromString(doubleQuote);
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
            tempItem = PyUnicode_FromObject(PyObject_Str(value));
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
            tempItem = PyUnicode_FromString(doubleQuote);
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
        }
        else
        {
            tempItem = PyUnicode_FromObject(PyObject_Str(value));
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
        }
        
        if (i != (length-1))
        {
            tempItem = PyUnicode_FromString(commaChar);
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
            tempItem = PyUnicode_FromString(spaceString);
            if (PyList_Append(futureString, tempItem) == -1)
            {
                PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
                return NULL;
            }
        }
    }
    tempItem = PyUnicode_FromString(closeBracket);
    if (PyList_Append(futureString, tempItem) == -1)
    {
        PyErr_Format(PyExc_MemoryError, "Failed to add item to List Object");
        return NULL;
    }
    const char* string = PyUnicode_AsUTF8(PyUnicode_Join(
        PyUnicode_FromString(emptyString),
        futureString
    ));
    return Py_BuildValue("s", string);
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
