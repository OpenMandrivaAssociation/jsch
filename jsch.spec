%define section         free
%define gcj_support     1

Name:           jsch
Version:        0.1.32
Release:        %mkrel 1
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jsch/
Source0:        http://ovh.dl.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Distribution:  JPackage
#Vendor:        JPackage Project

%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires: java-gcj-compat-devel 
%else
BuildArch:      noarch
%endif
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  jzlib >= 0:1.0.5
Requires:       jzlib >= 0:1.0.5

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Development/Java

%description    demo
%{summary}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath jzlib)
export OPT_JAR_LIST=
%ant dist javadoc 

%install
# jars
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 dist/lib/%{name}-*.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# examples
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%post demo
rm -f %{_datadir}/%{name}
ln -s %{name}-%{version} %{_datadir}/%{name}


%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%doc LICENSE.txt

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}-%{version}
%ghost %doc %{_datadir}/%{name}


