# TODO:
# - use PLD ldflags
# - cleanup

# Conditional build:
%bcond_with	static_libs	# build static libraries
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_with	nas		# NAS audio support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	system_phonon	# phonon libraries from phonon.spec intead of qt4.spec
%bcond_with	wkhtml		# WKHTMLTOPDF patch (affects QtGui ABI)
# -- databases
%bcond_without	mysql		# MySQL plugin
%bcond_without	odbc		# unixODBC plugin
%bcond_without	pgsql		# PostgreSQL plugin
%bcond_without	sqlite3		# SQLite3 plugin
%bcond_without	sqlite		# SQLite2 plugin
%bcond_without	ibase		# ibase (InterBase/Firebird) plugin
# -- SIMD CPU instructions
%bcond_with	sse		# use SSE instructions in gui/painting module
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3		# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41		# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42		# use SSE4.2 instructions (the same)
%bcond_with	avx		# use AVX instructions (future Intel x86 CPUs only)

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
# any SQL
%define		_withsql	1
%{!?with_sqlite3:%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}}

%define		icu_abi		52
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

%define		orgname		qtbase
Summary:	The Qt5 application framework
Summary(es.UTF-8):	Biblioteca para ejecutar aplicaciones Qt5
Summary(pl.UTF-8):	Biblioteka Qt5
Summary(pt_BR.UTF-8):	Estrutura para rodar aplicações Qt5
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	c94bbaf1bb7f0f4a32d2caa7501416e1
URL:		http://qt-project.org/
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	Mesa-libOpenVG-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel >= 0.93
BuildRequires:	fontconfig-devel
BuildRequires:	freetds-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gstreamer0.10-plugins-base-devel
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.10}
# see dependency on libicu version below
BuildRequires:	libicu-devel >= %{icu_abi}
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pulseaudio-devel >= 0.9.10
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	rsync
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_noautostrip	'.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing

%define		_qtdir		%{_libdir}/qt5

%description
Qt5 base libraries.

%package devel
Summary:	The Qt5 application framework - development files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Qt5 - development files.

%package examples
Summary:	Qt5 examples
Group:		X11/Development/Libraries

%description examples
Qt5 - examples.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%{__sed} -i -e 's,usr/X11R6/,usr/g,' mkspecs/linux-g++-64/qmake.conf \
	mkspecs/common/linux.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|QMAKE_CC.*=.*gcc|QMAKE_CC\t\t= %{__cc}|;
	s|QMAKE_CXX.*=.*g++|QMAKE_CXX\t\t= %{__cxx}|;
	s|QMAKE_LINK.*=.*g++|QMAKE_LINK\t\t= %{__cxx}|;
	s|QMAKE_LINK_SHLIB.*=.*g++|QMAKE_LINK_SHLIB\t= %{__cxx}|;
	s|QMAKE_CFLAGS_RELEASE.*|QMAKE_CFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcflags}|;
	s|QMAKE_CXXFLAGS_RELEASE.*|QMAKE_CXXFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcxxflags}|;
	s|QMAKE_CFLAGS_DEBUG.*|QMAKE_CFLAGS_DEBUG\t+= %{debugcflags}|;
	s|QMAKE_CXXFLAGS_DEBUG.*|QMAKE_CXXFLAGS_DEBUG\t+= %{debugcflags}|;
	' mkspecs/common/g++-base.conf

#%{__sed} -i -e '
#	s|QMAKE_INCDIR_QT.*|QMAKE_INCDIR_QT       = %{_includedir}/qt4|;
#	' mkspecs/common/linux.conf

# No -L/usr/lib.
%{__sed} -i -e '
	s|^QMAKE_LIBDIR_QT.*=.*|QMAKE_LIBDIR_QT       =|;
	' mkspecs/common/linux.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
%{__sed} -i -e '
	s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|;
	' mkspecs/common/linux.conf

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

COMMONOPT=" \
	-confirm-license \
	-opensource \
	-verbose \
	-prefix %{_qtdir} \
	-bindir %{_qtdir}/bin \
	-docdir %{_docdir}/qt5-doc \
	-headerdir %{_includedir}/qt5 \
	-libdir %{_libdir} \
	-plugindir %{_qtdir}/plugins \
	-datadir %{_datadir}/qt5 \
	-translationdir %{_localedir}/ \
	-sysconfdir %{_sysconfdir}/qt5 \
	-examplesdir %{_examplesdir}/qt5 \
	-optimized-qmake \
	-glib \
	%{!?with_gtk:-no-gtkstyle} \
	-%{!?with_pch:no-}pch \
	-no-rpath \
	%{!?with_sse:-no-sse} \
	%{!?with_sse2:-no-sse2} \
	%{!?with_sse3:-no-sse3} \
	%{!?with_ssse3:-no-ssse3} \
	%{!?with_sse41:-no-sse4.1} \
	%{!?with_sse42:-no-sse4.2} \
	%{!?with_avx:-no-avx} \
	-dbus \
	-dbus-linked \
	-reduce-relocations \
	-system-freetype \
	-system-libjpeg \
	-system-libpng \
	-system-pcre \
	-system-xcb \
	-system-xkbcommon \
	-system-zlib \
	-openssl-linked \
	-largefile \
	-I/usr/include/postgresql/server \
	-I/usr/include/mysql \
	%{?with_cups:-cups} \
	%{?with_nas:-system-nas-sound} \
	%{?debug:-debug} \
	%{!?debug:-release} \
	-fontconfig \
	-largefile \
	-iconv \
	-icu \
	-no-separate-debug-info \
	-xfixes \
	-nis \
	-sm \
	-xcursor \
	-xinput2 \
	-xinerama \
	-xrandr \
	-xkb \
	-xrender \
	-xshape \
	-continue"

%if 0
##################################
#       STATIC MULTI-THREAD      #
##################################

%if %{with static_libs}
OPT=" \
	-%{!?with_mysql:no}%{?with_mysql:qt}-sql-mysql \
	-%{!?with_odbc:no}%{?with_odbc:qt}-sql-odbc \
	-%{!?with_pgsql:no}%{?with_pgsql:qt}-sql-psql \
	-%{!?with_sqlite3:no}%{?with_sqlite3:qt}-sql-sqlite \
	-%{!?with_sqlite:no}%{?with_sqlite:qt}-sql-sqlite2 \
	-%{!?with_ibase:no}%{?with_ibase:qt}-sql-ibase \
	-static"

./configure $COMMONOPT $OPT

%{__make} -C src
%{__make} -C tools/assistant/lib
%{__make} -C tools/designer
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} distclean
%endif
%endif

##################################
#       SHARED MULTI-THREAD      #
##################################

OPT=" \
	-%{!?with_mysql:no}%{?with_mysql:plugin}-sql-mysql \
	-%{!?with_odbc:no}%{?with_odbc:plugin}-sql-odbc \
	-%{!?with_pgsql:no}%{?with_pgsql:plugin}-sql-psql \
	-%{!?with_sqlite3:no}%{?with_sqlite3:plugin}-sql-sqlite \
	-%{!?with_sqlite:no}%{?with_sqlite:plugin}-sql-sqlite2 \
	-%{!?with_ibase:no}%{?with_ibase:plugin}-sql-ibase \
	-shared"

./configure $COMMONOPT $OPT

%{__make}
#%{__make} \
#	sub-tools-all-ordered \
#	sub-demos-all-ordered \
#	sub-examples-all-ordered

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{env.d,qt5},%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_pkgconfigdir}}
#install -d $RPM_BUILD_ROOT%{_qtdir}/plugins/{crypto,network}

#echo '#QT_GRAPHICSSYSTEM=raster' > $RPM_BUILD_ROOT/etc/env.d/QT_GRAPHICSSYSTEM

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# for qt-creator sth is messed up in the Makefile, nothing for make install
#install bin/qdoc3 $RPM_BUILD_ROOT%{_qtdir}/bin/qdoc3

# kill -L/inside/builddir from *.la and *.pc (bug #77152)
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_libdir}/*.{la,prl}
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc
%{__sed} -i -e '
	s|moc_location=.*|moc_location=%{_bindir}/moc-qt5|;
	s|uic_location=.*|uic_location=%{_bindir}/uic-qt5|;
	' $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# libQtWebKit.la contains '-ljscore' and '-lwebcore', they come
# from src/3rdparty/webkit/{JavaScriptCore,WebCore}} but those libs aren't installed
#%{__sed} -i -e "s,-lwebcore,,g;s,-ljscore,,g;" $RPM_BUILD_ROOT%{_libdir}/libQtWebKit.la

# install tools
install bin/findtr	$RPM_BUILD_ROOT%{_qtdir}/bin

cd $RPM_BUILD_ROOT%{_bindir}
#ln -sf ../%{_lib}/qt5/bin/assistant assistant-qt5
#ln -sf ../%{_lib}/qt5/bin/designer designer-qt5
ln -sf ../%{_lib}/qt5/bin/findtr findtr-qt5
#ln -sf ../%{_lib}/qt5/bin/linguist linguist-qt5
#ln -sf ../%{_lib}/qt5/bin/lrelease lrelease-qt5
#ln -sf ../%{_lib}/qt5/bin/lupdate lupdate-qt5
ln -sf ../%{_lib}/qt5/bin/moc moc-qt5
ln -sf ../%{_lib}/qt5/bin/qmake qmake-qt5
#ln -sf ../%{_lib}/qt5/bin/qtconfig qtconfig-qt5
ln -sf ../%{_lib}/qt5/bin/uic uic-qt5
ln -sf ../%{_lib}/qt5/bin/rcc rcc-qt5
#ln -sf ../%{_lib}/qt5/bin/pixeltool .
#ln -sf ../%{_lib}/qt5/bin/qcollectiongenerator .
ln -sf ../%{_lib}/qt5/bin/qdbuscpp2xml qdbuscpp2xml-qt5
ln -sf ../%{_lib}/qt5/bin/qdbusxml2cpp qdbusxml2cpp-qt5
ln -sf ../%{_lib}/qt5/bin/qdoc qdoc-qt5
#ln -sf ../%{_lib}/qt5/bin/qhelpconverter .
#ln -sf ../%{_lib}/qt5/bin/qhelpgenerator .
#ln -sf ../%{_lib}/qt5/bin/qmlviewer .
#ln -sf ../%{_lib}/qt5/bin/qmlplugindump .
#ln -sf ../%{_lib}/qt5/bin/qttracereplay .
#ln -sf ../%{_lib}/qt5/bin/qvfb .
#ln -sf ../%{_lib}/qt5/bin/xmlpatternsvalidator .
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

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/libQt5Concurrent.so.?
%attr(755,root,root) %{_libdir}/libQt5Concurrent.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Core.so.?
%attr(755,root,root) %{_libdir}/libQt5Core.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5DBus.so.?
%attr(755,root,root) %{_libdir}/libQt5DBus.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Gui.so.?
%attr(755,root,root) %{_libdir}/libQt5Gui.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Network.so.?
%attr(755,root,root) %{_libdir}/libQt5Network.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5OpenGL.so.?
%attr(755,root,root) %{_libdir}/libQt5OpenGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5PrintSupport.so.?
%attr(755,root,root) %{_libdir}/libQt5PrintSupport.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Sql.so.?
%attr(755,root,root) %{_libdir}/libQt5Sql.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Test.so.?
%attr(755,root,root) %{_libdir}/libQt5Test.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Widgets.so.?
%attr(755,root,root) %{_libdir}/libQt5Widgets.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Xml.so.?
%attr(755,root,root) %{_libdir}/libQt5Xml.so.*.*
%{_libdir}/libQt5Bootstrap.a
%{_libdir}/libQt5OpenGLExtensions.a
%{_libdir}/libQt5PlatformSupport.a

%dir /etc/qt5
%dir %{_qtdir}
%dir %{_qtdir}/bin
%attr(755,root,root) %{_qtdir}/bin/*
%attr(755,root,root) %{_qtdir}/plugins

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

%{_libdir}/libQt5Concurrent.la
%{_libdir}/libQt5Core.la
%{_libdir}/libQt5DBus.la
%{_libdir}/libQt5Gui.la
%{_libdir}/libQt5Network.la
%{_libdir}/libQt5OpenGL.la
%{_libdir}/libQt5PrintSupport.la
%{_libdir}/libQt5Sql.la
%{_libdir}/libQt5Test.la
%{_libdir}/libQt5Widgets.la
%{_libdir}/libQt5Xml.la

%{_libdir}/libQt5Concurrent.prl
%{_libdir}/libQt5Core.prl
%{_libdir}/libQt5DBus.prl
%{_libdir}/libQt5Gui.prl
%{_libdir}/libQt5Network.prl
%{_libdir}/libQt5OpenGL.prl
%{_libdir}/libQt5PrintSupport.prl
%{_libdir}/libQt5Sql.prl
%{_libdir}/libQt5Test.prl
%{_libdir}/libQt5Widgets.prl
%{_libdir}/libQt5Xml.prl

%{_libdir}/libQt5Bootstrap.la
%{_libdir}/libQt5Bootstrap.prl
%{_libdir}/libQt5OpenGLExtensions.la
%{_libdir}/libQt5OpenGLExtensions.prl
%{_libdir}/libQt5PlatformSupport.la
%{_libdir}/libQt5PlatformSupport.prl

%{_includedir}/qt5
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
%{_pkgconfigdir}/*.pc
#%{_examplesdir}/qt5
%{_docdir}/qt5-doc
%{_qtdir}/mkspecs

%files examples -f examples.files
