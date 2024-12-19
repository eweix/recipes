# Paprika Cookbook

This is a standalone repository that fetches recipes from [paprika][paprika] and
updates a website with the information. It automatically generates pages for
each website and sorts them by category using Hugo's [taxonomies][taxonomy].

[paprika]: https://www.paprikaapp.com/
[hugo]: https://gohugo.io
[taxonomy]: https://gohugo.io/content-management/taxonomies/

## Setup

1. Fork this repository!
2. Add the following repository secrets:
   - EMAIL: the email you use for your paprika account
   - PASSWORD: the password for your paprika account
3. Allow GitHub actions to commit, pull, and push your repository.
4. Allow GitHub pages to work.

## So how does it work?

The workflow runs on three main parts:

1. Fetch recipes from paprika.
2. Separate recipe archive into individual recipes.
3. Generate webpages from recipes.

The [`recipes.yaml` workflow][wf] is scheduled to run once a week, to respect
the API and because it doesn't realistically need to be updated every day. I
suggest leaving it as is, or setting it up update once per day at MOST.

[wf]: https://github.com/eweix/recipes/blob/main/.github/workflows/recipes.yaml

### 1. Fetching recipes

After setting up the python environment and installing dependencies, the
workflow runs [`scripts/get_recipes.py`][get]. The script fetches recipes from
Paprika and exports them to `data/recipes.yaml`. The script authenticates the
request with Paprika using your own email and password, which is why they must
be set as secrets for the repository. Currently it is configured only to fetch
text, but can be tweaked to fetch photos by uncommenting the commented lines in
the file.

[get]: https://github.com/eweix/recipes/blob/main/scripts/get_recipes.py

### 2. Separating the recipe archive

[`scripts/generate_pages.py`][gen] reads `data/recipes.yaml` and splits it by
recipe, writing the information for each recipe to the frontmatter of a markdown
file. It also slugifies the title and applies some data formatting for Hugo. It
is currently configured to only generate markdown content pages for recipes that
are rated and/or categorized (i.e. recipes that have been used). However, this
can be configured by removing the "if" statement in the python code.

```python
#!/usr/bin/env python3

import yaml
from slugify import slugify

with open(r"./data/recipes.yaml", "r") as stream:
    data = yaml.safe_load(stream)  # load in data
    recipes = []  # make a list to track recipes
    for recipe in data:
        # get data for recipes set to be shared
        if (len(recipe["categories"]) > 0) or (recipe["rating"]>0):
            # format frontmatter for Hugo site generater
            recipe["Title"] = recipe["name"]
            recipe["slug"] = slugify(recipe["name"])

            # save recipe to list
            recipes.append(recipe["name"])

            # write file
            with open(r"./content/recipes/" + recipe["slug"] + ".md", "w") as file:
                file.write("---\n")  # begin frontmatter markup
                yaml.safe_dump(recipe, file)  # dump yaml data for recipe
                file.write("---\n")  # end frontmatter markup
print(recipes)
```

[gen]: https://github.com/eweix/recipes/blob/main/scripts/generate_pages.py
[fm]: https://gohugo.io/content-management/front-matter/#parameters

### 3. Generating the website

The cookbook website is powered by [Hugo][hugo] and comes with its own set of
layouts. Simply using the "on-push" trigger for the Hugo GitHub Pages action
means that the website will regularly be updated with recipes as they are saved!

Note that any edits made to the markdown content files for each recipe will be
overwritten when the recipes workflow fetches new data, since they are
regenerated each time.

## Credits

This work would not be possible without all the previous experimentation and
tools of other dedicated Paprika users. In particular, mattdsteele's [writeup of
the paprika API][api] helped me understand how Paprika syncs and stores recipes,
since the API is not publicly documented. To fetch the data, I used modified
versions of the [Paprika Exporter][papexp] utility developed by Shane Starcher
and Chris Nicholson.

[api]: https://gist.github.com/mattdsteele/7386ec363badfdeaad05a418b9a1f30a
[papexp]: https://github.com/sstarcher/paprika-exporter
