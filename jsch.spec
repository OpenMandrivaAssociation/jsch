%{?_javapackages_macros:%_javapackages_macros}
# copyright (c) 2000-2005, JPackage Project
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

Name:           jsch
Version:        0.1.51
Release:        3.1
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:		Development/Java
License:        BSD
URL:            http://www.jcraft.com/jsch/
Source0:        http://download.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
# wget \
# http://download.eclipse.org/tools/orbit/downloads/drops/R20090825191606/bundles/com.jcraft.jsch_0.1.41.v200903070017.jar
# unzip com.jcraft.jsch_*.jar META-INF/MANIFEST.MF
# mv META-INF/MANIFEST.MF .
# sed -i "/^Name/d" MANIFEST.MF
# sed -i "/^SHA1/d" MANIFEST.MF
# dos2unix MANIFEST.MF
# sed -i "/^$/d" MANIFEST.MF
# unix2dos MANIFEST.MF
Source1:        MANIFEST.MF
Source2:        plugin.properties
Source3:        http://repo1.maven.org/maven2/com/jcraft/%{name}/%{version}/%{name}-%{version}.pom

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-devel >= 1.4.2
BuildRequires:  jzlib >= 0:1.0.5
BuildRequires:  ant
BuildRequires:  zip

BuildArch:      noarch

Requires:       jzlib >= 0:1.0.5
Requires:       jpackage-utils

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package        javadoc
Summary:        Javadoc for %{name}

Requires:       jpackage-utils

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}


%description    demo
%{summary}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath jzlib)
ant dist javadoc 

# inject the OSGi Manifest
mkdir META-INF
cp %{SOURCE1} META-INF
cp %{SOURCE2} plugin.properties
zip dist/lib/%{name}-*.jar META-INF/MANIFEST.MF
zip dist/lib/%{name}-*.jar plugin.properties

%install
# jars
install -Dpm 644 dist/lib/%{name}-*.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# examples
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

# POM and depmap
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

%files -f .mfiles
%doc LICENSE.txt

%files javadoc
%doc %{_javadocdir}/%{name}*
%doc LICENSE.txt

%files demo
%doc %{_datadir}/%{name}*
%doc LICENSE.txt


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Krzysztof Daniel <kdaniel@redhat.com> 0:0.1.50-1
- Update to latest upstream.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.49-1
- Update to latest upstream.

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.1.48-3
- Add maven POM

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 2 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.48-1
- Update to latest upstream 0.1.48.

* Thu Mar 15 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:0.1.46-2
- Updated MANIFEST.MF to match the actual upstream version.
- Added plugin.properties to get proper vendor name in Eclipse.

* Wed Feb 15 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.46-1
- Update to latest upstream version 0.1.46.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 2 2011 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.45-1
- Update to new upstream version.

* Thu Sep 15 2011 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.44-4
- Guidelines fixes.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.44-2
- BR zip.
- Don't install versioned jar.

* Tue Nov 2 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.44-1
- New upstream version.

* Fri Sep 24 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.43-2
- Fix merge review comments (#225953).

* Mon Aug 16 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.43-1
- Update to new upstream version.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:0.1.41-4
- Fix changelog formatting error

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:0.1.41-3
- Update URL in comment for MANIFEST.MF
- Fix Groups
- Remove ghost symlinking

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 8 2009 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.41-1
- Update to new version 0.1.41.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.39-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:0.1.39-1.1
- 0.1.39

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.1.31-2.5
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.1.31-2jpp.4
- fix license tag

* Mon Apr 07 2008 Deepak Bhole <dbhole@redhat.com> - 0:0.1.31-2jpp.3
- Fix bz# 441071: Add backward compatibility patch from mwringe at redhat

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.1.31-2jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.1.31-1jpp.2
- Added %%{?dist} as per new policy

* Tue Jun 5 2007 Ben Konrath <bkonrath@redhat.com> - 0:0.1.31-1jpp.1
- 0.1.31.

* Tue Apr 3 2007 Ben Konrath <bkonrath@redhat.com> - 0:0.1.28-1jpp.6
- Add OSGi Manifest to jar.
- Disable aot-compile-rpm on ia64. 

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.1.28-1jpp.5
- Updated changelog entries in spec.

* Fri Aug 04 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.1.28-1jpp.4
- Added conditional compiling support.
- Added missing requirements.
- Additionally, for synchronizaion between logs:
- From r.apel@r-apel.de:
  - 0.1.26
- From fnasser@redhat.com:
  - 0.1.20

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:0.1.28-1jpp_3fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.28-1jpp_2fc
- rebuild

* Thu Jun  1 2006 Ben Konrath <bkonrath@redhat.com> - 0:0.1.28-1jpp_1fc
- 0.1.28
- Add BuildRequires ant.

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:0.1.18-1jpp_7fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.18-1jpp_6fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.18-1jpp_5fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_4fc
- Rebuild again

* Tue Dec 13 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_3fc
- Rebuild with gcc 4.1.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Gary Benson <gbenson@redhat.com> 0.1.18-1jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Fri Apr 22 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_1fc
- Build into Fedora.
- Natively-compile.

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.18-1jpp_1rh
- Merge with upstream for 0.1.18 upgrade

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.18-1jpp
- 0.1.18

* Fri Mar 18 2005 Andrew Overholt <overholt@redhat.com> 0.1.17-2jpp_1fc
- Build into Fedora.
- Remove Distribution and Vendor tags.
- Add BuildRequires:  java-devel for javadoc requirement.

* Tue Nov 02 2004 David Walluck <david@jpackage.org> 0:0.1.17-2jpp
- rebuild with jdk 1.4.2

* Tue Oct 19 2004 David Walluck <david@jpackage.org> 0:0.1.17-1jpp
- 0.1.17

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:0.1.13-2jpp
- Rebuild with ant-1.6.2

* Sat Feb 14 2004 David Walluck <david@anti-microsoft.org> 0:0.1.13-1jpp
- 0.1.13

* Wed Jan 14 2004 Ralph Apel <r.apel@r-apel.de> - 0:0.1.12-1jpp
- First JPackage build.
