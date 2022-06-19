from brownie import Codes, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import inquirer

def main():
    codes = Codes[-1]
    number_of_codes = codes.tokenCounter()
    print(f"There are {number_of_codes} coes")
    for token_id in range(number_of_codes):
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}.json"
        )
        code_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"Metadata file {metadata_filename} already exists")
        else:
            print(f"Creating metadata file {metadata_filename}")
            code_metadata["name"] = input("Enter the name of the code: ")
            code_metadata["description"] = input("Enter the description of the code: ")
            questions = [
                inquirer.List('language',
                    message="What language is the code written in?",
                    choices=['c#', 'c++', 'javascript', 'kotlin', 'php', 'python', 'ruby', 'solidity', 'typescript']
                ),
            ]
            answers = inquirer.prompt(questions)
            code_metadata['language'] = answers['language']
            image_file_name = "./img/" + answers['language'] + "-logo.png"
            image_uri = upload_to_ipfs(image_file_name)
            collectible_metadata["image"] = image_uri


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./image/PUG.png" -> PUG.png
        filename = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
