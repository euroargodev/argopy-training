**Hint for notebook producers**

- Use [this notebook template](./template_argopy_training_EAONE_soluce.ipynb) to produce yours.

- Use a pre-push hook to clean up notebooks from code soluce:

Create a pre-push hook in your Git repository. Navigate to the `.git/hooks` directory in your repository and create a file named `pre-push` (no file extension). Make sure the file is executable:

```bash
cd /path/to/your/argopy-training-repository/.git/hooks
touch pre-push
chmod +x pre-push
```

Then Edit the `pre-push` file and add the following content:

```bash
#!/bin/sh

# Run the Python script to clean notebooks out of code soluce
python /path/to/your/argopy-training-repository/for_nb_producers/pre-push-hook-clean-notebooks-of-soluce.py

# Add the cleaned notebooks to the staging area
git add *.ipynb

```
don't forget to replace `/path/to/your/argopy-training-repository` with the actual path to your repository.

To test the hook, try pushing a notebook for which named ends `_soluce.ipynb` and that contain cells tagged with `soluce` or starting with `##soluce`. The hook should automatically clean and rename the notebook before the push.
