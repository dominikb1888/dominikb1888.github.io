---
title: "Refactoring Exercise (2/3) - Making use of Pythons Built-in Powers"
date: 2022-02-01T08:15:53+02:00
draft: false
---


# The cleaning story continued - Built-Ins are coming!


In the first post, we looked at cleaning our code on the block level. We identified two import blocks we moved to a separate function, several similar blocks of mappings we replaced with a for loop.

In this post, we will look at the next level of granularity. We will check the code for further repetitions and see where code style can be improved to become less imperative.

This will require some more thinking toward what the code does or tries to achieve. Therefore we look at the data structures and their transformations first. The best way to do this quickly and to also see iteratively how things change is in a Jupyter Notebook.

We look at three Transformations:
1. CSV -> csv_data
2. csv_data to mapped
3. mapped to output


## CSV Import

The CSV Import has been moved to a separate function. Here is our snippet again:

```python {}

class FundingRaised:
    def _import_csv(filepath="../startup_funding.csv"):
        with open(filepath, "rt") as csvfile:
            data = csv.reader(csvfile, delimiter=",", quotechar='"')
            # skip header
            next(data)
            csv_data = []
            for row in data:
                csv_data.append(row)

    return csv_data
```

A CSV file is a set of lines with comma-separated content. Usually there is a header line in line 1 and content in all following lines. With linear reading, we will thus receive lines represented as list of elements. We are checking just the commands inside our functions:

```python {}
import csv

with open("../startup_funding.csv", "rt") as csvfile:
    data = csv.reader(csvfile, delimiter=",", quotechar='"')
    # skip header
    next(data)
    csv_data = []
    for row in data:
        csv_data.append(row)

csv_data

```

The only change to the previous code snippet is that we remove the function name and return value. Instead we reference the csv file directly and call the variable csv_data directly to see the output. Don't forget to import the csv module in the code cell you are using.

If we analyze the output we can see that we receive a list of list with no headers. This is the first hint to problems in the code. Why would I remove the headers from a table on import just to remap them later. Very weird. Let's try to verify this assumption by checking the next steps!


## csv_data -> mapped

How does the transformation of our list continue? Let's look the where function first.

The first step in this transformation is a filter operation, and a weird one two. We need to remap the position of our original header (we placed this information in a dict to clean up before) to the position in our list. I added comments to each line of code in plain English.  


```python {}
# We need to keep an order of the columns to make sure we can remap that to the content our csv_data list of lists. 
columns_dict = {1: "company_name", 4: "city", 5: "state", 9: "round"}
# To filter we need to first check for all options in above dict. Apparently our users aren't allowed to search for something else. This is business logic. We will discuss this later!
for key, column in columns_dict.items():
    # We will only take columns from the options dict our user passes that match our columns_dict above. 
    if column in options:
        # Create a temp list to hold our filtered results
        result = []
        for row in csv_data:
            # Let's iterate through our csv_data and see if the search term from our users options occurs in the right column within our csv_data
            if row[key] == options[column]:
                # if yes, we append this to our result list, i.e. a valid search result!
                result.append(row)
                
        # We overwrite our csv_data Variable, with our search result, mmmmmm                
        csv_data = result

```

Ui, ui. So basically our brief search implementation needs to keep a strict regist dominikb1888er of our column order to work. Otherwise we would not be able to match our users search request to the right column in our list of lists (aka a very bad version of a database).

I wonder what happens, if we remove the check for only these 4 columns and allow for all. If our test cases, which are describing the business logic do not test for any edge case here, we could just throw this line out. So, let's do this!

{{< gist dominikb1888 511582066f7e2b0c7f7ef0362f633222 >}}

The code passes all tests without any issues. This means either the code was implementing something the client never wanted or the product manager didn't specify a proper test suite. For us this does not matter for the moment. Our concern is making all tests pass.

Let's reflect on this code though. It looks a lot cleaner now, but a lot more as also become useless. Our Checking block is still necessary. However, the mapping block after needs to be questioned. If there is no need to check the options for certain column headers, which reason does the separation of headers and code have. Why would we need to map that code into a list of dicts in our final step in the function? Not at all, correct. We could start using a list of dicts right from the start and filter each line.

## Functions from Heaven - csv.DictReader()

Thanks to everyone involved in the python standard library. The CSV Module contains a way to not only read a CSV into a list lists, but to transpose this into a list of dicts with column headers as keys, and data values as dict values. Just like this:

```{Python}

[
    { 
         'header1': 'value',
         'header2': 'value',
    },
    {
         'header1': 'value',
         'header2': 'value',
    },
    
   # <...>
]

```

Let's see which changes we need to apply to the code when using this approach. We receive a correctly transposed CSV Table as a list of dicts right after import. So, we can directly filter on each line of this list.

First our new _import_csv() function:

```python {}

def _import_csv(filepath="../startup_funding.csv"):
    with open(filepath, "rt") as csvfile:
        return [row for row in csv.DictReader(csvfile, delimiter=",", quotechar='"')]
```

We added a little list comprehension to transform the Reader object containing a dict to a list of dicts. Just as we needed it. If we test this in our notebook, the output is fine. However, suddenly our tests do not pass anymore. Now this becomes interesting!

## A Union for the Options

Our for loop from before need to be able to filter through multiple columns - as many as the user passed to our function - and add the results to the result list. If we implement this in analogy to the previous expressive function, we discover that both where and find_by assume the presence of both options for a successful match (AND). We can translate this to make sure the options dictionary is a subset of the row while iterating through each row. How might we do this?

```python

[row for row in self.data if row | options == row]

```

As simple as the above one-liner! We can iterate through each row of our dataset and check if our options dict is an exact subset, i.e. all key-value-pairs in options match the corresponding key-value-pairs in our csv_data-row. This is the check we need for this:

```python {}
# Comparing two dicts using bitwise-or (aka Pipe)
(row | options) == row

# Alternative using Tuples
options.items() <= row.items()

```

[ ] The "|" operator can be used on Dicts since Python 3.9: https://www.python.org/dev/peps/pep-0584/. It allows creating the union of two dicts on both keys and values. If the options dict contains values also contained in the row dict, then both will be identical. If the options dict contains values that are not in the row dict, the row dicts values will be overwritten temporarily for the sake of comparing it to the original row dict. Obviously those do not match and hence the check fails.


Other potential logical Operators would be 

```python {}

intersection = dict(dict1.items() & dict2.items())
union = dict(dict1.items() | dict2.items())
difference = dict(dict1.items() ^ dict2.items())

```

After some cleanup our code looks like this:

{{< gist dominikb1888 f6912fd5617cd38be9843d1b35c6bd50 >}}

We moved the comprehension statement from our two functions into one staticmethod _filter which get's the data, filters it and returns a generator. We can render this generator as a list (where() function) or return the first item from it (next() in find_by() function).

Pretty clean now? 
In the next post we are extending the use case and will add some more Quality. Let's focus some more on patterns to secure professional code and safety a lot more. 
