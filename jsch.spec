Summary:        Pure Java implementation of SSH2
Name:           jsch
Version:        0.1.49
Release:        0.0.6
Group:          Development/Java
License:        BSD-style
Url:            http://www.jcraft.com/jsch/
Source0:        http://heanet.dl.sourceforge.net/project/jsch/jsch/0.1.49/jsch-0.1.49.zip
# wget \
# http://download.eclipse.org/tools/orbit/downloads/drops/R20080611105805/bundles/com.jcraft.jsch_0.1.37.v200803061811.jar
# unzip com.jcraft.jsch_*.jar META-INF/MANIFEST.MF
# mv META-INF/MANIFEST.MF .
# sed -i "/^Name/d" MANIFEST.MF
# sed -i "/^SHA1/d" MANIFEST.MF
# dos2unix MANIFEST.MF
# sed -i "/^$/d" MANIFEST.MF
# unix2dos MANIFEST.MF
Source1:        MANIFEST.MF
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  jzlib >= 0:1.0.5
BuildRequires:  zip
Requires:       jzlib >= 0:1.0.5

%track
prog %name = {
	url = http://www.jcraft.com/jsch/
	version = %version
	regex = jsch-(__VER__)\.jar
}

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
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
ant dist javadoc

# inject the OSGi Manifest
mkdir META-INF
cp %{SOURCE1} META-INF
zip dist/lib/%{name}-*.jar META-INF/MANIFEST.MF

%install
# jars
install -Dpm 644 dist/lib/%{name}-*.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# examples
install -dm 755 %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr examples/* %{buildroot}%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_datadir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/*.jar
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%doc %{_datadir}/%{name}-%{version}
%doc %{_datadir}/%{name}

