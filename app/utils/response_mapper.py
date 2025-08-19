from datetime import datetime
from typing import Any, Optional, Dict

class PaginationMeta:
    def __init__(self, current_page: int, total_items: int, items_per_page: int = 16):
        self.current_page = current_page
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.total_pages = (total_items + items_per_page - 1) // items_per_page
        self.has_next = current_page < self.total_pages
        self.has_prev = current_page > 1

    def to_dict(self) -> Dict:
        return {
            "current_page": self.current_page,
            "total_items": self.total_items,
            "items_per_page": self.items_per_page,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev
        }

class ResponseMapper:
    @staticmethod
    def success(status_code: int, message: str, data: Any, pagination: Optional[PaginationMeta] = None) -> Dict:
        """Crear una respuesta exitosa con formato estándar"""
        response = {
            "status_code": status_code,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        if pagination:
            response["pagination"] = pagination.to_dict()
        
        return response

class ErrorResponseMapper:
    @staticmethod
    def error(status_code: int, message: str) -> Dict:
        """Crear una respuesta de error con formato estándar"""
        return {
            "status_code": status_code,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
