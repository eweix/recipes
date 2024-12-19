#!/usr/bin/env python3

import yaml
from slugify import slugify

with open(r"./data/recipes.yaml", "r") as recipes:
    data = yaml.load(recipes)
    for recipe in data:
        recipe["Title"] = recipe["name"]
        slug = slugify(recipe["name"])
        with open(r"./content/" + slug + ".md", "w") as page:
            yaml.dump(recipe, page)
    except yaml.YAMLError as out:
        print(out)
