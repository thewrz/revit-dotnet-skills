"""Compile actual documentation examples; reject broken constructors/null flow."""
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    revision = os.environ.get('SKILL_TEST_REF')
    if revision:
        return subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT, text=True)
    return (ROOT / path).read_text()


def compile_example(code):
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary)
        (path / 'global.json').write_text('{"sdk":{"version":"8.0.100","rollForward":"latestFeature"}}')
        (path / 'Example.csproj').write_text('''<Project Sdk="Microsoft.NET.Sdk">
<PropertyGroup><TargetFramework>net8.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings>
<Nullable>enable</Nullable><TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup></Project>''')
        (path / 'Example.cs').write_text(code)
        result = subprocess.run(['dotnet', 'build', '--nologo'], cwd=path,
                                capture_output=True, text=True, timeout=120, check=False)
        return result.returncode, result.stdout + result.stderr


class ExampleTests(unittest.TestCase):
    def test_value_objects_compile(self):
        text = source('skills/csharp-coding-standards/value-objects-and-patterns.md')
        code = re.findall(r'```csharp\n(.*?)```', text, re.DOTALL)[0]
        status, output = compile_example(code)
        self.assertEqual(status, 0, output)

    def test_nullable_return_contract_reaches_caller(self):
        text = source('skills/csharp-nullable-reference-types/nullable-attributes-reference.md')
        text = text.split('### `[NotNullIfNotNull(string)]`')[1]
        code = re.findall(r'```csharp\n(.*?)```', text, re.DOTALL)[0]
        code = 'using System.Diagnostics.CodeAnalysis;\npublic static class Example {\n' + code
        code += '\npublic static int Use() => NormalizeUrl("HTTPS://EXAMPLE.COM").Length;\n}'
        status, output = compile_example(code)
        self.assertEqual(status, 0, output)
