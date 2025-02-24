from .global_def import command_description
from .global_def import text_descriptions
from .global_def import Resource
from .global_def import CelebrityResource
from .global_def import ResHolder

# собираем ресурсы
res_holder = ResHolder()

__all__ = [
    'command_description',
    'text_descriptions',
    'Resource',
    'CelebrityResource',
    'res_holder',
]
