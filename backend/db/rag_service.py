from typing import List
from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sqlmodel import select

from backend.db.models import Sources, Chunks
from backend.db.session import AsyncSessionLocal

embed_model = HuggingFaceEmbedding(model_name="GritLM/GritLM-7B")

async def add_document(source: str, meta: dict, text: str):
    """Chunks, embeds, and stores a document in the database."""
    splitter = SemanticSplitterNodeParser(
        buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
    )
    nodes = splitter.get_nodes_from_documents([Document(text=text)])

    async with AsyncSessionLocal() as session:
        source_obj = Sources(source=source, meta=meta)
        session.add(source_obj)
        await session.commit()
        await session.refresh(source_obj)

        for node in nodes:
            embedding = embed_model.get_text_embedding(node.get_content())
            chunk = Chunks(
                source_id=source_obj.id,
                chunk=node.get_content(),
                meta=node.metadata,
                embedding=embedding,
            )
            session.add(chunk)
        await session.commit()

async def retrieve_context(query: str, top_k: int = 5) -> List[str]:
    """Retrieves the top_k most relevant document chunks for a given query."""
    query_embedding = embed_model.get_query_embedding(query)

    async with AsyncSessionLocal() as session:
        statement = (
            select(Chunks)
            .order_by(Chunks.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )
        result = await session.execute(statement)
        chunks = result.scalars().all()

        return [chunk.chunk for chunk in chunks]