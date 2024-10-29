from producto.models import Categoria, Subcategoria


def base_categorias(request):
    categorias = Categoria.objects.all()
    categorias_con_subcategorias = {}
    for categoria in categorias:
        subcategorias= Subcategoria.objects.filter(categoria=categoria)
        # Añade al diccionario la categoría junto con sus subcategorías
        categorias_con_subcategorias[categoria] = subcategorias
    
    return  {
        'categorias':categorias,
        'categorias_con_subcategorias':categorias_con_subcategorias
        }