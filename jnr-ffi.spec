Name:		jnr-ffi
Version:	2.3.7
Release:	1
Summary:	Java library for calling native code without JNI
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/jnr/jnr-ffi
Source0:	https://github.com/jnr/jnr-ffi/archive/refs/tags/jnr-ffi-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
BuildSystem:	maven

%description
Library for invoking native functions from Java. Native calls go through
the system jffi package.

%prep
%setup -q -n jnr-ffi-jnr-ffi-%{version}
# Upstream's jffi native classifier is a jar of prebuilt JNI libraries.
# The system jffi package loads libjffi from the library path instead.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
# The test-compile antrun builds a native test library with the Ant 1.x
# <tasks> element, which current antrun rejects. Tests are skipped.
text = re.sub(
	r"\s*<plugin>\s*<artifactId>maven-antrun-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(
	r"\s*<dependency>(?:(?!</dependency>).)*<classifier>native</classifier>(?:(?!</dependency>).)*</dependency>",
	"",
	text,
	count=1,
	flags=re.S,
)
# bnd's default import reads a bundle version from every jar. ASM has none.
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(
	r"\s*<manifestFile>.*?</manifestFile>",
	"",
	text,
	count=1,
	flags=re.S,
)
# jnr-parent's surefire toolchain is not installed. Keep this plugin's own
# configuration and do not merge the parent's.
text = re.sub(
	r"(<artifactId>maven-surefire-plugin</artifactId>\s*<configuration)>",
	r'\1 combine.self="override">',
	text,
	count=1,
)
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
