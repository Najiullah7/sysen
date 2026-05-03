# Lab AI Reporter — Process and Iteration

**Prompt design choices:** The prompt asks for a structured report (summary, key insights as bullets, one recommendation) and specifies markdown format and length (about 150–200 words). This keeps the output consistent and readable. The data sent to the AI is a compact text summary (column names, sample rows, and a few more rows as JSON) so the model sees the structure and values without excessive tokens.

**How I iterated:** I started with a broad request (“summarize this data”) and then added the three-part structure and bullet/paragraph instructions so the report had clear sections. I specified “2–3 short paragraphs” and “3–4 bullet points” to avoid overly long or vague output. Testing showed that including both a small JSON sample and a short description of columns improved the model’s ability to name fields (e.g., ESTAB, RCPTOT, EMP) correctly in the report.
