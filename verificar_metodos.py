#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que todos los métodos necesarios existen en AIBuilderScheduler
"""

def verificar_metodos():
    """Verifica que todos los métodos necesarios existan"""
    
    print("="*80)
    print("VERIFICACIÓN DE MÉTODOS - AIBuilderScheduler")
    print("="*80)
    
    try:
        from ai_builder_scheduler import AIBuilderScheduler
        print("[OK] Módulo importado correctamente\n")
        
        scheduler = AIBuilderScheduler()
        print("[OK] Instancia creada correctamente\n")
        
        # Lista de métodos que deben existir
        metodos_requeridos = [
            '_leer_archivo',
            '_procesar_formato_nombre_duracion',
            '_parsear_fila_csv_especial',
            '_parsear_fecha_espanol',
            'leer_entrada',
            'generar_cronograma'
        ]
        
        print("Verificando métodos requeridos:")
        print("-"*80)
        
        todos_existen = True
        for metodo in metodos_requeridos:
            existe = hasattr(scheduler, metodo)
            estado = "[OK]" if existe else "[FALTA]"
            print(f"{estado:8} {metodo}")
            if not existe:
                todos_existen = False
        
        print("-"*80)
        
        if todos_existen:
            print("\n[SUCCESS] ¡Todos los métodos existen!")
            print("\nProbando lectura del CSV...")
            
            # Probar lectura del CSV
            try:
                df = scheduler.leer_entrada("Tabla_Tareas1.csv")
                print(f"[OK] CSV leído: {len(df)} actividades")
                print(f"[OK] Fecha de inicio: {scheduler.fecha_inicio}")
                
                return True
            except Exception as e:
                print(f"[ERROR] Al leer CSV: {e}")
                return False
        else:
            print("\n[ERROR] Faltan métodos. Verifica que el archivo ai_builder_scheduler.py esté actualizado.")
            return False
            
    except ImportError as e:
        print(f"[ERROR] No se puede importar el módulo: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = verificar_metodos()
    
    if exito:
        print("\n" + "="*80)
        print("✅ TODO ESTÁ LISTO")
        print("="*80)
        print("\nPuedes:")
        print("1. Iniciar el backend: cd backend && python app.py")
        print("2. Probar directamente: python test_nuevo_csv.py")
        print("3. Usar la interfaz web después de iniciar backend y frontend")
    else:
        print("\n" + "="*80)
        print("❌ HAY PROBLEMAS")
        print("="*80)
        print("\nRevisa el archivo ai_builder_scheduler.py")
        print("Asegúrate de que todos los cambios se hayan guardado correctamente")
    
    exit(0 if exito else 1)

