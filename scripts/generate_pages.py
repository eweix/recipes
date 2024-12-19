#!/usr/bin/env python3

import yaml
from slugify import slugify

with open(r"./data/recipes.yaml", "r") as stream:
    data = yaml.safe_load(stream)  # load in data
    recipes = []  # make a list to track recipes
    for recipe in data:
        # get data for recipes set to be shared
        if len(recipe["categories"]) > 0:  # only share if has been categorized
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
