from typing import Dict, Optional
from datetime import datetime

class Product:
    """Model representing a product (software/source code)"""
    
    def __init__(
        self,
        id: int = None,
        name: str = None,
        description: str = None,
        price: float = None,
        category_id: int = None,
        file_path: str = None,
        preview_image: str = None,
        created_at: str = None,
        updated_at: str = None,
        is_active: bool = True
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.file_path = file_path
        self.preview_image = preview_image
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.is_active = is_active
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create a Product instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            category_id=data.get('category_id'),
            file_path=data.get('file_path'),
            preview_image=data.get('preview_image'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            is_active=bool(data.get('is_active', True))
        )
    
    def to_dict(self) -> Dict:
        """Convert Product instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'file_path': self.file_path,
            'preview_image': self.preview_image,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_active': self.is_active
        }
    
    def __str__(self) -> str:
        """String representation of the product"""
        return f"{self.name} - ${self.price}" 