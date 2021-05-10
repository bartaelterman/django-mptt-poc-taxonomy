# Taxonomy and traits poc

This repository contains some code to do a proof of concept of
modeling, storing and querying taxonomy and traits information
using django and [mptt](https://django-mptt.readthedocs.io/en/latest/).

The main project, `mptt_poc` contains some apps:

- `mptt_poc`: main app including settings modules.
Some of the examples are included in the `urls.py` here
so you can see them. Check out that file to see how to access
them.
- `mptt_tutorial`: very basic first mptt model and query.
- `taxonomy`: a proof of concept (quite extensive already)
to model taxonomic information.
- `traits`: a proof of concept to model traits information.
This is still pretty basic and a work in progress.