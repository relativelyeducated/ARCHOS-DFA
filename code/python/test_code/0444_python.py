# From: GEEKOM A9 Max AI Performance Overview
# Date: 2025-10-07T22:23:36.064000
# Context: ### Best Ways to Find Patterns in ~200 AI Chat Threads on the Same Topic

Analyzing patterns across 200 AI chat threads (e.g., user queries, AI responses, conversation flows, or emergent themes) on a ...

import pandas as pd
   from sklearn.feature_extraction.text import CountVectorizer
   from sklearn.decomposition import LatentDirichletAllocation
   import matplotlib.pyplot as plt
   from wordcloud import WordCloud  # pip install wordcloud

   # Step 1: Load & Prep Data
   df = pd.read_csv('chats.csv')  # Columns: 'thread_id', 'message'
   # Filter to topic (e.g., contains 'AI ethics')
   df_topic = df[df['message'].str.contains('AI ethics', case=False, na=False)]
   texts = df_topic['message'].dropna().tolist()  # ~thousands of messages across 200 threads

   # Step 2: Vectorize (Bag-of-Words)
   vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english', max_features=1000)
   dtm = vectorizer.fit_transform(texts)

   # Step 3: Fit LDA Model (e.g., 5 topics)
   lda = LatentDirichletAllocation(n_components=5, random_state=42)
   lda.fit(dtm)

   # Step 4: Extract & Visualize Patterns
   # Top words per topic
   for i, topic in enumerate(lda.components_):
       top_words = [vectorizer.get_feature_names_out()[idx] for idx in topic.argsort()[-10:]]
       print(f"Topic {i}: {', '.join(top_words)}")

   # Word Cloud for Topic 0
   wc = WordCloud(width=800, height=400).generate(' '.join([vectorizer.get_feature_names_out()[i] for i in lda.components_[0].argsort()[-50:]]))
   plt.imshow(wc, interpolation='bilinear')
   plt.axis('off')
   plt.show()

   # Assign topics to messages (for per-thread patterns)
   topic_scores = lda.transform(dtm)
   df_topic['topic'] = topic_scores.argmax(axis=1)
   thread_topics = df_topic.groupby('thread_id')['topic'].agg(['value_counts'])  # Patterns per thread
   print(thread_topics.head())  # E.g., Thread 1: Mostly Topic 2 (ethics concerns)