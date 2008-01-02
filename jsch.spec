# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section   free

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:           jsch
Version:        0.1.36
Release:        %mkrel 0.0.2
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jsch/
Source0:        http://osdn.dl.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
# wget http://download.eclipse.org/tools/orbit/downloads/drops/S200705301823/bundles/com.jcraft.jsch_0.1.31.jar
# unzip com.jcraft.jsch_0.1.31.jar META-INF/MANIFEST.MF
# mv META-INF/MANIFEST.MF
# rmdir META-INF
Source1:        jsch-MANIFEST.MF
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  java-devel >= 1.4.2
BuildRequires:  jzlib >= 0:1.0.5
BuildRequires:  ant

%if ! %{gcj_support}
BuildArch:      noarch
%endif

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 1.0.31
%endif
Requires:       jzlib >= 0:1.0.5

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description    demo
%{summary}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath jzlib)
%{ant} dist javadoc 

# inject the OSGi Manifest
mkdir META-INF
cp -a %{SOURCE1} META-INF/MANIFEST.MF
zip dist/lib/%{name}-*.jar META-INF/MANIFEST.MF

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
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=234989
%ifnarch ia64
%{_bindir}/aot-compile-rpm
%endif 
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post demo
rm -f %{_datadir}/%{name}
ln -s %{name}-%{version} %{_datadir}/%{name}

%postun demo
if [ "$1" = "0" ]; then
    rm -f %{_datadir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%ifnarch ia64
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}-%{version}
%ghost %doc %{_datadir}/%{name}
