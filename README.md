# Amazon_TopRated_Product

A simple product recommendation web application built with Flask, using natural language processing and vector similarity to recommend top-rated Amazon products from a dataset.

This project loads product data, processes text features (name, category, description, reviews), computes vector embeddings, and returns the most relevant top-rated products for a user‑searched query.

**🧠 Features**

* Search for products by name or keywords
* Recommends top 10 products based on textual similarity and normalized rating
* Integrates Word2Vec embeddings for semantic matching
* Uses a Flask web front‑end to display results

**🚀 Demo**

When the user enters a product query on the homepage, the app:

- Processes the input text
- Converts all products to vector embeddings using Word2Vec
- Computes similarities with each product
- Ranks them using combined similarity + rating score
- Displays the Top 10 products with details

**📁 Project Structure**

- amazon_dataset.csv        # Dataset of Amazon products
- app.py                   # Flask application
- product_model.py         # Recommendation engine module
- templates/
   -Find_Product.html    # Frontend template
- README.md                # Project documentation


**📌 Example Usage**

Search for: Wireless headphones

The app returns the top 10 products from amazon_dataset.csv that are most semantically similar and have high ratings.
