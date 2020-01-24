# hwahae-backend

This is a project for a server programmer skill test.


## Debugging/Testing

Run debug server

```console
$ bash hwahae-backend/run_debug.sh
```

Unit test

```console
$ bash hwahae-backend/run_test.sh
```

## Considerations

Data cleansing

- Normalize string values into lower case to improve efficiency.
- Remove duplicated values. (ingredients)

Data validation

- Prepare for test serializer and endpoint for the data validation include 'score' information. (name='test_data', TestItemSerializer)
- Validate data with jupyter notebook and dump cache for valid data object. (notebook/1_data_validation.ipynb, notebook/test/valid.pickle)
- Add unit test for data validation by using dumped cache. (endpoint name)


## Tech stacks

- REST framework: djangorestframework 3.11.0
- Documentation: drf-yasg 1.17.0


## Todo list

Main workflow:

- [x] Raw data(json) analysis with jupyter notebook
- [x] DB table scheme design
- [x] Dump fixtures(json) from raw data(json)
- [x] Implement initial data part(Procfile, loaddata)
- [x] Validate DB, dump valid data(object for unit test)
- [x] Test QuerySet with shell, prepare for optimized queries
- [x] API implementation (include test API)
- [x] Exception handling - custom exeption handler
- [x] API testing and test code

Code quality:

- [x] Code structure migration

ETC:

- [x] API documentation (drf-yasg)

## References

Best practice of django rest framework

- https://chrisbartos.com/articles/how-to-structure-your-django-app-with-api/
- https://thinkster.io/django-angularjs-tutorial#learning-django-and-angularjs

