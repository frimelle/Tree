Tree
====

simple version of tree-of-life (https://github.com/frimelle/tree-of-life)

Needs on of the dumps from wikidata (https://dumps.wikimedia.org/other/wikidata/)

Right now it's using 20140922.json.gz

Creates a Python tree using data from wikidata (wikidata.org) and creates two files:

tree.txt:
is a file with all the nodes of the Biota tree with their level in the tree

roots.txt:
is a file with all the nodes that have no parents bur a child/children and need to be integrated in the biota tree on wikidata
(The file should include biota (Q2382443), too)
