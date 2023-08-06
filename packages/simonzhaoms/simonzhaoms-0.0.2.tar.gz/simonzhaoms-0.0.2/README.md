# Toy Package for Testing Code Coverage #

<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/simonzhaoms/python-code-coverage-test/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-55%25-orange.svg" /></a><br/><details><summary>Coverage Report</summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td colspan="5"><b>simonzhaoms</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/simonzhaoms/python-code-coverage-test/blob/main/simonzhaoms/coverage.py">coverage.py</a></td><td>11</td><td>5</td><td>55%</td><td><a href="https://github.com/simonzhaoms/python-code-coverage-test/blob/main/simonzhaoms/coverage.py#L10">10</a>, <a href="https://github.com/simonzhaoms/python-code-coverage-test/blob/main/simonzhaoms/coverage.py#L13-L16">13&ndash;16</a></td></tr><tr><td><b>TOTAL</b></td><td><b>11</b></td><td><b>5</b></td><td><b>55%</b></td><td>&nbsp;</td></tr></tbody></table></details>
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 1 | 0 :zzz: | 0 :x: | 0 :fire: | 0.086s :stopwatch: |

<!-- Pytest Coverage Comment:End -->

## Conda Env Setup ##

```bash
conda create -n simonzhaoms python=3.10
conda activate simonzhaoms
pip install -e .        # Install the toy package
pip install pytest      # For testing
pip install pytest-cov  # For code coverage
```


## Pytest ##

```bash
# '--import-mode=append' means using installed toy package.
# But it also works without '--import-mode=append'.
pytest --import-mode=append tests/
```


## Code Coverage ##

```bash
# '--cov=simonzhaoms' means generating code coverage for the path specified.
pytest --import-mode=append --cov=simonzhaoms tests/

# '--cov-report=html' indicates the file type for code coverage report,
# and it will be saved into the 'htmlcov' directory by default.
pytest --import-mode=append --cov=simonzhaoms --cov-report=html tests
```


## References ##

* The code example is from [Testing and Code coverage with
  Python](https://github.com/IBM/IBMDeveloper-recipes/blob/main/testing-and-code-coverage-with-python/index.md).
* pytest-cov: pytest plugin that uses coverage as a backend
    + [docs](https://pytest-cov.readthedocs.io/en/latest/)
        - [Tox](https://pytest-cov.readthedocs.io/en/latest/tox.html)
    + [PyPI](https://pypi.org/project/pytest-cov/)
* coverage
    + [docs](https://coverage.readthedocs.io/en/latest/index.html)
    + [PyPI](https://pypi.org/project/coverage/)
* PyCharm
    + [Code Coverage](https://www.jetbrains.com/help/pycharm/code-coverage.html)
* Best practices
    + [How to use code coverage in Python with
      pytest?](https://breadcrumbscollector.tech/how-to-use-code-coverage-in-python-with-pytest/)
    + [Improve Code Quality Using Test
      Coverage](https://www.codemag.com/article/1701081/Improve-Code-Quality-Using-Test-Coverage)
* GitHub Actions
    + [Pytest Coverage
      Comment](https://github.com/marketplace/actions/pytest-coverage-comment)
        - [Update Coverage on Readme](https://github.com/MishaKav/pytest-coverage-comment/blob/main/.github/workflows/update-coverage-on-readme.yml)
    + [Git Auto Commit](https://github.com/marketplace/actions/git-auto-commit)
    + [pytester-cov](https://github.com/marketplace/actions/pytester-cov)
