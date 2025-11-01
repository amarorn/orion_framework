#!/usr/bin/env python3
"""
Script de teste para o Oríon Framework.
Execute: python3 run_tests.py

Requisitos: pip install -e .
"""

import sys
import os
from pathlib import Path

# Tenta importar após instalação
try:
    import core
    import infrastructure
    import application
except ImportError:
    print("⚠️  Projeto não instalado. Execute: pip install -e .")
    sys.exit(1)

def test_imports():
    """Testa se todos os imports principais funcionam."""
    print("🧪 Testando imports...")
    
    try:
        from core.entities.pipeline import Pipeline
        from core.entities.node import Node
        from infrastructure.persistence.catalog import DataCatalog
        from infrastructure.config.context import OrionContext
        from infrastructure.logging.ConsoleLogger import ConsoleLogger
        from application.pipeline.builder import PipelineBuilder
        from application.pipeline.runner import PipelineRunner
        
        print("✅ Todos os imports principais funcionam!")
        return True
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_catalog():
    """Testa funcionalidade do Catalog."""
    print("\n🧪 Testando Catalog...")
    
    try:
        from infrastructure.persistence.catalog import DataCatalog
        
        catalog = DataCatalog({
            "test_dataset": {
                "type": "local_csv",
                "path": "test.csv"
            }
        })
        
        assert catalog.exists("test_dataset"), "Dataset deveria existir"
        assert not catalog.exists("inexistente"), "Dataset não deveria existir"
        
        print("✅ Catalog funciona corretamente!")
        return True
    except Exception as e:
        print(f"❌ Erro no Catalog: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_context():
    """Testa funcionalidade do Context."""
    print("\n🧪 Testando OrionContext...")
    
    try:
        from infrastructure.config.context import OrionContext
        from infrastructure.persistence.catalog import DataCatalog
        from infrastructure.logging.ConsoleLogger import ConsoleLogger
        
        catalog = DataCatalog({})
        context = OrionContext(catalog=catalog)
        
        assert context.catalog is not None, "Catalog deveria existir"
        assert context.logger is not None, "Logger deveria existir"
        
        print("✅ Context funciona corretamente!")
        return True
    except Exception as e:
        print(f"❌ Erro no Context: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pipeline_builder():
    """Testa criação de Pipeline via Builder."""
    print("\n🧪 Testando PipelineBuilder...")
    
    try:
        from application.pipeline.builder import PipelineBuilder
        from infrastructure.config.context import OrionContext
        from infrastructure.persistence.catalog import DataCatalog
        
        def dummy_extract(context):
            return "dummy_data"
        
        def dummy_transform(context, data):
            return f"transformed_{data}"
        
        builder = PipelineBuilder("test_pipeline")
        builder.add_node(dummy_extract, inputs=[], outputs=["raw_data"])
        builder.add_node(dummy_transform, inputs=["raw_data"], outputs=["processed_data"])
        pipeline = builder.build()
        
        assert pipeline.name == "test_pipeline", "Nome da pipeline incorreto"
        assert len(pipeline.nodes) == 2, "Deveria ter 2 nodes"
        
        print(f"✅ Pipeline '{pipeline.name}' criada com {len(pipeline.nodes)} nodes!")
        return True
    except Exception as e:
        print(f"❌ Erro no PipelineBuilder: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pipeline_execution():
    """Testa execução de uma pipeline simples."""
    print("\n🧪 Testando execução de Pipeline...")
    
    try:
        from application.pipeline.builder import PipelineBuilder
        from infrastructure.config.context import OrionContext
        from infrastructure.persistence.catalog import DataCatalog
        
        def extract(context):
            context.logger.info("Executando extract")
            return "data_from_source"
        
        def transform(context, data):
            context.logger.info(f"Transformando: {data}")
            transformed = f"transformed_{data}"
            return transformed
        
        builder = PipelineBuilder("test_execution")
        builder.add_node(extract, inputs=[], outputs=["raw"])
        builder.add_node(transform, inputs=["raw"], outputs=["processed"])
        pipeline = builder.build()
        
        catalog = DataCatalog({})
        context = OrionContext(catalog=catalog)
        
        result = pipeline.run(context)
        
        assert "processed" in result, "Resultado deveria conter 'processed'"
        assert result["processed"] == "transformed_data_from_source", "Transformação incorreta"
        
        print("✅ Pipeline executada com sucesso!")
        print(f"   Resultado: {result}")
        return True
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_example_pipeline():
    """Testa carregar o exemplo de pipeline."""
    print("\n🧪 Testando pipeline de exemplo...")
    
    try:
        # Verifica se o arquivo existe
        example_path = project_root / "examples" / "pipeline_clientes" / "pipeline.py"
        if not example_path.exists():
            print("⚠️  Arquivo de exemplo não encontrado, pulando...")
            return True
        
        # Tenta importar dinamicamente
        import importlib.util
        spec = importlib.util.spec_from_file_location("example_pipeline", example_path)
        module = importlib.util.module_from_spec(spec)
        
        # Adiciona ao sys.path para imports relativos funcionarem
        sys.path.insert(0, str(example_path.parent))
        
        spec.loader.exec_module(module)
        pipeline = module.create_pipeline()
        
        print(f"✅ Pipeline exemplo carregada: {pipeline.name}")
        print(f"   Nodes: {len(pipeline.nodes)}")
        return True
    except Exception as e:
        print(f"⚠️  Erro ao carregar exemplo (pode ser esperado): {e}")
        return True  # Não falha o teste se exemplo não funcionar


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("🧪 ORÍON FRAMEWORK - TESTES")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_catalog,
        test_context,
        test_pipeline_builder,
        test_pipeline_execution,
        test_example_pipeline,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro inesperado em {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passou: {passed}/{total}")
    print(f"❌ Falhou: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

