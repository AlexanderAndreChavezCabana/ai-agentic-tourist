#!/usr/bin/env python3
"""
Script automatizado para deployment en Google Cloud Run
Despliega tu chatbot en la nube en menos de 5 minutos
"""

import os
import subprocess
import sys
from pathlib import Path
import json

def print_header():
    """Mostrar header del script"""
    print("🚀 GOOGLE CLOUD RUN - AUTO DEPLOYMENT")
    print("=" * 50)
    print("🤖 Chatbot Turístico Huaraz")
    print("⏱️ Tiempo estimado: 3-5 minutos")
    print("-" * 50)

def check_prerequisites():
    """Verificar prerequisitos"""
    print("🔍 Verificando prerequisitos...")
    
    # Verificar directorio
    if not Path("app.py").exists():
        print("❌ Error: Ejecuta este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar gcloud CLI
    try:
        result = subprocess.run(['gcloud', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✅ Google Cloud CLI instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Google Cloud CLI no encontrado")
        print("📥 Instala desde: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)
    
    # Verificar Docker (opcional pero recomendado)
    try:
        subprocess.run(['docker', '--version'], 
                      capture_output=True, text=True, check=True)
        print("✅ Docker disponible")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Docker no encontrado (opcional)")
    
    print("✅ Prerequisitos verificados")

def setup_gcloud():
    """Configurar Google Cloud"""
    print("\n🔧 Configurando Google Cloud...")
    
    # Verificar si está logueado
    try:
        result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE', 
                                '--format=value(account)'], 
                               capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(f"✅ Ya logueado como: {result.stdout.strip()}")
        else:
            print("🔑 Necesitas autenticarte...")
            subprocess.run(['gcloud', 'auth', 'login'], check=True)
    except subprocess.CalledProcessError:
        print("🔑 Autenticando con Google Cloud...")
        subprocess.run(['gcloud', 'auth', 'login'], check=True)
    
    # Verificar/establecer proyecto
    try:
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                               capture_output=True, text=True, check=True)
        current_project = result.stdout.strip()
        if current_project and current_project != "unset":
            print(f"📋 Proyecto actual: {current_project}")
            use_current = input(f"¿Usar proyecto '{current_project}'? (s/n): ").lower()
            if use_current != 's':
                setup_new_project()
        else:
            setup_new_project()
    except subprocess.CalledProcessError:
        setup_new_project()

def setup_new_project():
    """Configurar nuevo proyecto"""
    print("📋 Configurar proyecto...")
    project_id = input("ID del proyecto (ej: huaraz-chatbot-123): ")
    if not project_id:
        project_id = "huaraz-chatbot-" + str(os.urandom(4).hex())
        print(f"🎲 Usando ID generado: {project_id}")
    
    # Establecer proyecto
    try:
        subprocess.run(['gcloud', 'config', 'set', 'project', project_id], check=True)
        print(f"✅ Proyecto configurado: {project_id}")
    except subprocess.CalledProcessError:
        print(f"❌ Error configurando proyecto: {project_id}")
        print("💡 Verifica que el proyecto exista o crea uno nuevo:")
        print("   https://console.cloud.google.com/projectcreate")
        sys.exit(1)

def enable_apis():
    """Habilitar APIs necesarias"""
    print("\n🔌 Habilitando APIs necesarias...")
    
    apis = [
        "run.googleapis.com",
        "cloudbuild.googleapis.com"
    ]
    
    for api in apis:
        try:
            print(f"   Habilitando {api}...")
            subprocess.run(['gcloud', 'services', 'enable', api], 
                          check=True, capture_output=True)
            print(f"   ✅ {api} habilitada")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Error habilitando {api}: {e}")

def get_environment_variables():
    """Obtener variables de entorno"""
    print("\n🔑 Configurando variables de entorno...")
    
    env_vars = {}
    
    # OpenAI API Key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        openai_key = input("🔑 OPENAI_API_KEY: ")
        if not openai_key:
            print("⚠️ Sin API key de OpenAI. El chatbot podría no funcionar.")
    
    if openai_key:
        env_vars["OPENAI_API_KEY"] = openai_key
    
    # Otras variables
    env_vars.update({
        "DEFAULT_LLM_PROVIDER": "openai",
        "APP_NAME": "Chatbot Turístico Huaraz",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO"
    })
    
    print("✅ Variables de entorno configuradas")
    return env_vars

def deploy_to_cloudrun(env_vars):
    """Deploy a Cloud Run"""
    print("\n🚀 Desplegando a Google Cloud Run...")
    
    # Configurar nombre del servicio
    service_name = "huaraz-chatbot"
    region = "us-central1"
    
    # Preparar comando de deploy
    cmd = [
        "gcloud", "run", "deploy", service_name,
        "--source", ".",
        "--platform", "managed",
        "--region", region,
        "--allow-unauthenticated",
        "--quiet"
    ]
    
    # Agregar variables de entorno
    if env_vars:
        env_string = ",".join([f"{k}={v}" for k, v in env_vars.items()])
        cmd.extend(["--set-env-vars", env_string])
    
    print(f"🔄 Ejecutando deploy en región {region}...")
    print("⏱️ Esto puede tomar 2-3 minutos...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Extraer URL del resultado
        lines = result.stderr.split('\n')
        service_url = None
        for line in lines:
            if "https://" in line and "run.app" in line:
                service_url = line.strip()
                break
        
        print("\n🎉 ¡DEPLOYMENT EXITOSO!")
        print("=" * 50)
        
        if service_url:
            print(f"🌍 Tu chatbot está VIVO en:")
            print(f"   {service_url}")
            print(f"📱 Interfaz web:")
            print(f"   {service_url}/static/index.html")
        else:
            print(f"🌍 URL: https://{service_name}-xxx-uc.a.run.app")
        
        print(f"\n📊 Gestionar servicio:")
        print(f"   https://console.cloud.google.com/run")
        
        return service_url
    
    except subprocess.CalledProcessError as e:
        print("❌ Error en deployment:")
        print(f"   Stdout: {e.stdout}")
        print(f"   Stderr: {e.stderr}")
        print("\n🆘 Troubleshooting:")
        print("   1. Verifica que el proyecto esté configurado")
        print("   2. Verifica que las APIs estén habilitadas")
        print("   3. Revisa los logs en Cloud Console")
        return None

def show_next_steps(service_url):
    """Mostrar próximos pasos"""
    print("\n🎯 PRÓXIMOS PASOS:")
    print("-" * 30)
    
    if service_url:
        print("1. 🧪 Probar el chatbot:")
        print(f"   Abre: {service_url}")
        
        print("\n2. 🔗 Compartir con otros:")
        print(f"   URL pública: {service_url}")
        
    print("\n3. 📊 Monitorear:")
    print("   • Logs: gcloud logging read")
    print("   • Console: https://console.cloud.google.com/run")
    
    print("\n4. 🔧 Configuraciones avanzadas:")
    print("   • Dominio personalizado")
    print("   • Escalado automático")
    print("   • CI/CD con GitHub Actions")
    
    print("\n💰 Costos:")
    print("   • Gratis para desarrollo/testing")
    print("   • Pay-per-use en producción")
    print("   • Auto-scale a $0 cuando no hay requests")

def main():
    """Función principal"""
    try:
        print_header()
        check_prerequisites()
        setup_gcloud()
        enable_apis()
        env_vars = get_environment_variables()
        service_url = deploy_to_cloudrun(env_vars)
        show_next_steps(service_url)
        
        print("\n✨ ¡Deployment completado exitosamente!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Deployment cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()