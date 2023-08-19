import pytest
from snippetchecker.api import SnippetChecker, SnippetType, LoopType

class TestSnippetChecker:
    @pytest.fixture
    def init_instance(self):
        self.c = SnippetChecker()

    def test__create_configure(self, init_instance):
        assert self.c.configure.get("API_ENTRYPOINT")
        assert self.c.configure.get("API_COMPATIBILITY")
        assert self.c.configure.get("API_VERSION")
        assert self.c.configure.get("UNIQUE_ID")

    def test__cookie_update(self, init_instance):
        newc = SnippetChecker()
        cookies = {a.name:a.value for a in self.c.cookiejar}
        newcookies = {a.name:a.value for a in newc.cookiejar}
        assert cookies != newcookies

    def test__determine_snippet_type(self, init_instance):
        assert self.c.determine_snippet_type("100") == SnippetType.CONSTANT_VALUE
        assert self.c.determine_snippet_type("1.035e-10") == SnippetType.CONSTANT_VALUE
        assert self.c.determine_snippet_type("'hogehoge'") == SnippetType.CONSTANT_VALUE
        assert self.c.determine_snippet_type("1+1+2+3*5") == SnippetType.CONSTANT_FORMULA
        assert self.c.determine_snippet_type("-1.035e-10") == SnippetType.CONSTANT_FORMULA
        assert self.c.determine_snippet_type("1.035e-10*'boo%d'%3+f'hoo{234}'") == SnippetType.CONSTANT_FORMULA
        assert self.c.determine_snippet_type("(1,2,3)") == SnippetType.CONSTANT_STRUCTURE
        assert self.c.determine_snippet_type("[t if a else u]") == SnippetType.CONSTANT_STRUCTURE
        assert self.c.determine_snippet_type("(1,2,3)+[1,2,3]+(1,2,3)+{'a':1,'b':2}") == SnippetType.CONSTANT_STRUCTURE
        assert self.c.determine_snippet_type("hoge = hogehoge + 1") == SnippetType.LINE_ASSIGN
        assert self.c.determine_snippet_type("boo,fuu = (hogehoge + 1, 'abc')") == SnippetType.LINE_ASSIGN
        assert self.c.determine_snippet_type("a,(b,d),d = t if a else u") == SnippetType.LINE_ASSIGN
        assert self.c.determine_snippet_type("hoge()") == SnippetType.LINE_VIABLE
        assert self.c.determine_snippet_type("boo() if a else b") == SnippetType.LINE_VIABLE
        assert self.c.determine_snippet_type("t = (a:=2) + 3") == SnippetType.LINE_VIABLE
        assert self.c.determine_snippet_type("for a in b: pass") == SnippetType.CODE_SNIPPET
        assert self.c.determine_snippet_type("if a: b=c;") == SnippetType.CODE_SNIPPET
        assert self.c.determine_snippet_type("a+=b;b+=1;c+=a") == SnippetType.CODE_SNIPPET
        assert len(self.c.errormsg) == 0

    def test__enumerate_difinitions_used(self, init_instance):
        assert set(self.c.enumerate_difinitions_used(
"""a = 100
b = -1.035e-10
c.boo = 'hoge'
""")) == {'a','b','c'}
        assert set(self.c.enumerate_difinitions_used(
"""def a():
  return
class b:
  c.boo = 'hoge'
""")) == {'a','b','c'}
        assert set(self.c.enumerate_difinitions_used(
"""a = lambda p: p**2
import b
from c import d
""")) == {'a','b','c'}
        assert len(self.c.errormsg) == 0

    def test__enumerate_variables_assign(self, init_instance):
        assert set(self.c.enumerate_variables_assign(
"""a = 100
b = -1.035e-10
c.boo = 'hoge'
""")) == {'a','b','c.boo'}
        assert set(self.c.enumerate_variables_assign(
"""def a():
  return
class b:
  c.boo = 'hoge'
""")) == {'c.boo'}
        assert set(self.c.enumerate_variables_assign(
"""a = lambda p: p**2
import b
from c import d
""")) == {'a'}
        assert len(self.c.errormsg) == 0

    def test__enumerate_functions_called(self, init_instance):
        assert set(self.c.enumerate_functions_called(
"""a()
b(-1.035e-10)
c.boo('hoge')
""")) == {'a','b','c.boo'}
        assert set(self.c.enumerate_functions_called(
"""a.b.c('hoge')
boo(fuu()+hoge())
""")) == {'a.b.c','boo','fuu','hoge'}
        assert len(self.c.errormsg) == 0
