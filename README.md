# NodeRank
Web Content Extraction using the PageRank algorithm to find the element containing the best content.

This project was primarily started as a way to extract quality content from web pages with reasonable accuracy, omitting chrome and other superfluous code, on serverless infrastructures like AWS Lambda. There are still a few hurdles on Lambda like making the Punkt (NLTK) library available and fitting within size restrictions of stored code, but it is doable, where in the case of Dragnet and Boilerpipe, dependancy and size issues make this a very difficult, perhaps impossible, task.

## Running:
``` python
# install requirements `pip install -r requirements.txt`
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
1. A matrix (`sim_mat`) is initialized with zeros and for each pairwise node combintation across the x and y axis. A "proability" is established based on the number of sentences of the child and the distance between the nodes.
1. This matrix is then passed to the networkx PageRank agorithm and the resulting nodes are ranked by relative strength.
1. The top node is returned and the text is gotten using the BeautifulSoup `get_text()` method.
1. We then apply some light NLP post-processing to clean things up a bit more.

## Notes
* To run the Jupyter notebook, you will need to install `dragnet` and `boilerpipe3` via pip.  Tested on Ubuntu.  Had issues installing dragnet on windows due to GNU depencencies.
* If you can think of a way to improve or want to contribute, email me at `jroakes@gmail.com`.
* Hamlet Batista supplied a Colaboraory link [here](https://colab.research.google.com/github/jroakes/NodeRank/blob/master/noderank.ipynb).

## Acknowledgements
* Ideas and code taken from [An Introduction to Text Summarization using the TextRank Algorithm with Python implementation](https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/).





