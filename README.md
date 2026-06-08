# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
This system covers AI specialization courses' reviews offered by Georgia Tech in their OMSCS program. 
This knowledge is valuable because it helps students make decision on which classes they'll take according to their needs. There is an existing official review website but the reviews are outdated.
<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | OMS Central |  | https://www.omscentral.com/reviews/recent|
| 2 | Reddit | |https://www.reddit.com/r/OMSCS/comments/1mf7kay/ai_has_now_been_added_as_a_specialization/ |
| 3 |Reddit | |https://www.reddit.com/r/OMSCS/comments/kawd2g/order_of_courses_for_ai/ |
| 4 | Reddit| |https://www.reddit.com/r/OMSCS/comments/1p4reqd/computer_suggestions_for_ai_specialization/ |
| 5 | Reddit| | https://www.reddit.com/r/OMSCS/comments/14fm1ss/what_is_the_musttaken_ai_course/|
| 6 |Reddit | | https://www.reddit.com/r/OMSCS/comments/1r8dcqp/how_are_we_feeling_about_ml4t_especially_for/|
| 7 | Reddit| | https://www.reddit.com/r/OMSCS/comments/qropq7/best_class_to_get_a_sense_of_what_aiml_is_all/|
| 8 |Reddit | |https://www.reddit.com/r/OMSCS/comments/r6i9l4/what_classes_outside_your_specialization_are_you/ |
| 9 |Reddit | | https://www.reddit.com/r/OMSCS/comments/18pg1ps/all_courses_ranked_by_difficulty_using_grades_and/|
| 10 | Reddit| | https://www.reddit.com/r/OMSCS/comments/zojljb/best_first_class_to_take/|
| 11 |Reddit | |https://www.reddit.com/r/OMSCS/comments/1ldmwpn/feeling_imposter_syndrome_struggling_in_a/ |
| 12 |Reddit | |https://www.reddit.com/r/OMSCS/comments/1o6k1co/this_class_is_breaking_mesuggestions/ |
| 13 | Reddit| |https://www.reddit.com/r/OMSCS/comments/1pgo5fs/i_got_out_finished_the_program_after_about_3_years/ |
| 14 |Reddit | | https://www.reddit.com/r/OMSCS/comments/1lei7sc/is_taking_omscs_nlp_worth_it_if_i_already_took/|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
700 characters
**Overlap:**
150 characters
**Why these choices fit your documents:**
Most of my documents are Reddit discussions and OMS Central reviews. They are usually short opinion-based posts, not long technical documents. A chunk size of 700 characters keeps enough context to keep a complete student opinion together and still being small enough for focused retrieval. I used a 150-character overlap to reduce the chance of important information being split between chunk boundaries. Before chunking, I cleaned the documents by removing Reddit usernames, vote counts, reply indicators, ads, and other UI-related text.

**Final chunk count:**
496 chunks
---

## Sample Chunks
Chunk 1

Source: ai_ml_classes_feeling.txt

"AI definitely and if you can afford another class, ML4T... AI covers very interesting topics..."

Chunk 2

Source: ml4t_review.txt

"ML4T is a heavily recommended first course for a reason... it was a great exposure for me to see if I wanted to pursue ML further or not."

Chunk 3

Source: finished_program.txt

"ML and AIES. Grade: A for both... ML was still hard but learned a ton and understood analysis of ML algorithms and datasets better."

Chunk 4

Source: class_is_breaking_me.txt

"Yes, been there with RL. The last project was brutal, spent almost 15 hours daily on it for weeks..."

Chunk 5

Source: ai_ml_classes_feeling.txt

"AI4R will give you a sense of AI and a bit of ML as well."
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

all-MiniLM-L6-v2 from Sentence Transformers

**Production tradeoff reflection:**

The all-MiniLM-L6-v2 is lightweight, runs locally, and doesn't require API calls. It performs well for semantic similarity search and keeps development simple. If I were deploying this system for real users and cost was not a concern, I'd consider larger embedding models with stronger semantic understanding and longer context support. I'd also evaluate models specifically optimized for retrieval tasks. The tradeoff would be higher accuracy versus increased latency, storage requirements, and operating costs.

---
## Retrieval Testing

### Query 1
Question:
What courses do OMSCS students commonly recommend as a first course for students interested in AI?

Top Retrieved Chunks:
1. Source: ai_ml_classes_feeling.txt, Distance: 0.4126
2. Source: must_taken_ai_course.txt, Distance: 0.5633 

These chunks are relevant because they directly discuss ML4T workload, usefulness, and student experiences.

### Query 2
Question:
What do students say about ML4T for someone pursuing the AI specialization?

Top Retrieved Chunks:
1. Source: ai_as_spec.txt, Distance: 0.7033
2. Source: ai_ml_classes_feeling.txt, Distance: 0.7203

Why these results are relevant:
The first chunk discuss beginner-friendly AI courses such as AI, KBAI, and ML4T. But it doesn't necessairly find information on someone pursuing this specific specialization.

### Query 3
Question:
Is the OMSCS NLP course worth taking if a student has already taken an NLP course before? 

Top Retrieved Chunks:
1. Source: nlp_class.txt, Distance: 0.3302
--- 

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt instructs the model to answer questions using only the retrieved OMSCS course-review documents. It explicitly tells the model not to use outside knowledge and to respond with "I don't have enough information in the provided documents to answer that" when the retrieved context is insufficient.

**How source attribution is surfaced in the response:**

Source attribution is added programmatically without relying on the LLM. After retrieval, the system records the source filename, chunk ID, and similarity score for each retrieved chunk. These source references are displayed alongside the generated answer so users can see where the information came from.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What courses do OMSCS students commonly recommend as a first course for students interested in AI? | AI, KBAI, ML4T, AI4R are commonly suggested introductory courses.                                          | Recommended AI, KBAI, Game AI, and ML/DL/NLP based on retrieved discussions.                                                    | Relevant           | Partially accurate |
| 2 | What do students say about ML4T for someone pursuing the AI specialization?                        | ML4T is commonly recommended as an introduction to ML but opinions vary on rigor and workload.             | Reported that students often recommend ML4T, but some criticize its rigor and course structure.                                 | Relevant           | Accurate           |
| 3 | What course order do students recommend for completing the AI specialization?                      | Students often suggest a progression such as AI4R/KBAI → ML4T → AI → ML → RL/DL.                           | System responded that it did not have enough information.                                                                       | Partially relevant | Inaccurate         |
| 4 | Which OMSCS courses are frequently described as the most difficult?                                | Courses such as ML, AI, RL, DL, Compilers, Distributed Computing, and GA are often described as difficult. | Identified several difficult courses but noted the documents did not provide a definitive ranking.                              | Relevant           | Partially accurate |
| 5 | Is the OMSCS NLP course worth taking if a student has already taken an NLP course before?          | Students generally say it can still be worthwhile, though there may be overlap with prior NLP coursework.  | Reported that OMSCS NLP can still be valuable, offers challenging assignments, and provides review of concepts despite overlap. | Relevant           | Accurate           |


**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

## Example Responses

**Example**

Question:
What do students say about ML4T?

Response:
Students commonly recommend ML4T as an introductory machine learning course. Several students described it as a good first course, although some criticized its rigor and course administration.

Sources:
- ml4t_review.txt
- oms_reviews.txt

**Example 2**

Question:
Is OMSCS NLP worth taking if I already took Andrew Ng's NLP course?

Response:
Students generally felt the course can still be worthwhile because of the projects and OMSCS-specific perspective, although some overlap with prior NLP coursework may exist.

Sources:
- nlp_class.txt
- oms_reviews.txt

**Out-of-Scope Example**

Question:
What is the best AI program at Stanford?

Response:
I don't have enough information in the provided documents to answer that.
---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What course order do students recommend for completing the AI specialization?

**What the system returned:**

"I don't have enough information in the provided documents to answer that."

**Root cause (tied to a specific pipeline stage):**

This was a retrieval failure. The document order_of_courses_for_ai.txt contains a recommended course sequence, but the embedding model did not rank the most relevant chunk highly enough for generation. The retrieved chunks were related to AI course selection in general but didn't contain the specific recommended ordering. Because the grounding prompt only allows answers from retrieved context, the model correctly declined to answer.

**What you would change to fix it:**

I would improve retrieval by splitting Reddit discussions at comment boundaries instead using fixed-size character chunks. I would also experiment with larger embedding models or add metadata-based filtering to better surface course-ordering discussions.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning document helped me make important design decisions before writing code. By deciding on my chunk size, overlap, embedding model, vector store, and evaluation questions ahead of time, I had a clear roadmap for building the system. The evaluation questions were useful because they gave me concrete retrieval and generation targets to test throughout development.

**One way your implementation diverged from the spec, and why:**

In my original plan, I wanted to treat individual Reddit posts and comments as natural chunks whenever possible and only split very long comments. During implementation, I instead used a  fixed-size chunking approach with 700-character chunks and 150-character overlap because it was simpler to implement consistently in both Reddit discussions and OMS Central reviews. This approach worked pretty well, but I found that some retrieval failures were ocurring when related information was split across chunks or when a chunk contained multiple discussion topics. If I continued developing the project, I would experiment with comment-level chunking and richer metadata to improve retrieval quality.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I provided my document sources, chunking strategy, and pipeline requirements from planning.md and asked for help implementing the document ingestion and chunking pipeline.
- *What it produced:*
It generated Python code for loading documents, cleaning text, splitting documents into chunks, and storing chunk metadata.
- *What I changed or overrode:*
I modified the cleaning process after noticing that Reddit usernames, vote counts, ads, and reply metadata were still appearing in my chunks. I also verified that the chunk size and overlap matched the values specified in my planning document.

**Instance 2**

- *What I gave the AI:*
I provided my retrieval approach and asked for help implementing embeddings with all-MiniLM-L6-v2, ChromaDB storage, and a retrieval function.
- *What it produced:*
It generated code for embedding chunks, storing them in ChromaDB, retrieving the top-k results, and connecting retrieval to a Groq-hosted LLM for grounded generation.
- *What I changed or overrode:*
I tested the retrieval results manually and adjusted the corpus by cleaning several documents before rebuilding the vector store. I also verified that source attribution was added programmatically without relying entirely on the LLM to cite sources.