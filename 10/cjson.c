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
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }
    const char* emptyString = "";
    const char* openBracket = "{";
    const char* closeBracket = "}";
    const char* commaChar = ",";
    const char* doubleQuote = "\"";
    const char* colon = ":";
    const char* oneChar = "1";
    const char* twoChar = "2";
    const char* threeChar = "3";
    const char* fourChar = "4";
    const char* fiveChar = "5";
    const char* sixChar = "6";
    const char* sevenChar = "7";
    const char*eightChar = "8";
    const char* nineChar = "9";
    if (length_unicode_json_str)
    {
        if(
            PyUnicode_Count(json_str, PyUnicode_FromString(openBracket), 0, 2) == 0 &&
            PyUnicode_Count(json_str, PyUnicode_FromString(closeBracket), length_unicode_json_str-2, length_unicode_json_str) == 0
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
        if (key != NULL)
        {
            printf("key - %s %d\n", PyUnicode_AsUTF8(key), PyObject_Length(key));
        }
        if (value != NULL)
        {
            printf("value - %s %d\n", PyUnicode_AsUTF8(value), PyObject_Length(value));
        }

        if (key == NULL && value == NULL && compare_symbols_ptr(element, doubleQuote))
        {
            lenKey++;
            key = PyList_New(0);
            if (key == NULL) {
                printf("ERROR: Failed to create List Object\n");
                return NULL;
            }
            printf("создаем ключ\n");
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
                        printf("ERROR: Failed to create List Object\n");
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
                        printf("ERROR: Failed to create List Object\n");
                        return NULL;
                    }
                    isNumber = true;
                    lenValue++;
                    if (PyList_Append(value, element) == -1)
                    {
                        printf("ERROR: Failed to add item to List Object\n");
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
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }
                printf("ключ собрали %s\n", string);
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

        if (key != NULL && value != NULL)
        {
            printf("тут");
            printf("dq %d", compare_symbols_ptr(element, doubleQuote));
            printf("comma %d", compare_symbols_ptr(element, commaChar));
            if (compare_symbols_ptr(element, doubleQuote) && isString)
            {
                const char* string = PyUnicode_AsUTF8(
                    PyUnicode_Join(PyUnicode_FromString(emptyString), value)
                );
                if (!(value = Py_BuildValue("s", string))) {
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    return NULL;
                }
                isNumber = false;
                isString = false;
                key = (PyObject*)NULL;
                value = (PyObject*)NULL;
                printf("собрали значение");
                if (key == NULL) {
                    printf("key none");
                }
                if (value == NULL) {
                    printf("value none");
                }
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
                    printf("ERROR: Failed to build integer value\n");
                    return NULL;
                }
                lenValue = 0;
                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    return NULL;
                }
                isNumber = false;
                isString = false;
                key = (PyObject*)NULL;
                value = (PyObject*)NULL;
                printf("собрали значение");
                if (key == NULL) {
                    printf("key none");
                }
                if (value == NULL) {
                    printf("value none");
                }
            }
            else
            {
                lenValue++;
                if (PyList_Append(value, element) == -1)
                {
                    printf("ERROR: Failed to add item to List Object\n");
                    return NULL;
                }
                continue;
            }
        }
    }
    return dict;
}

PyObject* cjson_dumps(PyObject* self, PyObject* args)
{
    PyObject* dict;
    PyObject* json_str;
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
    }
    return json_str;
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
