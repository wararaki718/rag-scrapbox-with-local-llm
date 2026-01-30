from batch.processor import Processor


def test_split_text():
    processor = Processor()
    text = "a" * 1000
    chunks = processor.split_text(text)
    
    # 500 characters chunk with 50 overlap
    # 1: 0-500
    # 2: 450-950
    # 3: 900-1000
    assert len(chunks) == 3
    assert len(chunks[0]) == 500
    assert len(chunks[1]) == 500
    assert len(chunks[2]) == 100

def test_split_text_empty():
    processor = Processor()
    chunks = processor.split_text("")
    assert chunks == []
