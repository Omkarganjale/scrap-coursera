# scrap-edx

Python Selenium web scrapping bot for parsing meta data of Coursera courses.

---

## Data fields

Description of the data fields

| field   | Description                           |
| ------- | ------------------------------------- |
| subject | Subject of course                     |
| title   | Course Title                          |
| desc    | Course Description                    |
| outcome | What you'll learn                     |
| skills  | Skills you'll gain                    |
| hours   | Average hours per week for completion |
| instit  | Hosting Institute                     |
| level   | Difficulty level of course            |
| lang    | Language-Subtitle                     |
| url     | URL of course                         |
| imgurl  | Course Image                          |

_Note: For a given course all the above fields might not be present, in that case the values will be populated with "NA"_

<br/>

---

<br />

## Configure

<br />

-   ```python
    MAX_COURSES_PER_SUBJECT
    ```

    Is the number of courses user wish to parse per subject

-   ```python
    subjects
    ```

    List of all the subjects which will be processed. <br />
    By default All.<br />
    Following are the subjects which will be processed by default.

    ```python
    Business
    Computer Science
    Data Science
    Health
    Social Sciences
    Physical Science and Engineering
    Information Technology
    Arts and Humanities
    Language Learning
    Personal Development
    Math and Logic
    ```

-   ```python
      driver
    ```

    Install a compatible driver

    Edge users can download webdriver from here:
    https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    ```python
    driver = webdriver.Edge('Path/to/driver')
    ```

    Chrome user's can download webdriver from here:
    https://sites.google.com/chromium.org/driver/

    ```python
    driver = webdriver.Chrome('Path/to/driver')
    ```
