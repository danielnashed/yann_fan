

def chunk_text_by_paragraphs(text: str, max_chunk_size: int, min_chunk_size: int) -> list:
    """
    Splits a given text into chunks of 1 to many paragraphs.

    :param text: The input text to be chunked.
    :param max_chunk_size: The maximum size (in characters) allowed for each chunk. Default is 1500.
    :param min_chunk_size: The minimum size (in characters) required for each chunk. Default is 500.
    :return: A list of chunked text, where each chunk contains 1 or multiple paragraphs.
    """
    chunks = []
    current_chunk = ""

    start_index = 0
    while start_index < len(text):
        end_index = start_index + max_chunk_size
        if end_index >= len(text):
            end_index = len(text)
        else:
            # Find the nearest paragraph boundary
            paragraph_boundary = text.find("\n\n", start_index, end_index)
            if paragraph_boundary != -1:
                end_index = paragraph_boundary

        chunk = text[start_index:end_index].strip()
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)
            current_chunk = ""
        else:
            current_chunk += chunk + "\n\n"

        start_index = end_index + 1

    ## Post-loop handling becuase the last chunk may not have been added
    if len(current_chunk.strip()) >= min_chunk_size:
        chunks.append(current_chunk.strip())
    elif chunks:
        chunks[-1] += "\n\n" + current_chunk.strip()
    elif current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks