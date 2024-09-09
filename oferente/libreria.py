
from afip import Afip
# CUIT al cual le queremos generar el certificado
tax_id = 23395413929

# Usuario para ingresar a AFIP.
# Para la mayoria es el mismo CUIT, pero al administrar
# una sociedad el CUIT con el que se ingresa es el del administrador
# de la sociedad.
username = "23395413929"

# Contraseña para ingresar a AFIP.
password = "Guitarra327373"

# Alias para el certificado (Nombre para reconocerlo en AFIP)
# un alias puede tener muchos certificados, si estas renovando
# un certificado pordes utilizar le mismo alias
cert_alias = "certifica"

# Creamos una instancia de la libreria
afip = Afip({
    "CUIT": tax_id,
    "access_token": "m3xSl53ql9BT13vaBkkkwq2adIBsiAc2FO30Ggv7EkBR1P6xx39e6N7A9DM5xff8",
    "production": True
})

# Creamos el certificado (¡Paciencia! Esto toma unos cuantos segundos)
res = afip.createCert(username, password, cert_alias)

# Mostramos el certificado por pantalla
print(res["cert"])

# Mostramos la key por pantalla
print(res["key"])

# ATENCION! Recorda guardar el cert y key ya que 
# la libreria por seguridad no los guarda, esto depende de vos.
# Si no lo guardas vas tener que generar uno nuevo con este metodo
