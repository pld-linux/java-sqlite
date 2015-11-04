#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%include	/usr/lib/rpm/macros.java
Summary:	SQLite Java Wrapper/JDBC Driver
Name:		java-sqlite
Version:	20150419
Release:	1
License:	BSD
Group:		Libraries/Java
Source0:	http://www.ch-werner.de/javasqlite/javasqlite-%{version}.tar.gz
# Source0-md5:	242e384c1cd863d6996a35cf8c1c1e97
URL:		http://www.ch-werner.de/javasqlite/
Patch0:		jnipath.patch
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	jdk >= 1.5
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	sqlite3-devel >= 3.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
javasqlite is a Java wrapper including a basic JDBC driver for the
SQLite database engine. It is designed using JNI to interface to the
SQLite API.

%package javadoc
Summary:	API documentation for %{name}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n javasqlite-%{version}
sed -e 's|@JNIPATH@|%{_libdir}/%{name}|' %{PATCH0} | %{__patch} -p1

%undos doc/ajhowto.txt
f=ChangeLog; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8; mv $f.utf8 $f
rm doc/stylesheet.css # overrides javadoc's defaults

%build
%configure \
	--with-jardir=%{_libdir}/%{name} \
	--libdir=%{_libdir}/%{name} \
	--without-sqlite

# Java build not parallel clean
%{__make} -j1 sqlite.jar
%{__make}
%{__make} javadoc JAVADOCLINK=%{_javadocdir}/java

%if %{with tests}
%{__make} test test3 testg \
	JAVA_RUN=%java JAVAC=%javac 
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/%{name}/libsqlite_jni.la

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -a doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog license.terms
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/sqlite.jar
%{_libdir}/%{name}/libsqlite_jni.so

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}
