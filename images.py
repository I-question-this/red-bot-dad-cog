#!/usr/bin/env python3
import argparse
import json
import os
import random
random.seed()
import requests
from typing import Iterable

# Set up the file path to the json file which acts as our database.
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_JSON = os.path.join(FILE_DIR, "images.json")

# Open up the database of images
with open(IMAGES_JSON) as fin:
    IMAGES = json.load(fin)


def image_urls_in_category(category:str) -> Iterable[str]:
    """Yield all urls within the specified category
    
    Parameters
    ----------
    category: str
        The category to filter urls by.

    Returns
    -------
    Iterable[str]
        The yielded urls with a matching category.
    """
    for img in IMAGES:
        if category in img["categories"]:
            yield img["url"]


def random_image_url_in_category(category:str) -> str:
    """Return random url in selected category.
    Note, it will fail if there are no images in the selected category.

    Parameters
    ----------
    category: str
        The category to find an image in.

    Returns
    -------
    str
        The url of the selected image.
    """
    return random.choice(list(image_urls_in_category(category)))


def add_url(url:str, categories:list[str]) -> None:
    """Add a new image to the database of images.
    Note, if the url already exists then it will instead add the given
    categories to the already existing list.

    Parameters
    ----------
    url: str
        The url of the image to save.
    categories: list[str]
        The list of categories that apply to this image.
    """
    # Check if the given url already exists
    already_existed=False
    for ind in range(len(IMAGES)):
        if url == IMAGES[ind]["url"]:
            already_existed = True
            # Combine the categories
            cats = set()
            for cat in IMAGES[ind]["categories"]:
                cats.add(cat)
            for cat in categories:
                cats.add(cat)
            IMAGES[ind]["categories"] = list(set(cats))

    if not already_existed:
        IMAGES.append({
            "url": url,
            "categories": categories
            })

    # Save the edits
    with open(IMAGES_JSON, "w") as fout:
        json.dump(IMAGES, fout, indent=1)


def backup_images(backup_dir:str, quiet:bool=False) -> None:
    """Backup all the images to the given directory.

    Parameters
    ----------
    backup_dir: str
        The path of the directory to save the images to.
        If the directory does not exist it will create it, but it
        won't create parent directoriess
    quiet: bool=False
        If true then only when a URL does not work and/or backup
        file does not exist and cant' be created will information
        be printed to the console.
    """
    # Check if backup directory already exist
    if not os.path.isdir(backup_dir):
        # It doesn't exist, so make it
        os.mkdir(backup_dir)
    
    for img in IMAGES:
        # Check URL
        response = requests.get(img["url"])

        # Format the url into a proper file path
        backup_file_name = "-".join(img['url'].split("/"))
        for bad_char in ["?", "/", ":", ".", "="]:
            backup_file_name = backup_file_name.replace(bad_char, "-")

        # Check if backup exists
        full_backup_path = os.path.join(backup_dir, backup_file_name)
        if os.path.isfile(full_backup_path):
            backup_status = True
        else:
            if not response.ok:
                backup_status = False
            else:
                with open(full_backup_path, "wb") as handler:
                    handler.write(response.content)
                backup_status = True
      
        # Output status if allowed
        if not(response.ok and backup_status and quiet):
            print(img["url"])
            print(f"URL Status: {'Good' if response.ok else 'Bad'}")
            print(backup_file_name)
            print(f"Backup Status: {'Good' if backup_status else 'Bad'}")
            print("-"*40)


def parse_arguments(args=None) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    # Top level parser setup
    parser = argparse.ArgumentParser(
            description="Manage the database of Dad's images via adding more "\
                        "or backing them up.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(help="sub-command help")

    # Create parser for the add command
    parser_add = subparsers.add_parser("add", 
            help="Add an image to Dadbot's collection")
    parser_add.add_argument("url", help="The url of the image to add")
    parser_add.add_argument("categories", type=str, nargs="+",
            help="The categories this image is in")
    parser_add.set_defaults(func=add_url)

    # Create parser for the backup command
    parser_add = subparsers.add_parser("backup",
            help="Backup Dad's image collection. "\
                 "Will also check if URLs for backed up images are still "\
                 "valid.")
    parser_add.add_argument("backup_dir",
            help="The file directory to backup the images to.")
    parser_add.add_argument("-q", "--quiet", default=False,
            action="store_true",
            help="Limit output to failed images.")
    parser_add.set_defaults(func=backup_images)

    # Parse arguments
    args = parser.parse_args(args=args)

    # Check if a subcommand was given
    if args.func is None:
        parser.print_help()
        return None
    else:
        return args


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    import sys
    args = parse_arguments()
    try:
        if args is not None:
            # Extract the func argument
            func = args.func
            del args.func
            # Give all other arguments to the selected subcommand
            func(**vars(args))
        sys.exit(0)
    except FileNotFoundError as exp:
        print(exp, file=sys.stderr)
        sys.exit(-1)

