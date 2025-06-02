"""
Tests for Module abstract base class.
Module抽象基底クラスのテスト。
"""

import pytest
from typing import Dict, Any, List
from flexify.core import Module, ParamInfo, Status, ModuleError


class TestModuleImpl(Module):
    """
    Test implementation of Module for testing purposes.
    テスト目的のModuleのテスト実装。
    """
    
    def execute(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple test execution that adds output_value to session.
        session に output_value を追加する単純なテスト実行。
        """
        input_value = session.get("input_value", 0)
        session["output_value"] = input_value * 2
        return session
    
    @classmethod
    def get_param_info(cls) -> List[ParamInfo]:
        """
        Define test parameters.
        テストパラメータを定義します。
        """
        return [
            ParamInfo(
                name="input_value",
                type=int,
                required=True,
                description="Input value to double"
            ),
            ParamInfo(
                name="output_value",
                type=int,
                required=False,
                default=0,
                description="Doubled output value"
            )
        ]


class ErrorModule(Module):
    """
    Module that raises an error for testing error handling.
    エラーハンドリングをテストするためにエラーを発生させるモジュール。
    """
    
    def execute(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Always raises an error.
        常にエラーを発生させます。
        """
        raise ValueError("Test error")
    
    @classmethod
    def get_param_info(cls) -> List[ParamInfo]:
        """
        No parameters needed for error module.
        エラーモジュールにはパラメータは不要です。
        """
        return []


class TestModuleClass:
    """
    Test cases for Module abstract base class.
    Module抽象基底クラスのテストケース。
    """
    
    def test_module_initialization(self):
        """
        Test module initialization with PENDING status.
        PENDINGステータスでのモジュール初期化をテストします。
        """
        module = TestModuleImpl()
        assert module.status == Status.PENDING
    
    def test_execute_success(self):
        """
        Test successful module execution.
        成功するモジュール実行をテストします。
        """
        module = TestModuleImpl()
        session = {"input_value": 5}
        result = module.execute(session)
        
        assert result["output_value"] == 10
        assert "input_value" in result
    
    def test_safe_execute_success(self):
        """
        Test safe_execute with successful execution.
        成功する実行でのsafe_executeをテストします。
        """
        module = TestModuleImpl()
        session = {"input_value": 5}
        
        result = module.safe_execute(session)
        
        assert module.status == Status.SUCCESS
        assert result["output_value"] == 10
    
    def test_safe_execute_missing_required_input(self):
        """
        Test safe_execute with missing required input.
        必須入力が欠落している場合のsafe_executeをテストします。
        """
        module = TestModuleImpl()
        session = {}  # Missing required "input_value"
        
        with pytest.raises(ModuleError) as exc_info:
            module.safe_execute(session)
        
        assert module.status == Status.FAILED
        assert "Required input 'input_value' not found" in str(exc_info.value)
        assert exc_info.value.module_name == "TestModuleImpl"
    
    def test_safe_execute_invalid_type(self):
        """
        Test safe_execute with invalid input type.
        無効な入力型でのsafe_executeをテストします。
        """
        module = TestModuleImpl()
        session = {"input_value": "not an int"}
        
        with pytest.raises(ModuleError) as exc_info:
            module.safe_execute(session)
        
        assert module.status == Status.FAILED
        assert "invalid type" in str(exc_info.value)
    
    def test_safe_execute_error_handling(self):
        """
        Test safe_execute error handling.
        safe_executeのエラーハンドリングをテストします。
        """
        module = ErrorModule()
        session = {}
        
        with pytest.raises(ModuleError) as exc_info:
            module.safe_execute(session)
        
        assert module.status == Status.FAILED
        assert "Unexpected error" in str(exc_info.value)
        assert exc_info.value.module_name == "ErrorModule"
        assert isinstance(exc_info.value.original_error, ValueError)
    
    def test_validate_inputs(self):
        """
        Test validate_inputs correctly validates input parameters.
        validate_inputsが入力パラメータを正しく検証することをテストします。
        """
        module = TestModuleImpl()
        
        # Test with correct input
        session = {"input_value": 42}
        module.validate_inputs(session)  # Should not raise
        
        # Test with missing input
        session = {}
        with pytest.raises(ModuleError) as exc_info:
            module.validate_inputs(session)
        assert "Required input 'input_value' not found" in str(exc_info.value)
    
    def test_abstract_methods_not_implemented(self):
        """
        Test that abstract methods must be implemented.
        抽象メソッドが実装される必要があることをテストします。
        """
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class without implementing abstract methods
            Module()
    
    def test_get_param_info(self):
        """
        Test get_param_info returns correct parameter information.
        get_param_infoが正しいパラメータ情報を返すことをテストします。
        """
        params = TestModuleImpl.get_param_info()
        
        assert len(params) == 2
        assert params[0].name == "input_value"
        assert params[0].type == int
        assert params[0].required is True
        assert params[1].name == "output_value"
        assert params[1].required is False