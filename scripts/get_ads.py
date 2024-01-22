import ads
import os
import yaml
import glob
import numpy as np

def make_bib(authors, outfile="../_includes/most_recent_all.bib"):

    with open(outfile, "w+") as out:
        for author in authors:
            # Search for papers by the author, sorted by publication date (most recent first)
            papers = list(
                ads.SearchQuery(
                    q=f'author:"{author}"',
                    fl=[
                        "citation_count",
                        "abbr",
                        "bibcode",
                    ],
                    sort="date desc",  # Sort by publication date in descending order
                )
            )
            
            # Check if there are any papers for the author
            if papers:
                # Get the most recent paper (first paper in the list)
                most_recent_paper = papers[0]
                
                # Export the BibTeX entry for the most recent paper
                bibquery = ads.ExportQuery(most_recent_paper.bibcode)
                bibs = bibquery.execute()
                
                # Write the BibTeX entry to the output file
                out.write(bibs)


def extract_names_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the YAML front matter
    front_matter = []
    in_front_matter = False
    for line in lines:
        if line.strip() == '---':
            if not in_front_matter:
                in_front_matter = True
                continue
            else:
                break
        if in_front_matter:
            front_matter.append(line)
            # print(line)

    # Parse the YAML front matter
    front_matter_str = ''.join(front_matter)
    data = yaml.safe_load(front_matter_str)
    return data.get('title')  # Assuming 'name' is the key for names


def get_names_from_collections(collection_path):
    names = []
    print(collection_path)
    # Iterate over all Markdown files in the collection
    for file_path in glob.glob(os.path.join(collection_path, '*.md')):
        name = extract_names_from_file(file_path)
        if name:
            names.append(name)
    return names

def main():
    collections = ['_pi','_postdocs','_grads','_undergrads']
    names = np.concatenate([get_names_from_collections('../'+folder) for folder in collections ])
    names = [name.split(' ') for name in names]
    names = ['^'+name[-1]+', '+name[0] for name in names]
    sorted_names = sorted(names)
    make_bib(sorted_names,outfile='most_recent_all.bib')


if __name__ == "__main__":
    main()