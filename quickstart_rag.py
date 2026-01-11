"""
Quick Start - Sistema RAG
Inicialización rápida para desarrollo
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Cargar env
load_dotenv()

print("=" * 70)
print("🚀 QUICK START - SISTEMA RAG HUARAZ")
print("=" * 70)

# Verificar OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("\n❌ ERROR: OPENAI_API_KEY no encontrada")
    print("\nPasos para solucionar:")
    print("1. Abre el archivo .env")
    print("2. Añade: OPENAI_API_KEY=tu-api-key-aqui")
    print("3. Vuelve a ejecutar este script\n")
    sys.exit(1)

print(f"\n✅ OpenAI API Key configurada: {api_key[:10]}...{api_key[-4:]}")

# Verificar dependencias
print("\n📦 Verificando dependencias...")
required = {
    'langchain': 'langchain',
    'langchain_community': 'langchain_community',
    'langchain_openai': 'langchain_openai',
    'faiss': 'faiss',
    'beautifulsoup4': 'bs4'  # Se instala como beautifulsoup4 pero se importa como bs4
}

missing = []
for package_name, import_name in required.items():
    try:
        __import__(import_name)
        print(f"   ✅ {package_name}")
    except ImportError:
        print(f"   ❌ {package_name}")
        missing.append(package_name)

if missing:
    print(f"\n⚠️  Faltan dependencias: {', '.join(missing)}")
    print("\nEjecuta: pip install -r requirements.txt\n")
    sys.exit(1)

# Inicializar RAG
print("\n🔧 Inicializando sistema RAG...")
print("   (Esto puede tardar 1-2 minutos la primera vez)\n")

try:
    from src.rag.web_loader import HuarazWebRAG
    
    rag = HuarazWebRAG(openai_api_key=api_key)
    
    # Intentar cargar desde caché
    if rag.load_vector_store():
        print("✅ Sistema cargado desde caché (rápido)")
    else:
        print("📥 Cargando contenido web (primera vez)...")
        print("   URLs a procesar:")
        for url in rag.TOURISM_URLS:
            print(f"   - {url}")
        
        if rag.initialize(force_reload=True):
            print("\n✅ Sistema inicializado y guardado en caché")
        else:
            print("\n⚠️  Hubo problemas al inicializar")
            sys.exit(1)
    
    # Prueba rápida
    print("\n🧪 Prueba de búsqueda...")
    results = rag.search("tours huaraz", k=2)
    
    if results:
        print(f"   ✅ Encontrados {len(results)} resultados")
        print(f"   📄 Ejemplo: {results[0].page_content[:100]}...")
    
    print("\n" + "=" * 70)
    print("✅ SISTEMA RAG LISTO")
    print("=" * 70)
    print("\n🎉 Todo está configurado correctamente!")
    print("\nAhora puedes:")
    print("1. Ejecutar el chatbot: python app.py")
    print("2. El agente usará automáticamente el sistema RAG")
    print("3. Pregunta sobre precios y tours para ver la búsqueda web en acción")
    print("\nEjemplo de preguntas:")
    print("  - '¿Cuánto cuesta el tour a la Laguna 69?'")
    print("  - 'Recomiéndame hoteles en Huaraz con precios'")
    print("  - '¿Qué tours hay disponibles?'\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\nRevisa los errores arriba y contacta soporte si persiste.\n")
    sys.exit(1)
