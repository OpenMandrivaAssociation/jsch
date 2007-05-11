%define section         free
%define gcj_support     1

Name:           jsch
Version:        0.1.33
Release:        %mkrel 1
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jsch/
Source0:        http://ovh.dl.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
Requires:       jzlib >= 0:1.0.5
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package demo
Summary:        Examples for %{name}
Group:          Development/Java

%description demo
%{summary}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath jzlib)
export OPT_JAR_LIST=:
%{ant} dist javadoc 

%install
# jars
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/lib/%{name}-*.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# examples
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a examples/* %{buildroot}%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}
