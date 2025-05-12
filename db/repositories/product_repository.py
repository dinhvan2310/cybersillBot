import logging
import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional
from models.product import Product
from db.database import get_connection

logger = logging.getLogger(__name__)

class ProductRepository:
    """Repository for product-related database operations"""
    
    @staticmethod
    async def create_product(
        name: str,
        description: str,
        price: float,
        category_id: int = None,
        file_path: str = None,
        preview_image: str = None
    ) -> Optional[Product]:
        """Create a new product entry"""
        async with await get_connection() as db:
            try:
                query = """
                INSERT INTO products (
                    name, description, price, category_id, 
                    file_path, preview_image, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                current_time = datetime.now().isoformat()
                cursor = await db.execute(
                    query, 
                    (name, description, price, category_id, file_path, preview_image, current_time, current_time)
                )
                await db.commit()
                
                # Get the inserted product
                product_id = cursor.lastrowid
                return await ProductRepository.get_product_by_id(product_id)
            except Exception as e:
                logger.error(f"Error creating product: {e}")
                return None
    
    @staticmethod
    async def get_product_by_id(product_id: int) -> Optional[Product]:
        """Get product by ID"""
        async with await get_connection() as db:
            db.row_factory = aiosqlite.Row
            query = "SELECT * FROM products WHERE id = ?"
            cursor = await db.execute(query, (product_id,))
            row = await cursor.fetchone()
            
            if not row:
                return None
                
            return Product.from_dict(dict(row))
    
    @staticmethod
    async def get_all_products(active_only: bool = True, category_id: int = None) -> List[Product]:
        """Get all products, optionally filtered by category and active status"""
        async with await get_connection() as db:
            db.row_factory = aiosqlite.Row
            
            params = []
            query = "SELECT * FROM products WHERE 1=1"
            
            if active_only:
                query += " AND is_active = 1"
                
            if category_id is not None:
                query += " AND category_id = ?"
                params.append(category_id)
                
            query += " ORDER BY name ASC"
            
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            
            return [Product.from_dict(dict(row)) for row in rows]
    
    @staticmethod
    async def search_products(search_term: str, active_only: bool = True) -> List[Product]:
        """Search products by name or description"""
        async with await get_connection() as db:
            db.row_factory = aiosqlite.Row
            
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern]
            
            query = """
            SELECT * FROM products 
            WHERE (name LIKE ? OR description LIKE ?)
            """
            
            if active_only:
                query += " AND is_active = 1"
                
            query += " ORDER BY name ASC"
            
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            
            return [Product.from_dict(dict(row)) for row in rows]
    
    @staticmethod
    async def update_product(
        product_id: int,
        name: str = None,
        description: str = None,
        price: float = None,
        category_id: int = None,
        file_path: str = None,
        preview_image: str = None,
        is_active: bool = None
    ) -> Optional[Product]:
        """Update product details"""
        # Get existing product first
        existing_product = await ProductRepository.get_product_by_id(product_id)
        if not existing_product:
            logger.error(f"Product with ID {product_id} not found for update")
            return None
            
        # Update only the fields that are provided
        update_fields = []
        params = []
        
        if name is not None:
            update_fields.append("name = ?")
            params.append(name)
            
        if description is not None:
            update_fields.append("description = ?")
            params.append(description)
            
        if price is not None:
            update_fields.append("price = ?")
            params.append(price)
            
        if category_id is not None:
            update_fields.append("category_id = ?")
            params.append(category_id)
            
        if file_path is not None:
            update_fields.append("file_path = ?")
            params.append(file_path)
            
        if preview_image is not None:
            update_fields.append("preview_image = ?")
            params.append(preview_image)
            
        if is_active is not None:
            update_fields.append("is_active = ?")
            params.append(1 if is_active else 0)
            
        # Always update the updated_at timestamp
        update_fields.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        
        if not update_fields:
            # No fields to update
            return existing_product
            
        # Add product_id to params
        params.append(product_id)
        
        async with await get_connection() as db:
            try:
                query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
                await db.execute(query, params)
                await db.commit()
                
                return await ProductRepository.get_product_by_id(product_id)
            except Exception as e:
                logger.error(f"Error updating product: {e}")
                return None
    
    @staticmethod
    async def delete_product(product_id: int) -> bool:
        """Delete product (set is_active to false)"""
        async with await get_connection() as db:
            try:
                query = "UPDATE products SET is_active = 0, updated_at = ? WHERE id = ?"
                current_time = datetime.now().isoformat()
                await db.execute(query, (current_time, product_id))
                await db.commit()
                return True
            except Exception as e:
                logger.error(f"Error deleting product: {e}")
                return False 