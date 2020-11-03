# Lexical Neighborhood Density for Hebrew words

A small, simple project for calculating the OLD20 metric of lexical neighborhood density described by [Yarkoni, Balota, & Yap (2008)](https://link.springer.com/article/10.3758/PBR.15.5.971) for a set of Hebrew word lists from [Smith, Walters, & Prior (2019)](https://www.cambridge.org/core/journals/bilingualism-language-and-cognition/article/target-accessibility-contributes-to-asymmetric-priming-in-translation-and-crosslanguage-semantic-priming-in-unbalanced-bilinguals/9E1B273C798D223790FD4DE9CD60FFC4) and two Hebrew lexicons (base and surface) from [MILA](https://yeda.cs.technion.ac.il/).

The word lists are in the files concrete.csv, fillers.csv, and nonwords.csv, and the lexicons are in base_lexicon.csv and surface_lexicon.csv.

The code itself is very simple, so I took the opportunity writing it to improve my coding practices and actively counteract some bad habits I developed as an academic/scientific programmer. Specifically, I wrote this code using test-driven development, I was careful to write docstrings for all of the functions, and I (inadvertently) got myself into some git rabbitholes and then (purposefully) got myself back out.
