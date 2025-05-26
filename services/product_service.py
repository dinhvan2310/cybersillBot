from db.repositories.product_repository import ProductRepository
from typing import Optional, List, Dict

class ProductService:
    def __init__(self, db_path='db.sqlite3'):
        self.repo = ProductRepository(db_path)

    def create_product(self, name: str, desc: str, price: float, path: str) -> int:
        return self.repo.add_product(name, desc, price, path)

    def get_product(self, product_id: int) -> Optional[Dict]:
        return self.repo.get_product_by_id(product_id)

    def get_all_products(self) -> List[Dict]:
        return self.repo.get_all_products()

    def update_product(self, product_id: int, name: str, desc: str, price: float, path: str) -> bool:
        return self.repo.update_product(product_id, name, desc, price, path)

    def delete_product(self, product_id: int) -> bool:
        return self.repo.delete_product(product_id) 