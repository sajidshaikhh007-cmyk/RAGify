






Code information:
The main code is present in the "project" folder
Download the dependencies through the requirements.txt file 
Create your own Api of HuggingFace and Mistral Api

<BR>
<BR>

Execution:
run ---(main.py) file 


COMPLETE WORKFLOW:

PDF
 │
 ▼
Load → Chunk → Embed → Vector DB
                         ▲
                         │
User Question → Embed → Search
                         │
                         ▼
                  Relevant Chunks
                         │
                         ▼
                  Context + Query
                         │
                         ▼
                        LLM
                         │
                         ▼
                     Answer


                  
