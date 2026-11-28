"""Pruebas escritas desde los casos de abuso (fase 4).

Reglas:
* Cada prueba lleva @pytest.mark.caso_abuso(N), donde N es el número del issue
  del caso de abuso del que sale.
* La prueba afirma el comportamiento seguro, el «Entonces» del requerimiento.
  Por eso falla mientras la app siga vulnerable: rojo esperado en la fase 4.
* Cuando el equipo corrige la debilidad (fase 5), la prueba suma
  @pytest.mark.corregida y el gate del release exige que pase.

Ejecución local, con la app levantada (bash lab/app.sh levantar):
    pytest seguridad/fase-4/pruebas -v
"""

import pytest
import random
import string
import time

def registro(sesion, app_url):
  usuario = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
  clave = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
  sesion.get(f"{app_url}/register")
  datos = {
    "username": usuario,
    "email": f"{usuario}@ejemplo.com",
    "password1": clave,
    "password2": clave,
    "csrfmiddlewaretoken": sesion.cookies.get("csrftoken"),
  }
  info = sesion.post(f"{app_url}/register", data=datos, allow_redirects=False)
  assert info.status_code == 302, f"no se pudo registrar ({info.status_code}) (error NO relacionado al ataque)"
  sesion.cookies.clear()
  return usuario, clave

def iniciar_sesion(sesion, app_url, usuario, clave):
  sesion.get(f"{app_url}/login/")
  datos = {
    "username": usuario,
    "password": clave,
    "csrfmiddlewaretoken": sesion.cookies.get("csrftoken"),
  }
  info = sesion.post(f"{app_url}/login/", data=datos, allow_redirects=False)
  assert info.status_code == 302, f"no se pudo iniciar sesión ({info.status_code}) (error NO relacionado al ataque)"

@pytest.mark.caso_abuso(8)  
def test_no_permite_cierre_de_sesion(app_url, sesion):
  """Dado un usario con sesión iniciada 
  Cuando solicitar finalizar la sesión 
  Entonces el servidor rechaza la solicitud y no cierra la sesión"""
  usuario, clave = registro(sesion, app_url)
  iniciar_sesion(sesion, app_url, usuario, clave)
  mensaje = sesion.get(f"{app_url}/logout/", allow_redirects=False)
  assert mensaje.status_code == 405, f"No se cerró la sesión apropiadamente ({mensaje.status_code})"

@pytest.mark.caso_abuso(4)  
def test_comportamiento_apropiado_SQLi(app_url, sesion):
  """Dado un atacante en el formulario de registro
  Cuando intenta un SQLi en el nombre de usuario
  Entonces el rechaza el intento o acepta el texto"""
  sesion.get(f"{app_url}/register")
  datos = {
    "username": "admin' OR '1'='1' --",
    "email": "malvado@ejemplo.com",
    "password1": "clave",
    "password2": "clave",
    "csrfmiddlewaretoken": sesion.cookies.get("csrftoken"),
  }
  mensaje = sesion.post(f"{app_url}/register", data=datos, allow_redirects=False)
  assert mensaje.status_code < 500, f"Ante un intento de SQLi se retornó {mensaje.status_code}"

@pytest.mark.corregida
@pytest.mark.caso_abuso(7)  
def test_tiempo_limite_por_inactividad(app_url, sesion):
  """Dado un usuario con sesión iniciada
  Cuando ha sido inactivo por más de 40 minutos
  Entonces se cierra la sesión"""
  usuario, clave = registro(sesion, app_url)
  iniciar_sesion(sesion, app_url, usuario, clave)
  cookie = next(c for c in sesion.cookies if c.name == "sessionid")
  vigencia = cookie.expires - time.time()
  assert vigencia <= 40 * 60, "La sesión se mantiene abierta más de 40 minutos"

RUTA_INEXISTENTE = "/ruta-que-no-existe-lab-fase-5/"
MARCADOR_MODO_DEPURACION = "DEBUG = True"

@pytest.mark.corregida
@pytest.mark.caso_abuso(4)
def test_error_no_expone_informacion_interna(app_url, sesion):
  """Dado un visitante que pide una ruta inexistente
  Cuando la app responde con un error
  Entonces la respuesta no muestra la página de depuración de Django"""
  respuesta = sesion.get(f"{app_url}{RUTA_INEXISTENTE}", allow_redirects=False)
  assert MARCADOR_MODO_DEPURACION not in respuesta.text, "La respuesta de error expone la página de depuración"
  
RUTA_LOGIN = "/login/"
NOMBRE_CABECERA_CSP = "Content-Security-Policy"
DIRECTIVA_BASE_CSP = "default-src"

@pytest.mark.corregida
@pytest.mark.caso_abuso(4)
def test_cabecera_csp_presente(app_url, sesion):
  """Dado un visitante de la página de login
  Cuando la solicita
  Entonces la respuesta incluye una política Content-Security-Policy con directiva base"""
  respuesta = sesion.get(f"{app_url}{RUTA_LOGIN}", allow_redirects=False)
  politica = respuesta.headers.get(NOMBRE_CABECERA_CSP, "")
  assert DIRECTIVA_BASE_CSP in politica, "Falta la cabecera Content-Security-Policy"