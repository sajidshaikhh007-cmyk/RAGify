






Code information:
The main code is present in the "project" folder
Download the dependencies through the requirements.txt file 
Create your own Api of HuggingFace and Mistral Api

<BR>
<BR>

Execution:
run ---(main.py) file 


COMPLETE WORKFLOW:



                    ┌─────────────────────┐
                    │      User           │
                    │   Uploads PDF       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Loader       │
                    │ Extract PDF Text    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Splitter     │
                    │ Split into Chunks    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embedding       │
                    │ Text → Vectors      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Vector Store     │
                    │   Store Embeddings  │
                    └──────────┬──────────┘
                               │
                               │
            ┌──────────────────┘
            │
            ▼
┌─────────────────────┐
│    User Question    │
│ "What is RAG?"      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Question Embedding  │
│ Question → Vector   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Similarity Search   │
│ Find relevant       │
│ document chunks     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Context + Question  │
│      ↓              │
│      LLM            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Answer         │
│ Generated using     │
│ retrieved context   │
└─────────────────────┘




