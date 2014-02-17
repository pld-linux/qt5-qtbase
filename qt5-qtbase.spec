# TODO:
# - libraries split (per-library or at least base/gui parts)
# - separate some plugins (SQL, DirectFB...)

# Conditional build:
%bcond_with	static_libs	# static libraries [incomplete support in .spec]
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_without	directfb	# DirectFB platform support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	tslib		# tslib support
# -- databases
%bcond_without	freetds		# TDS (Sybase/MS SQL) plugin
%bcond_without	mysql		# MySQL plugin
%bcond_without	odbc		# unixODBC plugin
%bcond_without	pgsql		# PostgreSQL plugin
%bcond_without	sqlite2		# SQLite2 plugin
%bcond_without	sqlite3		# SQLite3 plugin
%bcond_without	ibase		# ibase (InterBase/Firebird) plugin
%bcond_with	db2		# DB2 support
%bcond_with	oracle		# OCI (Oracle) support
# -- SIMD CPU instructions
%bcond_with	sse		# use SSE instructions in gui/painting module
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3		# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41		# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42		# use SSE4.2 instructions (the same)
%bcond_with	avx		# use AVX instructions (Intel since Sandy Bridge, AMD since Bulldozer)
%bcond_with	avx2		# use AVX2 instructions (Intel since Haswell)

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%ifarch	athlon
%define		with_3dnow	1
%endif
%ifarch athlon pentium3 pentium4 %{x8664}
%define		with_mmx	1
%endif
%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664}
%define		with_sse2	1
%endif

%define		icu_abi		52
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

%define		orgname		qtbase
Summary:	Qt5 - base components
Summary(pl.UTF-8):	Biblioteka Qt5 - podstawowe komponenty
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License:	LGPLv2 with exceptions or GPLv3 with exceptions
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	c94bbaf1bb7f0f4a32d2caa7501416e1
URL:		http://qt-project.org/
%{?with_directfb:BuildRequires:	DirectFB-devel}
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	Mesa-libOpenVG-devel
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
%{?with_gtk:BuildRequires:	atk-devel}
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	fontconfig-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.18}
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libxcb-devel >= 1.5
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	pcre16-devel >= 8.30
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pulseaudio-devel >= 0.9.10
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	sed >= 4.0
%{?with_sqlite2:BuildRequires:	sqlite-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRequires:	tar >= 1:1.22
%{?with_tslib:BuildRequires:	tslib-devel}
BuildRequires:	udev-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	xcb-util-image-devel
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-renderutil-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.2.0
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%define		qt5dir		%{_libdir}/qt5

%description
Qt is a software toolkit for developing applications.

This package contains base components, like Core, Network or Xml.

%description -l pl.UTF-8
Qt to programowy toolkit do tworzenia aplikacji.

Ten pakiet zawiera podstawowe komponenty, takie jak Core, Network czy
Xml.

%package devel
Summary:	The Qt5 application framework - development files
Summary(pl.UTF-8):	Szkielet aplikacji Qt5 - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The Qt5 application framework - development files.

%description devel -l pl.UTF-8
Szkielet aplikacji Qt5 - pliki programistyczne.

%package doc
Summary:	Documentation for Qt5 application framework base components
Summary(pl.UTF-8):	Dokumentacja do podstawowych komponentów szkieletu aplikacji Qt5
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for Qt5 application framework base components.

%description doc -l pl.UTF-8
Dokumentacja do podstawowych komponentów szkieletu aplikacji Qt5.

%package examples
Summary:	Examples for Qt5 application framework base components
Summary(pl.UTF-8):	Przykłady do podstawowych komponentów szkieletu aplikacji Qt5
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Examples for Qt5 application framework base components.

%description examples -l pl.UTF-8
Przykłady do podstawowych komponentów szkieletu aplikacji Qt5.

%package -n qt5-build
Summary:	Qt5 build tools
Summary(pl.UTF-8):	Narzędzia do budowania dla Qt4
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description -n qt5-build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) etc.

%description -n qt5-build -l pl.UTF-8
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów użytkownika (uic) i podobne
narzędzia.

%package -n qt5-qmake
Summary:	Qt5 makefile generator
Summary(pl.UTF-8):	Generator plików makefile dla aplikacji Qt5
Group:		Development/Tools

%description -n qt5-qmake
Qt5 makefile generator.

%description -n qt5-qmake -l pl.UTF-8
Generator plików makefile dla aplikacji Qt5.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%{__sed} -i -e 's,usr/X11R6/,usr/g,' mkspecs/linux-g++-64/qmake.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|^\(QMAKE_COMPILER *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CC *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CXX *\)=.*g++|\1= %{__cxx}|;
	s|^QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO .*|QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO += -g %{rpmcppflags} %{rpmcflags}|;
	s|^QMAKE_CXXFLAGS_RELEASE_WITH_DEBUGINFO .*|QMAKE_CXXFLAGS_RELEASE_WITH_DEBUGINFO += -g %{rpmcppflags} %{rpmcxxflags}|;
	' mkspecs/common/g++-base.conf
%{__sed} -i -e '
	s|^\(QMAKE_CFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcflags}|;
	s|^\(QMAKE_CXXFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcxxflags}|;
	s|^\(QMAKE_CFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_CXXFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_LFLAGS *\)+=.*|\1+= %{rpmldflags}|;
	' mkspecs/common/gcc-base.conf

# define QMAKE_STRIP to true, so we get useful -debuginfo pkgs
%{__sed} -i -e '
	s|^\(QMAKE_STRIP *\)=.*|\1= :|;
	' mkspecs/common/linux.conf

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

# DEFAULT OPTIONS FOR ALL BUILDS
COMMONOPT=" \
	-confirm-license \
	-opensource \
	-verbose \
	%{?debug:-debug} \
	%{!?debug:-release} \
	-prefix %{qt5dir} \
	-bindir %{qt5dir}/bin \
	-docdir %{_docdir}/qt5-doc \
	-headerdir %{_includedir}/qt5 \
	-libdir %{_libdir} \
	-plugindir %{qt5dir}/plugins \
	-datadir %{_datadir}/qt5 \
	-translationdir %{_localedir} \
	-sysconfdir %{_sysconfdir}/qt5 \
	-examplesdir %{_examplesdir}/qt5 \
%if %{with mysql}
	-I/usr/include/mysql \
%endif
%if %{with pgsql}
	-I/usr/include/postgresql/server \
%endif
	-%{!?with_cups:no-}cups \
	-%{!?with_directfb:no-}directfb \
	-dbus-linked \
	-fontconfig \
	-glib \
	-%{!?with_gtk:no-}gtkstyle \
	-iconv \
	-icu \
	-largefile \
	-nis \
	-no-rpath \
	-no-separate-debug-info \
	%{!?with_sse:-no-sse} \
	%{!?with_sse2:-no-sse2} \
	%{!?with_sse3:-no-sse3} \
	%{!?with_ssse3:-no-ssse3} \
	%{!?with_sse41:-no-sse4.1} \
	%{!?with_sse42:-no-sse4.2} \
	%{!?with_avx:-no-avx} \
	%{!?with_avx2:-no-avx2} \
	-openssl-linked \
	-optimized-qmake \
	-%{!?with_pch:no-}pch \
	-reduce-relocations \
	-sm \
	-system-freetype \
	-system-libjpeg \
	-system-libpng \
	-system-pcre \
	-system-sqlite \
	-system-xcb \
	-system-xkbcommon \
	-system-zlib \
	%{?with_tslib:-tslib} \
	-xcursor \
	-xfixes \
	-xinerama \
	-xinput2 \
	-xkb \
	-xrandr \
	-xrender \
	-xshape"

# STATIC
%if %{with static_libs}
OPT=" \
	--sql-db2=%{?with_db2:qt}%{!?with_db2:no} \
	--sql-ibase=%{?with_ibase:qt}%{!?with_ibase:no} \
	--sql-mysql=%{?with_mysql:qt}%{!?with_mysql:no} \
	--sql-oci=%{?with_oracle:qt}%{!?with_oracle:no} \
	--sql-odbc=%{?with_odbc:qt}%{!?with_odbc:no} \
	--sql-psql=%{?with_pgsql:qt}%{!?with_pgsql:no} \
	--sql-sqlite2=%{?with_sqlite2:qt}%{!?with_sqlite2:no} \
	--sql-sqlite=%{?with_sqlite3:qt}%{!?with_sqlite3:no} \
	--sql-tds=%{?with_freetds:qt}%{!?with_freetds:no} \
	-static"

./configure $COMMONOPT $OPT

%{__make} -C src
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} distclean
%endif

# SHARED
OPT=" \
	--sql-db2=%{?with_db2:plugin}%{!?with_db2:no} \
	--sql-ibase=%{?with_ibase:plugin}%{!?with_ibase:no} \
	--sql-mysql=%{?with_mysql:plugin}%{!?with_mysql:no} \
	--sql-oci=%{?with_oracle:plugin}%{!?with_oracle:no} \
	--sql-odbc=%{?with_odbc:plugin}%{!?with_odbc:no} \
	--sql-psql=%{?with_pgsql:plugin}%{!?with_pgsql:no} \
	--sql-sqlite2=%{?with_sqlite2:plugin}%{!?with_sqlite2:no} \
	--sql-sqlite=%{?with_sqlite3:plugin}%{!?with_sqlite3:no} \
	--sql-tds=%{?with_freetds:plugin}%{!?with_freetds:no} \
	-shared"

./configure $COMMONOPT $OPT

%{__make}

# use just built qdoc instead of requiring already installed qt5-build
wd="$(pwd)"
%{__sed} -i -e 's|%{qt5dir}/bin/qdoc|LD_LIBRARY_PATH='${wd}'/lib$${LD_LIBRARY_PATH:+:$$LD_LIBRARY_PATH} '${wd}'/bin/qdoc|' src/*/Makefile
# build only HTML docs (qch docs require qhelpgenerator)
%{__make} html_docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/qt5,%{_bindir},%{_pkgconfigdir}}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_html_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# kill unnecessary -L%{_libdir} from *.la, *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.{la,prl} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# install tools
install bin/findtr	$RPM_BUILD_ROOT%{qt5dir}/bin
# symlinks in system bin dir
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt5/bin/findtr findtr-qt5
ln -sf ../%{_lib}/qt5/bin/moc moc-qt5
ln -sf ../%{_lib}/qt5/bin/qmake qmake-qt5
ln -sf ../%{_lib}/qt5/bin/uic uic-qt5
ln -sf ../%{_lib}/qt5/bin/rcc rcc-qt5
ln -sf ../%{_lib}/qt5/bin/qdbuscpp2xml qdbuscpp2xml-qt5
ln -sf ../%{_lib}/qt5/bin/qdbusxml2cpp qdbusxml2cpp-qt5
ln -sf ../%{_lib}/qt5/bin/qdoc qdoc-qt5
cd -

# Prepare some files list
ifecho() {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return # XXX this is never true due $RPM_BUILD_ROOT being set
	r=`echo $RESULT | awk '{ print $1 }'`

	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt5
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt5 -printf "%%P "`; do
	ifecho examples %{_examplesdir}/qt5/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Concurrent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Concurrent.so.5
%attr(755,root,root) %{_libdir}/libQt5Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Core.so.5
%attr(755,root,root) %{_libdir}/libQt5DBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5DBus.so.5
%attr(755,root,root) %{_libdir}/libQt5Gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Gui.so.5
%attr(755,root,root) %{_libdir}/libQt5Network.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Network.so.5
%attr(755,root,root) %{_libdir}/libQt5OpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5OpenGL.so.5
%attr(755,root,root) %{_libdir}/libQt5PrintSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5PrintSupport.so.5
%attr(755,root,root) %{_libdir}/libQt5Sql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Sql.so.5
%attr(755,root,root) %{_libdir}/libQt5Test.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Test.so.5
%attr(755,root,root) %{_libdir}/libQt5Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Widgets.so.5
%attr(755,root,root) %{_libdir}/libQt5Xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Xml.so.5

%dir /etc/qt5
%dir %{qt5dir}
%dir %{qt5dir}/bin
%dir %{qt5dir}/plugins
# loaded from src/gui/accessible/qaccessible.cpp
%dir %{qt5dir}/plugins/accessible
%attr(755,root,root) %{qt5dir}/plugins/accessible/libqtaccessiblewidgets.so
# loaded from src/network/bearer/qnetworkconfigmanager_p.cpp
%dir %{qt5dir}/plugins/bearer
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqconnmanbearer.so
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqgenericbearer.so
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqnmbearer.so
# loaded from src/gui/kernel/qgenericpluginfactory.cpp
%dir %{qt5dir}/plugins/generic
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevkeyboardplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevmouseplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevtabletplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevtouchplugin.so
%if %{with tslib}
%attr(755,root,root) %{qt5dir}/plugins/generic/libqtslibplugin.so
%endif
# loaded from src/gui/image/qimage{reader,writer}.cpp
%dir %{qt5dir}/plugins/imageformats
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqgif.so
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqico.so
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqjpeg.so
# loaded from src/gui/kernel/qplatforminputcontextfactory.cpp
%dir %{qt5dir}/plugins/platforminputcontexts
%attr(755,root,root) %{qt5dir}/plugins/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%attr(755,root,root) %{qt5dir}/plugins/platforminputcontexts/libibusplatforminputcontextplugin.so
# loaded from src/gui/kernel/qplatformintegrationfactory.cpp
%dir %{qt5dir}/plugins/platforms
%if %{with directfb}
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqdirectfb.so
%endif
# -kms, requires GLESv2 instead of GL
#%attr(755,root,root) %{qt5dir}/plugins/platforms/libqkms.so
# -eglfs, requires GLESv2 instead of GL
#%attr(755,root,root) %{qt5dir}/plugins/platforms/libqeglfs.so
#%attr(755,root,root) %{qt5dir}/plugins/platforms/libqminimalegl.so
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqlinuxfb.so
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqminimal.so
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqoffscreen.so
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqxcb.so
# loaded from src/gui/kernel/qplatformthemefactory.cpp
%dir %{qt5dir}/plugins/platformthemes
%if %{with gtk}
%attr(755,root,root) %{qt5dir}/plugins/platformthemes/libqgtk2.so
%endif
# loaded from src/printsupport/kernel/qplatformprintplugin.cpp
%dir %{qt5dir}/plugins/printsupport
%if %{with cups}
%attr(755,root,root) %{qt5dir}/plugins/printsupport/libcupsprintersupport.so
%endif
# loaded from src/sql/kernel/qsqldatabase.cpp
%dir %{qt5dir}/plugins/sqldrivers
%if %{with db2}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqldb2.so
%endif
%if %{with ibase}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlibase.so
%endif
%if %{with sqlite3}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlite.so
%endif
%if %{with sqlite2}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlite2.so
%endif
%if %{with mysql}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlmysql.so
%endif
%if %{with oracle}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqloci.so
%endif
%if %{with odbc}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlodbc.so
%endif
%if %{with pgsql}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlpsql.so
%endif
%if %{with freetds}
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqltds.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Concurrent.so
%attr(755,root,root) %{_libdir}/libQt5Core.so
%attr(755,root,root) %{_libdir}/libQt5DBus.so
%attr(755,root,root) %{_libdir}/libQt5Gui.so
%attr(755,root,root) %{_libdir}/libQt5Network.so
%attr(755,root,root) %{_libdir}/libQt5OpenGL.so
%attr(755,root,root) %{_libdir}/libQt5PrintSupport.so
%attr(755,root,root) %{_libdir}/libQt5Sql.so
%attr(755,root,root) %{_libdir}/libQt5Test.so
%attr(755,root,root) %{_libdir}/libQt5Widgets.so
%attr(755,root,root) %{_libdir}/libQt5Xml.so
# static-inly
%{_libdir}/libQt5Bootstrap.a
%{_libdir}/libQt5OpenGLExtensions.a
%{_libdir}/libQt5PlatformSupport.a

%{_libdir}/libQt5Bootstrap.prl
%{_libdir}/libQt5Concurrent.prl
%{_libdir}/libQt5Core.prl
%{_libdir}/libQt5DBus.prl
%{_libdir}/libQt5Gui.prl
%{_libdir}/libQt5Network.prl
%{_libdir}/libQt5OpenGL.prl
%{_libdir}/libQt5OpenGLExtensions.prl
%{_libdir}/libQt5PlatformSupport.prl
%{_libdir}/libQt5PrintSupport.prl
%{_libdir}/libQt5Sql.prl
%{_libdir}/libQt5Test.prl
%{_libdir}/libQt5Widgets.prl
%{_libdir}/libQt5Xml.prl

%dir %{_includedir}/qt5
%{_includedir}/qt5/QtConcurrent
%{_includedir}/qt5/QtCore
%{_includedir}/qt5/QtDBus
%{_includedir}/qt5/QtGui
%{_includedir}/qt5/QtNetwork
%{_includedir}/qt5/QtOpenGL
%{_includedir}/qt5/QtOpenGLExtensions
%{_includedir}/qt5/QtPlatformSupport
%{_includedir}/qt5/QtPrintSupport
%{_includedir}/qt5/QtSql
%{_includedir}/qt5/QtTest
%{_includedir}/qt5/QtWidgets
%{_includedir}/qt5/QtXml

%{_pkgconfigdir}/Qt5Bootstrap.pc
%{_pkgconfigdir}/Qt5Concurrent.pc
%{_pkgconfigdir}/Qt5Core.pc
%{_pkgconfigdir}/Qt5DBus.pc
%{_pkgconfigdir}/Qt5Gui.pc
%{_pkgconfigdir}/Qt5Network.pc
%{_pkgconfigdir}/Qt5OpenGL.pc
%{_pkgconfigdir}/Qt5OpenGLExtensions.pc
%{_pkgconfigdir}/Qt5PlatformSupport.pc
%{_pkgconfigdir}/Qt5PrintSupport.pc
%{_pkgconfigdir}/Qt5Sql.pc
%{_pkgconfigdir}/Qt5Test.pc
%{_pkgconfigdir}/Qt5Widgets.pc
%{_pkgconfigdir}/Qt5Xml.pc

%{_libdir}/cmake/Qt5
%{_libdir}/cmake/Qt5Concurrent
%{_libdir}/cmake/Qt5Core
%{_libdir}/cmake/Qt5DBus
%{_libdir}/cmake/Qt5Gui
%{_libdir}/cmake/Qt5Network
%{_libdir}/cmake/Qt5OpenGL
%{_libdir}/cmake/Qt5OpenGLExtensions
%{_libdir}/cmake/Qt5PrintSupport
%{_libdir}/cmake/Qt5Sql
%{_libdir}/cmake/Qt5Test
%{_libdir}/cmake/Qt5Widgets
%{_libdir}/cmake/Qt5Xml

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc

%files examples -f examples.files

%files -n qt5-build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/findtr-qt5
%attr(755,root,root) %{_bindir}/moc-qt5
%attr(755,root,root) %{_bindir}/qdbuscpp2xml-qt5
%attr(755,root,root) %{_bindir}/qdbusxml2cpp-qt5
%attr(755,root,root) %{_bindir}/qdoc-qt5
%attr(755,root,root) %{_bindir}/rcc-qt5
%attr(755,root,root) %{_bindir}/uic-qt5
%attr(755,root,root) %{qt5dir}/bin/findtr
%attr(755,root,root) %{qt5dir}/bin/moc
%attr(755,root,root) %{qt5dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt5dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt5dir}/bin/qdoc
%attr(755,root,root) %{qt5dir}/bin/rcc
%attr(755,root,root) %{qt5dir}/bin/syncqt.pl
%attr(755,root,root) %{qt5dir}/bin/uic

%files -n qt5-qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake-qt5
%attr(755,root,root) %{qt5dir}/bin/qmake
%{qt5dir}/mkspecs
