%define bname citationstyles
%define sname locales

%define commit b5f4b87d7693f69a5697fc21e1b2b31dc6dc39b6
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%bcond_with java

Summary:	Citation Style Language (CSL) citation locales
Name:		%{bname}-%{sname}
Version:	1.0.1
Release:	1
# Creative Commons Attribution-ShareAlike 3.0 Unported
License:	CC-BY-SA
Group:		Publishing
URL:		https://citationstyles.org/
Source0:	https://github.com/citation-style-language/%{sname}/archive/%{commit}/%{sname}-%{commit}.tar.gz
Source1:	https://repo1.maven.org/maven2/org/%{bname}/%{sname}/1.0/%{sname}-1.0.pom
BuildArch:	noarch

%if %{with java}
BuildRequires:	maven-local
%endif

%if %{with java}
Requires:	java-headless
Requires:	javapackages-tools 
%endif

%description
Citation Style Language (CSL) citation locales.

%files
%{_datadir}/%{name}/*
%doc README.md

#----------------------------------------------------------------------------

%if %{with java}
%package java
Summary:	Java package for %{name}
Group:		Development/Java

%description java
Citation Style Language (CSL) citation locales packaged for Java applications.

%files java
%{_javadir}/%{sname}*.jar
%{_javadir}/%{bname}/
%doc README.md
%endif

#----------------------------------------------------------------------------

%prep
%setup -q -n %{sname}-%{commit}	

%if %{with java}
# Add pom.xml
cp -a %{SOURCE1} ./pom.xml

# Fix version in pom.xml
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}</version>"
%endif

%build

%if %{with java}
# jar
%jar cf %{sname}-%{version}.jar locales*.xml

# add the index to the jar
%jar i %{sname}-%{version}.jar
%endif

%install
install -dm 0755 %{buildroot}%{_datadir}/%{name}/
install -pm 0644 locales*.{json,xml}  %{buildroot}%{_datadir}/%{name}/

# jar
%if %{with java}
install -dm 0755 %{buildroot}%{_javadir}/%{bname}
install -pm 0644 %{sname}-%{version}.jar %{buildroot}%{_javadir}/%{bname}/%{sname}-%{version}.jar
ln -fs %{sname}-%{version}.jar %{buildroot}%{_javadir}/%{bname}/%{sname}.jar
ln -fs %{bname}/%{sname}.jar %{buildroot}%{_javadir}/%{sname}-%{version}.jar
%endif

