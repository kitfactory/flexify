"""
Tests for exception classes.
例外クラスのテスト。
"""

import pytest
from flexify.core import ModuleError


class TestModuleError:
    """
    Test cases for ModuleError exception.
    ModuleError例外のテストケース。
    """
    
    def test_module_error_basic(self):
        """
        Test basic ModuleError creation and message.
        基本的なModuleErrorの作成とメッセージをテストします。
        """
        error = ModuleError("Test error message")
        assert str(error) == "Test error message"
        assert error.module_name is None
        assert error.original_error is None
    
    def test_module_error_with_module_name(self):
        """
        Test ModuleError with module name.
        モジュール名を持つModuleErrorをテストします。
        """
        error = ModuleError("Test error", module_name="TestModule")
        assert str(error) == "[TestModule] Test error"
        assert error.module_name == "TestModule"
    
    def test_module_error_with_original_error(self):
        """
        Test ModuleError with original exception.
        元の例外を持つModuleErrorをテストします。
        """
        original = ValueError("Original error")
        error = ModuleError("Wrapped error", original_error=original)
        assert error.original_error == original
        assert isinstance(error.original_error, ValueError)
    
    def test_module_error_inheritance(self):
        """
        Test that ModuleError inherits from Exception.
        ModuleErrorがExceptionを継承していることをテストします。
        """
        error = ModuleError("Test error")
        assert isinstance(error, Exception)
    
    def test_module_error_raising(self):
        """
        Test raising and catching ModuleError.
        ModuleErrorの発生とキャッチをテストします。
        """
        with pytest.raises(ModuleError) as exc_info:
            raise ModuleError("Test error", module_name="TestModule")
        
        assert "Test error" in str(exc_info.value)
        assert exc_info.value.module_name == "TestModule"