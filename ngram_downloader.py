import urllib
import urllib2
import urlparse
import json
import math
import time
from pprint import pprint
from cookielib import CookieJar

def add_query_params_to_url(params, url):
    url_parts = list(urlparse.urlparse(url))

    # Add the query to the dictionary of queries
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    # The element at index-4 of url_parts is the query, so reset the query to
    # the newly updated query params.
    url_parts[4]= urllib.urlencode(query)

    return urlparse.urlunparse(url_parts)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Takes in ngrams in a form of a list of tuples:
# i.e. ngrams = [("the", "bug"), ("like", "cat")]
def get_ngram_probabilities(ngrams):
    assert (len(ngrams) > 0)
    results = {}

    num_results_per_query = 50

    for chunk_ngrams in chunks(ngrams, num_results_per_query):
        base_url = "https://books.google.com/ngrams/graph?year_start=1500&year_end=2008&corpus=15&smoothing=1"
        params = {}
        ngrams_space_combined = [" ".join(ngram) for ngram in chunk_ngrams]
        params["content"] = ", ".join(ngrams_space_combined)

        # Form the actual url for querying by appending the content query param
        url = add_query_params_to_url(params, base_url)

        # Get the raw HTML as a string
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        content = opener.open(url).read()

        # In this raw HTML there will be a 'var data' somewhere in a JavaScript
        # <script> tag. We can use this data once we find the beginnings and ends
        # of the declaration for var data by finding the index of the first
        # square bracket following 'var data', and then finding the first semicolon
        # afterwards, and taking the information in between.
        start_index_of_var_data_keyword = content.find("var data")
        start_index_of_data = content.find("[", start_index_of_var_data_keyword)
        end_index_of_data = content.find(";", start_index_of_data)

        # Now that we have the raw data, put it into JSON format so we can parse it.
        raw_data = content[start_index_of_data:end_index_of_data]
        json_data = json.loads(raw_data)

        # Since the data is in order of our query params we can just loop through
        # each individual ngram's data to find it's ranking data.
        for ngram in json_data:
            ngram_tuple = ngram["ngram"]
            timeseries_data = ngram["timeseries"]
            num_data_points = len(timeseries_data)

            if num_data_points > 0:
                results[tuple(ngram_tuple.split())] = (timeseries_data[num_data_points-1])
            else:
                results[tuple(ngram_tuple.split())] = (-1.0)

    # The return value will be a list of floats where each float corresponds to
    # a bigram, in the same order as the passed in bigrams.
    # pprint(results, indent=4)
    return results

def main():
    ngrams = [("the", "bug"), ("like", "cat")]
    print get_ngram_probabilities(ngrams)

if __name__ == '__main__':
    main()