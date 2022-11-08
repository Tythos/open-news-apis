Open News APIs
==============

This is a collection of modules that give developers a quick and easy way to experiment with ingest and normalization of realtime news traffic from multiple key worldwide journalism sources.

.. contents::

Overview
--------

These sources were originally selected and inspired by the outstanding catalogue of public API lists here:

  https://github.com/public-api-lists/public-api-lists#news

Different APIs have different rate limits on polling. Those are typically documented at the header docstrings for each module, but for surge/testing purposes these limits can typically be overridden with a specific environmental variable value.

The "LICENSE" file indicates an MIT license for the source code in this project, but this does not apply to the content or APIs of the organizations that operate the endpoints utilized. Those typically have their own developer account agreements, including restrictions on commercial use and rate limits. Please refer to the URLs indicated in each of the following subsections for details.

guardian
--------

The "world_content.py" module polls the "content" endpoint for the "world" news section from the UK news publication "The Guardian". Key API documentation can be found here:

  https://open-platform.theguardian.com/documentation/

After registration, you should place your API key in the git-ignored file "api.key" within this folder.

newsapi
-------

The "top_headlines.py" module polls the "top headlines" endpoint from the news aggregator "newsapi"; specific documentation of this endpoint can be found here:

  https://newsapi.org/docs

After registration, you should place your API key in the git-ignored file "api.key" within this folder.

nyt
---

The "times_rss_api.py" and "times_wire_api.py" modules poll the RSS and wire-service endpoints, respectively, from the New York Times API; specific documentation for these endpoints can be found herE:

  https://developer.nytimes.com/

After registration, you should place your API key in the git-ignored file "api.key" within this folder.
