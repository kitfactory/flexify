#!/usr/bin/env python3
"""
Example script demonstrating how to use Flexify.
Flexifyの使用方法を示すサンプルスクリプト。
"""

import json
from pathlib import Path
from flexify.runner import SimpleRunner
from flexify.registry import get_global_registry

# Import example modules to register them
from flexify.examples import text_modules, math_modules


def print_result(name: str, result: dict):
    """
    Pretty print workflow results.
    ワークフロー結果を見やすく表示します。
    """
    print(f"\n{'='*60}")
    print(f"Workflow: {name}")
    print(f"{'='*60}")
    
    # Sort keys for consistent output
    for key in sorted(result.keys()):
        value = result[key]
        if isinstance(value, list) and len(value) > 10:
            # Truncate long lists
            print(f"{key}: {value[:5]} ... {value[-5:]}")
        else:
            print(f"{key}: {value}")


def run_text_analysis():
    """
    Run text analysis workflow example.
    テキスト分析ワークフローの例を実行します。
    """
    print("\n" + "="*70)
    print("Running Text Analysis Workflow")
    print("="*70)
    
    runner = SimpleRunner()
    
    # Create sample text file if it doesn't exist
    sample_file = Path("examples/data/sample.txt")
    if not sample_file.exists():
        sample_file.parent.mkdir(parents=True, exist_ok=True)
        sample_file.write_text("""Hello World! This is a sample text file for Flexify.

Flexify is a modular task processing framework that allows you to:
- Define reusable modules
- Create workflows in YAML or JSON
- Process data through a pipeline
- Track execution status

This sample file contains multiple lines and words
to demonstrate the text processing capabilities
of the example modules.""")
    
    result = runner.run("examples/workflows/text_analysis.yaml")
    print_result("Text Analysis", result)
    
    # Show workflow status
    status = runner.get_status()
    print(f"\nWorkflow Status:")
    print(f"  Completed: {status.is_completed()}")
    print(f"  Modules executed: {', '.join(status.completed_modules)}")


def run_math_pipeline():
    """
    Run math pipeline workflow example.
    数学パイプラインワークフローの例を実行します。
    """
    print("\n" + "="*70)
    print("Running Math Pipeline Workflow")
    print("="*70)
    
    runner = SimpleRunner()
    result = runner.run("examples/workflows/math_pipeline.json")
    print_result("Math Pipeline", result)


def run_simple_calculator():
    """
    Run simple calculator workflow example.
    シンプルな計算機ワークフローの例を実行します。
    """
    print("\n" + "="*70)
    print("Running Simple Calculator Workflow")
    print("="*70)
    
    runner = SimpleRunner()
    result = runner.run("examples/workflows/simple_calculator.yaml")
    
    print(f"\nCalculation: (10 + 5) * 3 = {result.get('final_result')}")
    print(f"Square root of {result.get('final_result')} = {result.get('sqrt_result'):.4f}")


def run_programmatic_example():
    """
    Example of running a workflow programmatically.
    プログラムでワークフローを実行する例。
    """
    print("\n" + "="*70)
    print("Running Programmatic Workflow")
    print("="*70)
    
    from flexify.runner import WorkflowConfig, ModuleConfig
    
    # Create workflow configuration programmatically
    config = WorkflowConfig(
        name="programmatic_workflow",
        initial_session={"n": 15},
        modules=[
            ModuleConfig(
                name="fibonacci",
                class_name="flexify.examples.math_modules.FibonacciModule"
            ),
            ModuleConfig(
                name="stats",
                class_name="flexify.examples.math_modules.StatisticsModule",
                inputs={"numbers": "sequence"}
            )
        ]
    )
    
    runner = SimpleRunner()
    result = runner.run_from_config(config)
    
    print(f"\nFibonacci sequence (n=15): {result.get('sequence')}")
    print(f"Statistics of Fibonacci sequence:")
    print(f"  Mean: {result.get('mean')}")
    print(f"  Std Dev: {result.get('std_dev')}")
    print(f"  Range: {result.get('range')}")


def main():
    """
    Run all examples.
    すべての例を実行します。
    """
    print("Flexify Example Workflows")
    print("=" * 70)
    
    try:
        run_text_analysis()
    except Exception as e:
        print(f"Error in text analysis: {e}")
    
    try:
        run_math_pipeline()
    except Exception as e:
        print(f"Error in math pipeline: {e}")
    
    try:
        run_simple_calculator()
    except Exception as e:
        print(f"Error in simple calculator: {e}")
    
    try:
        run_programmatic_example()
    except Exception as e:
        print(f"Error in programmatic example: {e}")
    
    print("\n" + "="*70)
    print("All examples completed!")


if __name__ == "__main__":
    main()