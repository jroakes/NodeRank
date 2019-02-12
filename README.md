# NodeRank
Web Content Extraction using the PageRank algorithm to find the element containing the best content.

This project was primarily started as a way to extract content from web pages with reasonable accuracy, omitting chrome and other superfluous code to get the meat of the content only.

## Running:
``` python
# Put the noderank.py file in your working directory
import noderank
url="https://salience.co.uk/insight/magazine/basic-log-file-analysis/"
content - extract_content_noderank(url=url, timeout=10)
```

## Idea
Since there is a structural relationship between the nodes in the DOM of a webpage, can we use that structure to help identify the parent which is most likely to contain the quality content on the page.

This algorithm does the following.
1. The `body` element of the page is exracted using BeautifulSoup.
1. Unneccesary elements are stripped out of the `body` node. eg. `<script>`, `<style>`, etc.  This can be adjusted to suit your needs.
1. A matrix (`sim_mat`) is initialized with zeros and for each pairwise node combintation across the x and y axis, a "proability" is established based on the number of sentences of the child and the distance between the nodes.
1. This matrix is then passed to the networkx PageRank agorithm and the resulting nodes are ranked by relative strength.
1. The top node is returned and the text is gotten using the BeautifulSoup `get_text()` method.
1. We then apply some light NLP post-processing to clean things up a bit more.





