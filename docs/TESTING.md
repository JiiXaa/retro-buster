# Testing

## Applications used to test the project:

- DBeaver used to test the SQL database

## Manual testing during the development

- [x] VHS Search functionality depending on queries
- [x] Edit the specific VHS entry
- [x] Delete the specific VHS entry (asking user to confirm before entry is deleted)

## Errors during development:

```python
TypeError: 'VhsDetails' object is not iterable
```

The above error did not let me loop over and display the vhs_details tables associated with a VHS tape.
Tried to print all tables in the console and for the "vhs.vhs_details" None was returned. <br>
Found solution for the error in this article:
https://geoalchemy-2.readthedocs.io/en/latest/orm_tutorial.html <br>

**Solution:** <br>

```
"uselist=True" indicates that the property should be loaded as a list, as opposed to a scalar.
```

In the Movie db model uselist was set to False
in the relationship definition. That is the reason why vhs.vhs_details was't a list, but rather a single object of VhsDetails class.
