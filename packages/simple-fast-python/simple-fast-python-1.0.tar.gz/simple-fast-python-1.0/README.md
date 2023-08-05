# implementation of SiMPle-Fast in Python

An implementation of matrix profiles in Python using numpy.

## quickstart

```bash
# generate testing data for the directories, ensure that you have octave installed
octave-cli .\tests\resources\reference_simple_fast_self.m
octave-cli .\tests\resources\reference_simple_fast_ab.m

rscript tests/test_tsmp.R
pytest tests
```

### uploading the package

Tag a commit on GitHub and the actions should take care of the rest. To manually upload via twine:

```bash
pipx install twine
python -m build
# upload to testpypi
twine upload --repository testpypi dist/*
twine upload dist/*
```

# references

- https://sites.google.com/view/simple-fast
- https://github.com/matrix-profile-foundation/tsmp
- https://www.kaggle.com/c/birdclef-2021/
- https://github.com/acmiyaguchi/birdclef-2021
