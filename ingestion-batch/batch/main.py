import sys

from loguru import logger

from .elasticsearch_client import ESClient
from .processor import Processor
from .scrapbox import ScrapboxClient


def main():
    logger.info("Starting ingestion batch...")
    
    scrapbox = ScrapboxClient()
    es = ESClient()
    processor = Processor()
    
    try:
        # ES インデックスの初期化
        es.create_index()
        
        # Scrapbox から全ページ取得
        pages = scrapbox.get_all_pages()
        logger.info(f"Retrieved {len(pages)} pages from Scrapbox")
        
        all_processed_docs = []
        for page in pages:
            docs = processor.process_page(page)
            all_processed_docs.extend(docs)
            
            # メモリ節約のために一定数溜まったらバルクインサートする
            if len(all_processed_docs) >= 50:
                es.bulk_index(all_processed_docs)
                all_processed_docs = []
        
        # 残りをインサート
        if all_processed_docs:
            es.bulk_index(all_processed_docs)
            
        logger.info("Ingestion batch completed successfully.")
        
    except Exception as e:
        logger.error(f"Batch failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
