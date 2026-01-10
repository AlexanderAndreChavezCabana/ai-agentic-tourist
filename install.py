#!/usr/bin/env python
"""Script de instalación automática"""
import os
import sys
import subprocess
from pathlib import Path

print("="*60)
print("INSTALADOR - CHATBOT TURÍSTICO OPENAI")
print("="*60 + "\n")

project_root = Path(__file__).parent

# Paso 1: Instalar dependencias
print("1️⃣  Instalando dependencias...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(project_root / "requirements.txt")])
    print("   ✓ Dependencias instaladas\n")
except Exception as e:
    print(f"   ✗ Error: {e}\n")
    sys.exit(1)

# Paso 2: Crear .env
print("2️⃣  Configurando .env...")
env_file = project_root / ".env"
env_example = project_root / ".env.example"

if not env_file.exists():
    if env_example.exists():
        # Copiar desde .env.example
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("   ✓ Archivo .env creado desde .env.example")
        print("   ⚠️  IMPORTANTE: Edita .env y añade tu OPENAI_API_KEY\n")
    else:
        print("   ✗ No se encontró .env.example\n")
        sys.exit(1)
else:
    print("   ✓ Archivo .env ya existe\n")

# Paso 3: Verificar imports
print("3️⃣  Verificando módulos...")
try:
    from src.llm.base import LLMFactory
    from src.agents.touristic_agent import AgentBuilder
    print("   ✓ Todos los módulos importados correctamente\n")
except ImportError as e:
    print(f"   ✗ Error de importación: {e}\n")
    sys.exit(1)

# Paso 4: Instrucciones finales
print("="*60)
print("✅ INSTALACIÓN COMPLETADA")
print("="*60 + "\n")

print("PRÓXIMOS PASOS:\n")
print("1. Edita el archivo .env y añade tu OpenAI API Key:")
print("   OPENAI_API_KEY=tu_api_key_aqui\n")
print("2. Obtén tu API Key en: https://platform.openai.com/api-keys\n")
print("3. Prueba el chatbot:")
print("   python main.py\n")
print("4. O prueba con ejemplos:")
print("   python examples/basic_usage.py\n")
print("="*60)
