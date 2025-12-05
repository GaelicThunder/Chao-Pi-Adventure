"""Tests for Chao entity"""

import pytest
from core.chao import Chao


class TestChao:
    """Test Chao class"""
    
    def test_chao_creation(self):
        """Test basic Chao creation"""
        chao = Chao("TestChao")
        assert chao.name == "TestChao"
        assert chao.age == 0.0
        assert chao.stamina == 100
    
    def test_stat_consumption(self):
        """Test item consumption"""
        chao = Chao()
        initial_run = chao.run
        
        success = chao.consume_item("Run Fruit")
        assert success
        assert chao.run == initial_run + 0.25
    
    def test_evolution_trigger(self):
        """Test evolution at age 100"""
        chao = Chao()
        chao.run = 20
        chao.age = 99
        
        chao.age_up(1.0)
        assert chao.age >= 100
        assert chao.evolved
    
    def test_money_management(self):
        """Test money operations"""
        chao = Chao()
        chao.add_money(100)
        assert chao.money == 100
        
        success = chao.spend_money(50)
        assert success
        assert chao.money == 50
        
        success = chao.spend_money(100)
        assert not success
        assert chao.money == 50
    
    def test_serialization(self):
        """Test to_dict and from_dict"""
        chao = Chao("Original")
        chao.fly = 10
        chao.money = 50
        
        data = chao.to_dict()
        restored = Chao.from_dict(data)
        
        assert restored.name == "Original"
        assert restored.fly == 10
        assert restored.money == 50
