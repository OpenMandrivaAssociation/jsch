Name:           jsch
Version:        0.1.49
Release:        0.0.4
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jsch/
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

BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  jzlib >= 0:1.0.5
BuildRequires:  ant
BuildRequires:  zip

BuildArch:      noarch

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
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 dist/lib/%{name}-*.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# examples
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}-%{version}
%doc %{_datadir}/%{name}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:0.1.41-0.0.3mdv2011.0
+ Revision: 665838
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.1.41-0.0.2mdv2011.0
+ Revision: 606115
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.1.41-0.0.1mdv2010.1
+ Revision: 523131
- rebuilt for 2010.1

* Fri Jan 23 2009 Jérôme Soyer <saispo@mandriva.org> 0:0.1.41-0.0.0mdv2009.1
+ Revision: 332740
- New upstream release

* Mon Oct 20 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.1.40-0.0.0mdv2009.1
+ Revision: 295825
- 0.1.40

* Wed Jul 30 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.1.39-1.1.1mdv2009.0
+ Revision: 255169
- update OSGI manifest for the new eclipse

* Fri Jun 13 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.1.39-0.0.1mdv2009.0
+ Revision: 218741
- new version 0.1.39 and disable gcj compile

* Wed Apr 23 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.1.38-0.0.1mdv2009.0
+ Revision: 196798
- new version

* Tue Jan 22 2008 David Walluck <walluck@mandriva.org> 0:0.1.37-0.0.1mdv2008.1
+ Revision: 156080
- BuildRequires: zip
- remove %%ghost references
- compile demos
- reference jar by name when building/installing
- 0.1.37

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Fri Nov 02 2007 David Walluck <walluck@mandriva.org> 0:0.1.36-0.0.1mdv2008.1
+ Revision: 105307
- 0.1.36

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.1.34-0.0.2mdv2008.0
+ Revision: 87442
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Aug 29 2007 David Walluck <walluck@mandriva.org> 0:0.1.34-0.0.1mdv2008.0
+ Revision: 74718
- 0.1.34

* Wed Aug 08 2007 David Walluck <walluck@mandriva.org> 0:0.1.33-1.0.2mdv2008.0
+ Revision: 60577
- match eclipse jsch version in manifest

* Fri Jul 27 2007 David Walluck <walluck@mandriva.org> 0:0.1.33-1.0.1mdv2008.0
+ Revision: 56260
- fix Bundle-Version in MANIFEST.MF
- add MANIFEST.MF for eclipse

* Fri May 11 2007 David Walluck <walluck@mandriva.org> 0:0.1.33-1mdv2008.0
+ Revision: 26412
- 0.1.33


* Thu Mar 08 2007 David Walluck <walluck@mandriva.org> 0.1.32-1mdv2007.1
+ Revision: 134928
- 0.1.32

* Wed Jan 17 2007 David Walluck <walluck@mandriva.org> 0:0.1.31-1mdv2007.1
+ Revision: 110012
- 0.1.31

* Thu Nov 02 2006 David Walluck <walluck@mandriva.org> 0:0.1.30-1mdv2007.1
+ Revision: 75109
- 0.1.30
- Import jsch

* Mon Aug 28 2006 David Walluck <walluck@mandriva.org> 0:0.1.29-1mdv2007.0
- 0.1.29

* Thu May 25 2006 David Walluck <walluck@mandriva.org> 0:0.1.28-2mdv2007.0
- rebuild for libgcj.so.7

* Sat May 06 2006 David Walluck <walluck@mandriva.org> 0:0.1.28-1mdk
- 0.1.28

* Thu Apr 20 2006 David Walluck <walluck@mandriva.org> 0:0.1.27-1mdk
- 0.1.27
- aot compile

* Sat Apr 01 2006 David Walluck <walluck@mandriva.org> 0:0.1.26-1mdk
- 0.1.26

* Fri Mar 10 2006 Jerome Soyer <saispo@mandriva.org> 0.1.25-1mdk
- New release 0.1.25

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:0.1.24-2mdk
- BuildRequires: ant, java-devel

* Sat Jan 14 2006 David Walluck <walluck@mandriva.org> 0:0.1.24-1mdk
- 0.1.24

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:0.1.20-1.1mdk
- release

* Sat Apr 23 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.20-1jpp
- 0.1.20

* Sat Apr 23 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.18-1jpp
- 0.1.18

* Tue Nov 02 2004 David Walluck <david@jpackage.org> 0:0.1.17-2jpp
- rebuild with jdk 1.4.2

* Wed Oct 20 2004 David Walluck <david@jpackage.org> 0:0.1.17-1jpp
- 0.1.17

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:0.1.13-2jpp
- Rebuild with ant-1.6.2

