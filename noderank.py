from bs4 import BeautifulSoup
import random
import math
import string
import re
import numpy as np
import nltk
import networkx as nx

def getUA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]

    return random.choice(uastrings)

def prepare_sentences(text):
    
    # Clean characters
    text = "".join([t for t in text if t.isalnum() or t in string.punctuation or t == ' '])
    
    # Get rid of whitespace characters
    sentences = nltk.sent_tokenize(text)
    text = " ".join([s.strip() for s in sentences])
    
    # Fix puctuation spacing
    text = re.sub(r"(\w{2,})([\.\!\?]+)(\w)", r"\1\2 \3", text)
    
    return text


def find_children(n1, n2):
    
    children1 = [c for c in n1.children]
    children2 = [c for c in n2.children]
    
    for i, children in enumerate([children1,children2]):
        level = 1

        while children:
            lchildren = children
            children = []
            for ch in lchildren:
                if not ch.name:
                    continue
                if ch == n1 or ch == n2:
                    if i == 0:
                        return len( nltk.sent_tokenize(n2.get_text()) ) * ( 1/math.exp(level) )
                    else:
                        return len( nltk.sent_tokenize(n1.get_text()) ) * ( 1/math.exp(level) )
                                        
                children.extend(ch.children)

            level += 1
            
    return 0


def find_content(html):
    
    # Get body and extract out non-content nodes
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('body')
    remove = [s.extract() for s in body(["script", "style","iframe","noscript","nav","footer","header", "svg", "h1","h2", "h3", "h4", "h5", "xml"])]
    text = ""
    
    # Further clean nodes and build a lookup list
    nodes = body.findAll()
    nodes = [n for n in nodes if n.name and n.get_text()]
    nodeix = [i for i,v in enumerate(nodes)]    

    # Build similarity matrix and use number of sentences child resursion depth as metric
    sim_mat = np.zeros([len(nodes), len(nodes)])
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                sim_mat[i][j] = find_children(nodes[i], nodes[j])

    # Run pagerank algorithm on matrix
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    
    # Sort nodex by best and get text of best node
    ranked_nodes = sorted(((scores[i],s) for i,s in enumerate(nodeix)), reverse=True)
    text = nodes[ranked_nodes[0][1]].get_text()
    
    return prepare_sentences(text)


def extract_content_pagerank(url, timeout=10):
    
    headers = {'user-agent': getUA()}
    r = requests.get(url, headers = headers, verify=False, timeout=timeout)
    html = r.content
    return find_content(html)
    

# Test URLS
url="https://www.nytimes.com/2019/02/05/technology/artificial-intelligence-drug-research-deepmind.html"
#url="https://www.houstonchronicle.com/news/investigations/article/Southern-Baptist-sexual-abuse-spreads-as-leaders-13588038.php"
#url="https://www.clearwaycommunitysolar.com/"
#url="https://thenewstack.io/dr-michael-stonebraker-a-short-history-of-database-systems/"

print(extract_content_pagerank(url, timeout=10))
