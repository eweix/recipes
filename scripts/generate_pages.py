#!/usr/bin/env python3

import yaml
from slugify import slugify

with open(r"./data/recipes.yaml", "r") as recipes:
    data = yaml.safe_load(recipes)
    try:
        for recipe in data:
            # get data for recipes set to be shared
            if "shared" in recipe["categories"]:
                recipe["categories"].pop("public")
                recipe["Title"] = recipe["name"]
                slug = slugify(recipe["name"])
                with open(r"./content/recipes/" + slug + ".md", "w") as page:
                    yaml.safe_dump(recipe, page)

            # alternatively, just generate pages for all recipes
            # recipe["categories"].pop("public")
            # recipe["Title"] = recipe["name"]
            # slug = slugify(recipe["name"])
            # with open(r"./content/recipes/" + slug + ".md", "w") as page:
            #     yaml.safe_dump(recipe, page)
    except yaml.YAMLError as out:
        print(out)
