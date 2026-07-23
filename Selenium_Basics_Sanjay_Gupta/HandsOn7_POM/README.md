# Hands-On 7 – Page Object Model (POM)

## Question 59

### Problem without POM

Suppose the Submit button ID changes from

```
submit
```

to

```
btn-submit
```

In a traditional Selenium framework, every test script that uses

```python
driver.find_element(By.ID, "submit")
```

must be updated.

If there are 50 test cases, all 50 files must be modified.

---

### Solution using POM

In the Page Object Model, the locator is stored only once.

Example

```python
SUBMIT_BUTTON = (By.ID, "submit")
```

If the ID changes to

```python
SUBMIT_BUTTON = (By.ID, "btn-submit")
```

only **one line** needs to be updated.

All tests continue working without modification.

---

### Advantages of POM

- Reusable code
- Better readability
- Easy maintenance
- Centralized locators
- Cleaner test scripts
- Reduced code duplication
