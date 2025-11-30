# start_web_server.py - Inicia el servidor web para la aplicación
# -----------------------------------------------------------------------------
"""
Script para iniciar un servidor HTTP simple que sirve la aplicación web.
Abre automáticamente el navegador en la dirección correcta.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuración
PORT = 8000
WEB_APP_DIR = Path(__file__).parent / "web_app"

def start_server():
    """Inicia el servidor web y abre el navegador."""
    
    # Cambiar al directorio web_app
    if not WEB_APP_DIR.exists():
        print(f"❌ Error: No se encontró el directorio {WEB_APP_DIR}")
        sys.exit(1)
    
    os.chdir(WEB_APP_DIR)
    
    print("=" * 70)
    print(" " * 15 + "🌐 SERVIDOR WEB - COHETE DE AGUA")
    print("=" * 70)
    print(f"\n📂 Sirviendo archivos desde: {WEB_APP_DIR}")
    print(f"🌍 Puerto: {PORT}")
    print(f"🔗 URL: http://localhost:{PORT}")
    print("\n" + "-" * 70)
    print("💡 INSTRUCCIONES:")
    print("-" * 70)
    print("1. El navegador se abrirá automáticamente")
    print("2. Si no se abre, ve manualmente a: http://localhost:{PORT}")
    print("3. Para DETENER el servidor: Presiona Ctrl+C")
    print("-" * 70)
    
    # Configurar el servidor
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n✅ Servidor iniciado exitosamente en el puerto {PORT}")
            print(f"🚀 Abriendo navegador...")
            
            # Abrir navegador automáticamente
            webbrowser.open(f"http://localhost:{PORT}")
            
            print(f"\n⏳ Servidor en ejecución... (Presiona Ctrl+C para detener)\n")
            print("=" * 70)
            
            # Mantener el servidor corriendo
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 Servidor detenido por el usuario")
        print("=" * 70)
        print("👋 ¡Gracias por usar el simulador!")
        
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: El puerto {PORT} ya está en uso.")
            print(f"💡 Soluciones:")
            print(f"   1. Cierra cualquier otro servidor en el puerto {PORT}")
            print(f"   2. Cambia el puerto en este script (variable PORT)")
            print(f"   3. Usa: netstat -ano | findstr :{PORT}  para ver qué lo usa")
        else:
            print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
# -----------------------------------------------------------------------------
