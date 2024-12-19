from producto.models import Categoria, Subcategoria
from oferente.models import Oferente


def base_categorias(request):
    categorias = Categoria.objects.filter(eliminado=False)
    categorias_con_subcategorias = {}
    for categoria in categorias:
        subcategorias= Subcategoria.objects.filter(categoria=categoria)
        # Añade al diccionario la categoría junto con sus subcategorías
        categorias_con_subcategorias[categoria] = subcategorias
    
    return  {
        'categorias':categorias,
        'categorias_con_subcategorias':categorias_con_subcategorias
        }

def comercio_context(request):
    """
    Contexto global para verificar si el usuario tiene un comercio registrado.
    """
    if request.user.is_authenticated:
        tiene_comercio = Oferente.objects.filter(id_usuario=request.user).exists()
    else:
        tiene_comercio = False

    return {'tiene_comercio': tiene_comercio}

